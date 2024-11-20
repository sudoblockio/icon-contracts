import json
import os
import shutil
import subprocess
import zipfile
from typing import Any, Type

from google.protobuf.json_format import MessageToJson
from pydantic import ValidationError

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.metrics import Metrics
from icon_contracts.models.contracts import Contract
from icon_contracts.models.social_media import SocialMedia
from icon_contracts.models.verification_contract import VerificationInput
from icon_contracts.schemas.block_etl_pb2 import BlockETL  # noqa
from icon_contracts.schemas.block_etl_pb2 import LogETL  # noqa
from icon_contracts.schemas.block_etl_pb2 import TransactionETL  # noqa
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.utils.api import get_first_tx
from icon_contracts.utils.contract_content import (  # get_contract_name,
    get_s3_client,
    github_release_to_dir,
    upload_to_s3,
    zip_content_to_dir,
)
from icon_contracts.utils.rpc import getScoreStatus, icx_getTransactionResult
from icon_contracts.utils.zip import unzip_safe
from icon_contracts.workers.db import session_factory
from icon_contracts.workers.kafka import Worker
from icon_contracts.workers.verification import (
    compare_source,
    get_on_chain_contract_src,
    get_source_code_head_dir,
    replace_build_tool,
)

metrics = Metrics()

ADDRESSES_PROCESSED = set()

CONTRACT_VERIFICATION_CONTRACTS = {
    "cxfc514c18d8dd85f06e31509a1f231efc5d8939e0",  # Mainnet
    "cx4a574176f82852487b547126b7a59874f5599acd",  # Berlin
    "cx59fd09b8fd87ad82961c29c4ff5e44773f629330",  # Lisbon
}


# BTP_CONTRACTS_LIST = [
#     "",
# ]


class TransactionsWorker(Worker):
    # Need to pipe this in due to bug in boto
    s3_client: Any = None

    # Metrics
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    msg: Any = None
    data: dict = None

    block: Type[BlockETL] = BlockETL()
    transaction: TransactionETL = None
    log: Type[LogETL] = None

    def upload_contract_source(self, contract, content):
        # If we have access credentials this is not None
        if self.s3_client:

            # Increment the revision number
            contract.revision_number += 1
            zip_name = f"{contract.address}_{contract.revision_number}"
            # Unzip the contents of the dict to a directory
            contract_path = zip_content_to_dir(content, zip_name)
            # Upload to
            upload_to_s3(self.s3_client, contract_path, zip_name)
            contract.source_code_link = f"https://{settings.CONTRACTS_S3_BUCKET}.s3.us-west-2.amazonaws.com/contract-sources/{zip_name}"
            # Cleanup
            shutil.rmtree(os.path.dirname(contract_path))
            logger.info(f"Uploaded contract to {contract.source_code_link}")
        else:
            logger.info(f"Skip uploading tx")

    def process_contract(self, content: str):
        """
        Process the contract by checking its status in the DB and uploading the
        source to S3 and including a download link in the DB.
        """
        r = icx_getTransactionResult(self.transaction.hash)
        if r is not None:
            tx_result = r.json()["result"]
        else:
            logger.info(f"Failed getting tx hash {self.transaction.hash}")
            return

        address = tx_result["scoreAddress"]

        # Check if there is a contract in the DB with that address otherwise create it
        contract = self.session.get(Contract, address)

        if contract is None:
            # In order process
            logger.info(f"Creating new contract address = {address} at block = {self.block.number}")
            contract = Contract(
                address=address,
                owner_address=self.transaction.from_address,
                last_updated_block=self.block.number,
                created_block=self.block.number,
                created_timestamp=self.transaction.timestamp,
                creation_hash=self.transaction.hash,
            )
            contract.extract_contract_details()

            # self.session.merge(contract)
            # self.session.commit()

        if self.data["contentType"] == "application/zip":
            contract.contract_type = "python"
            if contract.status is None:
                # Means we haven't seen the audit yet
                contract.status = "Pending"
        elif self.data["contentType"] == "application/java":
            contract.contract_type = "java"
            contract.status = "Active"
        else:
            raise Exception(f"Don't know contentType {self.data['contentType']}")

        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            contract.last_updated_block is None
            or self.block.number > contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(f"Updating contract address = {address} at block = {self.block.number}")
            self.contracts_updated_python += 1
            metrics.contracts_created_python.set(self.contracts_updated_python)

            # Upload to s3
            self.upload_contract_source(contract, content)

            contract.last_updated_block = self.block.number
            contract.last_updated_timestamp = self.transaction.timestamp

            # Method that classifies the contract based on ABI for IRC2 stuff
            contract.extract_contract_details()

            # Remove any verified contract link
            contract.verified_source_code_link = None
            contract.verified = False

        # Condition where we have already updated the record
        if (
            self.block.number <= contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(
                f"Updating contract creation for address = {address} at block = {self.block.number}"
            )
            contract.created_block = self.block.number
            contract.created_timestamp = self.transaction.timestamp
            contract.creation_hash = self.transaction.hash

            # Upload to s3
            self.upload_contract_source(contract, content)

        # Produce the record so adjacent services can find out about new contracts as
        # this is the only service that actually inspects the ABI and classifies the
        # contracts.
        self.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            self.transaction.hash,  # Keyed on hash
            # Convert the pydantic object to proto
            contract_to_proto(
                contract,
                contract_updated_block=self.block.number,
                is_creation=True,
            ),
        )

        # Commit the contract
        self.session.merge(contract)
        self.session.commit()

    def process_audit(self):
        data = json.loads(self.transaction.data)

        # Contract creation events
        if "contentType" in data:
            logger.info(f"Unknown event for with hash = {self.transaction.hash}")
            # No idea what is going on here.
            self.produce_json(
                topic=settings.PRODUCER_TOPIC_DLQ,
                key="unknown-event-content-type",
                value=MessageToJson(self.transaction),
            )
            self.json_producer.poll(0)
            return

        if "method" not in data:
            logger.info(f"No method found in audit hash {self.transaction.hash}")
            return

        if data["method"] not in ["acceptScore", "rejectScore"]:
            logger.info(f"Method not supported in audit hash {self.transaction.hash}")
            return

        # # Audit related events
        address = icx_getTransactionResult(data["params"]["txHash"]).json()["result"][
            "scoreAddress"
        ]

        status = None
        if data["method"] == "acceptScore":
            status = "Active"
        elif data["method"] == "rejectScore":
            status = "Rejected"

        contract = self.session.get(Contract, address)

        if contract is None:
            logger.info(
                f"Creating contract from approval for address = {address} at block = {self.block.number}"
            )
            self.contracts_created_python += 1
            metrics.contracts_created_python.set(self.contracts_created_python)
            contract = Contract(
                address=address,
                status=status,
            )
            contract.extract_contract_details()

        # Out of order processes
        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            contract.last_updated_timestamp is None or
            contract.last_updated_block is None or
            self.block.number > contract.last_updated_block
        ):
            logger.info(
                f"Updating contract status from approval for address = {address} at block = {self.block.number}"
            )
            self.contracts_updated_python += 1
            metrics.contracts_created_python.set(self.contracts_updated_python)

            contract.status = status
            contract.last_updated_block = self.block.number
            contract.last_updated_timestamp = self.transaction.timestamp

            # Method that classifies the contract based on ABI for IRC2 stuff
            contract.extract_contract_details()

            self.produce_protobuf(
                settings.PRODUCER_TOPIC_CONTRACTS,
                self.transaction.hash,  # Keyed on hash
                contract_to_proto(
                    contract,
                    contract_updated_block=self.block.number,
                    # contract_updated_hash=self.transaction.hash,
                    is_creation=False,
                ),
            )

            self.session.merge(contract)
            self.session.commit()

    def process_verification_social_media(self, params: VerificationInput):
        """Process social media contacts for verifiction txs."""

        social_media = self.session.get(SocialMedia, params.contract_address)
        if social_media is None:
            social_media = SocialMedia(**params.dict())

        # ignore_fields = ["source_code_location", "zipped_source_code"]
        for k, v in params.dict().items():
            if k not in SocialMedia.__fields__:
                continue

            setattr(social_media, k, v)

        self.session.merge(social_media)
        self.session.commit()

    def process_verification(self):
        """
        Process contract verifications. Only runs txs to the contract verification
        contract which adheres to a schema that we can control.

        Runs the following steps:
        1. Validates that the sender of the Tx is the owner of the contract
        2. Unzips the bytestring of the contract to `verified_source_code/`
            a. Remove any `build/` directories so to make it impossible for someone
            to provide a pre-built binary that is not what we are verifying
            b. Run gradlew Optimizedjar on it to produce the
        3. Unzip the resulting binary
        4. Downloads the binary that is on-chain from the backend `source_code_link`
        5. Does a file comparison of those two items to make sure they are the same
        6. Pushes the new source code to s3
        7. Stores a link in db and marks as verified

        Assumes that the backend has the latest version of the contract

        Results in the following directory structure:
        - /tmp/<random>/
            - verified_source_code.txt - From verification Tx
            - verified_source_code.zip - From txt
            - verified_source_code - From unzip
                - Remove all build dirs
                - Replace gradlew and wrapper with own version - safety?
                - Run gradlew optimized jar
                - Unzip the binary to verified_jar/ -> Binary path supplied from msg
            - verified_jar dir unzipped
            - on_chain_source_code - From the last updated source code - s3 downloaded
        """
        if not settings.ENABLE_CONTRACT_VERIFICATION:
            return

        data = json.loads(self.transaction.data)

        if "method" not in data or "params" not in data:
            return

        if data["method"] != "verify":
            return

        try:
            params = VerificationInput(**data["params"])
        except ValidationError as e:
            logger.info(f"Invalid input for contract verification {e}")
            return

        # Verify that the sender is the owner address for the contract
        contract = self.session.get(Contract, params.contract_address)
        if contract is None:
            logger.info(
                f"Contract verification Tx to {params.contract_address} not found with Tx hash {self.transaction.hash}"
            )
            return

        if contract.owner_address != self.transaction.from_address:
            logger.info(
                f"Contract verification Tx from {self.transaction.from_address} to {params.contract_address} not from owner with Tx hash {self.transaction.hash}"
            )
            return

        self.process_verification_social_media(params)

        # Verify that the source code is the same as what is on-chain
        tmp_path = None
        # chdir to /tmp/tmp<random>/
        try:
            # Unzip the source code
            output_name = "verified_source_code"

            # Handle sources - supporting zip within tx or refs to GH release
            if params.zipped_source_code != "":
                # Unzip the contents of the dict to a directory
                logger.info(f"Processing zip for {self.transaction.hash}")
                zip_path = zip_content_to_dir(params.zipped_source_code, output_name)

                # Unzip utility that protects against zip bombs
                contract_path = os.path.join(os.path.dirname(zip_path), output_name)
                unzip_safe(
                    input_zip=zip_path,
                    output_dir=contract_path,
                    contract_hash=self.transaction.hash,
                )
                tmp_path = os.path.dirname(contract_path)
                # This step is there for ambiguous zips - ie a dir or it's head dir
                source_code_head_dir = get_source_code_head_dir(os.path.join(tmp_path, output_name))
                verified_contract_path = os.path.join(tmp_path, output_name, source_code_head_dir)

            elif params.github_org != "":
                logger.info(f"Processing github release for {self.transaction.hash}")
                tmp_path, verified_contract_path = github_release_to_dir(output_name, params)
                shutil.make_archive(
                    os.path.join(tmp_path, output_name), "zip", verified_contract_path
                )
            else:
                logger.info(f"Unsupported verification format.")
                return

            logger.info(f"Validating in {tmp_path}")
            os.chdir(tmp_path)

            # Use an official gradlew builder and wrapper
            replace_build_tool(verified_contract_path)
            logger.info(f"Running gradlew on {verified_contract_path} path.")
            os.chdir(verified_contract_path)

            # Create the build command that will be
            process = ["./gradlew"]
            if params.gradle_target != "":
                process.append(":" + params.gradle_target + ":" + params.gradle_task)
            else:
                process.append(params.gradle_task)
            logger.info(f"Running gradle build command `{' '.join(process)}`")
            subprocess.run(process)

            # Find binary
            os.chdir(tmp_path)
            binary_path = os.path.join(verified_contract_path, params.source_code_location)
            if not os.path.exists(binary_path):
                logger.info(f"Binary not found in {binary_path} for {self.transaction.hash}")
                return

            # Unzip the optimized jar so that we can inspect each file
            with zipfile.ZipFile(binary_path, "r") as zip_ref:
                zip_ref.extractall("verified_jar/")

            # Downloads the on chain zipped binaries
            on_chain_src_dir = get_on_chain_contract_src(contract.source_code_link)

            # Compare binary to what is on-chain
            compare_source(on_chain_src_dir, "verified_jar")
            logger.info(f"Successfully compared {self.transaction.hash}")

            # Get the optimized jar file name
            link = f"https://{settings.CONTRACTS_S3_BUCKET}.s3.us-west-2.amazonaws.com/verified-contract-sources/{params.contract_address}.zip"

            upload_to_s3(
                self.s3_client,
                os.path.join(tmp_path, output_name) + ".zip",
                params.contract_address + ".zip",
                prefix="verified-contract-sources",
            )

            contract.verified_source_code_link = link
            contract.verified = True
            self.session.merge(contract)
            self.session.commit()

            # Cleanup
            shutil.rmtree(tmp_path)
            logger.info(f"Uploaded contract to {contract.verified_source_code_link}")
        except Exception as e:
            logger.info(f"Unable verify contract - {self.transaction.hash} - {e}")
            if settings.CONTRACT_VERIFICATION_CLEANUP and tmp_path is not None:
                if os.path.exists(tmp_path):
                    shutil.rmtree(os.path.dirname(tmp_path))

    def process_new_contract_tx(self, address: str):
        """
        Handles internally created contracts producing them to protobuf. Does this by
         extracting out the details and then if the contract is not in the DB,
         produces a msg for that contract.
        """

        contract = self.session.get(Contract, address)
        if contract is None:
            contract = Contract(address=address)

        # This method updates contract static details
        contract.extract_contract_details()

        # Adding other info for initial_block might screw up non-internal contracts
        if contract.last_updated_timestamp is None:
            contract.last_updated_timestamp = get_first_tx(address=contract.address)

        # We then need to produce this to proto
        self.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            self.transaction.hash,  # Keyed on hash
            # Convert the pydantic object to proto
            contract_to_proto(
                contract_db=contract,
                contract_updated_block=self.block.number,
                is_creation=True,
            ),
        )

        self.session.merge(contract)
        self.session.commit()

    def process_transaction(self):
        # Pass on any invalid Tx in this service
        if self.transaction.to_address == "" or self.transaction.status != "0x1":
            return

        # Check for new address and process them if they are a contract
        if (
            self.transaction.to_address[0:2] == "cx"
            and self.transaction.to_address not in ADDRESSES_PROCESSED
        ):
            self.process_new_contract_tx(address=self.transaction.to_address)
            ADDRESSES_PROCESSED.add(self.transaction.to_address)

        if (
            self.transaction.from_address[0:2] == "cx"
            and self.transaction.from_address not in ADDRESSES_PROCESSED
        ):
            self.process_new_contract_tx(address=self.transaction.from_address)
            ADDRESSES_PROCESSED.add(self.transaction.from_address)

        # Handle audit process
        elif self.transaction.to_address == settings.one_address:
            self.process_audit()

        # Handle verification process
        elif self.transaction.to_address in CONTRACT_VERIFICATION_CONTRACTS:
            self.process_verification()

        # elif self.transaction.to_address in BTP_CONTRACTS_LIST:
        #     self.process_btp()

        # Need to check the data field if there is a json payload otherwise we are not
        # interested in it in this context
        if str(self.transaction.data) != "":
            try:
                self.data = json.loads(self.transaction.data)
            except Exception:
                self.produce_json(
                    topic=settings.PRODUCER_TOPIC_DLQ,
                    key="unknown-event-content-type",
                    value=MessageToJson(self.transaction),
                )
                return
        else:
            return

        if self.data is not None:
            # These are contract creation Txs
            if "contentType" in self.data:
                if self.data["contentType"] in ["application/zip", "application/java"]:
                    logger.info(f"Handling contract creation hash {self.transaction.hash}.")
                    self.process_contract(self.data["content"])

    def process(self):
        value = self.msg.value()
        if value is None:
            return
        self.block.ParseFromString(value)
        # Logic that handles backfills so that they do not continue to consume records
        # past the offset that the job was set off at.
        self.handle_msg_count()

        for tx in self.block.transactions:
            self.transaction = tx
            self.process_transaction()


def transactions_worker_head(consumer_group=settings.CONSUMER_GROUP):
    with session_factory() as session:
        kafka = TransactionsWorker(
            s3_client=get_s3_client(),
            session=session,
            topic=settings.CONSUMER_TOPIC_BLOCKS,
            consumer_group=consumer_group + "-head",
            auto_offset_reset=settings.CONSUMER_AUTO_OFFSET_RESET,
        )
        kafka.start()


def transactions_worker_tail(consumer_group, partition_dict):
    with session_factory() as session:
        kafka = TransactionsWorker(
            partition_dict=partition_dict,
            s3_client=get_s3_client(),
            session=session,
            topic=settings.CONSUMER_TOPIC_BLOCKS,
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
        )
        kafka.start()
