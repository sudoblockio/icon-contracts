import json
import os
import shutil
import subprocess
import zipfile
from typing import Any

from google.protobuf.json_format import MessageToJson

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.metrics import Metrics
from icon_contracts.models.contracts import Contract
from icon_contracts.models.social_media import SocialMedia
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.utils.contract_content import (
    get_contract_name,
    get_s3_client,
    upload_to_s3,
    zip_content_to_dir,
)
from icon_contracts.utils.rpc import icx_getTransactionResult
from icon_contracts.workers.db import session_factory
from icon_contracts.workers.kafka import Worker
from icon_contracts.workers.verification import (
    compare_source,
    get_on_chain_contract_src,
    replace_build_tool,
)

metrics = Metrics()


CONTRACT_VERIFICATION_CONTRACTS = {
    "cx84c88b975f60aeff9ee534b5efdb69d66d239596",  # Berlin
    "cx338322697c252ec776bf81157f55e1f47beb7d78",  # Lisbon
}


class TransactionsWorker(Worker):
    # Need to pipe this in due to bug in boto
    s3_client: Any = None

    partition_dict: dict = None

    # Metrics
    msg_count: int = 0
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    def process_contract(self, content: str, value: TransactionRaw):
        """
        Process the contract by checking its status in the DB and uploading the
        source to S3 and including a download link in the DB.
        """
        tx_result = icx_getTransactionResult(value.hash).json()["result"]

        address = tx_result["scoreAddress"]
        timestamp = int(value.timestamp, 16)

        # Check if there is a contract in the DB with that address otherwise create it
        contract = self.session.get(Contract, address)

        if contract is None:
            # In order process
            logger.info(
                f"Creating new contract address = {address} at block = {value.block_number}"
            )
            contract = Contract(
                address=address,
                name=get_contract_name(address),
                owner_address=value.from_address,
                last_updated_block=value.block_number,
                # last_updated_timestamp=timestamp, # Out on purpose for subsequent logic
                created_block=value.block_number,
                created_timestamp=timestamp,
                creation_hash=value.hash,
            )
            self.session.merge(contract)
            self.session.commit()

        # Out of order processes
        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            value.block_number > contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(f"Updating contract address = {address} at block = {value.block_number}")
            self.contracts_updated_python += 1
            metrics.contracts_created_python.set(self.contracts_updated_python)

            # If we have access credentials this is not None
            if self.s3_client:

                # Increment the revision number
                contract.revision_number = +1
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

            contract.name = get_contract_name(contract.address)
            contract.last_updated_block = value.block_number
            contract.last_updated_timestamp = timestamp

            # Method that classifies the contract based on ABI for IRC2 stuff
            contract.extract_contract_details()

        # Condition where we have already updated the record
        if (
            value.block_number <= contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(
                f"Updating contract creation for address = {address} at block = {value.block_number}"
            )
            contract.created_block = value.block_number
            contract.created_timestamp = timestamp
            contract.creation_hash = value.hash

        # Produce the record so adjacent services can find out about new contracts as
        # this is the only service that actually inspects the ABI and classifies the
        # contracts.  So far only (10/21) `icon-addresses` is using this topic.
        self.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            value.hash,  # Keyed on hash
            # Convert the pydantic object to proto
            contract_to_proto(contract),
        )

        # Commit the contract
        self.session.merge(contract)
        self.session.commit()

    def process_audit(self, value: TransactionRaw):
        data = json.loads(value.data)

        # Contract creation events
        if "contentType" in data:
            logger.info(f"Unknown event for with hash = {value.hash}")
            # No idea what is going on here.
            self.produce_json(
                topic=settings.PRODUCER_TOPIC_DLQ,
                key="unknown-event-content-type",
                value=MessageToJson(value),
            )
            self.json_producer.poll(0)
            return

        if "method" not in data:
            logger.info(f"No method found in audit hash {value.hash}")
            return

        if data["method"] not in ["acceptScore", "rejectScore"]:
            logger.info(f"Method not supported in audit hash {value.hash}")
            return

        # # Audit related events
        address = icx_getTransactionResult(data["params"]["txHash"]).json()["result"][
            "scoreAddress"
        ]

        status = None
        if data["method"] == "acceptScore":
            status = "Accepted"
        elif data["method"] == "rejectScore":
            status = "Rejected"

        contract = self.session.get(Contract, address)

        if contract is None:
            logger.info(
                f"Creating contract from approval for address = {address} at block = {value.block_number}"
            )
            self.contracts_created_python += 1
            metrics.contracts_created_python.set(self.contracts_created_python)
            contract = Contract(
                address=address,
                name=get_contract_name(address),
                status=status,
                owner_address=value.from_address,
                # We deal with update dates based on submission due to 2.0 dropping audit
                last_updated_block=0,
            )

        # Out of order processes
        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            value.block_number > contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(
                f"Updating contract status from approval for address = {address} at block = {value.block_number}"
            )
            self.contracts_updated_python += 1
            metrics.contracts_created_python.set(self.contracts_updated_python)

            contract.status = status

        self.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            value.hash,  # Keyed on hash
            contract_to_proto(contract),
        )

        self.session.merge(contract)
        self.session.commit()

    def process_verification_social_media(self, params: dict):
        """Process social media contacts for verifiction txs."""

        social_media = self.session.get(SocialMedia, params["contract_address"])
        if social_media is None:
            social_media = SocialMedia(**params)

        ignore_fields = ["source_code_location", "zipped_source_code"]
        for k, v in params.items():
            if k in ignore_fields:
                continue

            setattr(social_media, k, v)

        self.session.merge(social_media)
        self.session.commit()

    def process_verification(self, value):
        """
        Process contract verifications. Only runs txs to the contract verification
        contract which adheres to a schema that we can control.

        Runs the following steps:
        1. Validates that the sender of the Tx is the owner of the contract
        2. Unzips the bytestring of the contract to `verified_source_code/`
            a. Remove any `build/` directories so to make it impossible for someone
            to provide a pre-built binary that is not what we are verifying
            b. Run gradelew Optimizedjar on it to produce the
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

        data = json.loads(value.data)

        if "method" not in data or "params" not in data:
            return

        if data["method"] != "verify":
            return

        params = data["params"]

        # Verify that the sender is the owner address for the contract
        contract = self.session.get(Contract, params["contract_address"])
        if contract is None:
            logger.info(
                f'Contract verification Tx to {params["contract_address"]} not found with Tx hash {value.hash}'
            )
            return

        if contract.owner_address != value.from_address:
            logger.info(
                f'Contract verification Tx from {value.from_address} to {params["contract_address"]} not from owner with Tx hash {value.hash}'
            )
            return

        self.process_verification_social_media(params)

        # Verify that the source code is the same as what is on-chain
        contract_path = None
        try:
            # Unzip the source code
            zip_name = "verified_source_code"
            # Unzip the contents of the dict to a directory
            contract_path = zip_content_to_dir(params["zipped_source_code"], zip_name)

            # chdir to /tmp/tmp<random>/
            tmp_path = os.path.dirname(contract_path)
            os.chdir(tmp_path)

            with zipfile.ZipFile(contract_path, "r") as zip_ref:
                zip_ref.extractall(zip_name)

            # Paths
            source_code_head_dir = params["source_code_location"].split("/")[0]
            verified_contract_path = os.path.join(tmp_path, zip_name, source_code_head_dir)

            # Use an official gradlew builder and wrapper
            replace_build_tool(verified_contract_path)
            subprocess.run([os.path.join(verified_contract_path, "gradlew"), "optimizedJar"])

            # Find binary
            binary_path = os.path.join(tmp_path, zip_name, params["source_code_location"])
            if not os.path.exists(binary_path):
                logger.info(f"Binary not found in {binary_path} for {value.hash}")
                return

            # Unzip the optimized jar so that we can inspect each file
            with zipfile.ZipFile(binary_path, "r") as zip_ref:
                zip_ref.extractall("verified_jar/")

            # Downloads the on chain zipped binaries
            on_chain_src_dir = get_on_chain_contract_src(contract.source_code_link)

            # Compare binary to what is on-chain
            compare_source(on_chain_src_dir, "verified_jar")
            logger.info(f"Successfully compared {value.hash}")

            # Get the optimized jar file name
            link = f"https://{settings.CONTRACTS_S3_BUCKET}.s3.us-west-2.amazonaws.com/verified-contract-sources/{params['contract_address']}.zip"

            upload_to_s3(
                self.s3_client,
                contract_path,
                params["contract_address"] + ".zip",
                prefix="verified-contract-sources",
            )

            contract.verified_source_code_link = link
            contract.verified = True
            self.session.merge(contract)
            self.session.commit()

            # Cleanup
            shutil.rmtree(tmp_path)
            logger.info(f"Uploaded contract to {contract.source_code_link}")
        except Exception as e:
            logger.info(f"Unable verify contract - {value.hash} - {e}")
            if os.path.exists(contract_path):
                shutil.rmtree(os.path.dirname(contract_path))

    def handle_msg_count(self, msg=None, value=None):
        # Logic that handles backfills so that they do not continue to consume records
        # past the offset that the job was set off at.
        if self.partition_dict is not None:
            if self.msg_count % 1000 == 0:
                end_offset = self.partition_dict[(self.topic, msg.partition())]
                offset = [
                    i.offset
                    for i in self.get_offset_per_partition()
                    if i.partition == msg.partition() and i.topic == self.topic
                ][0]

                logger.info(f"offset={offset} and end={end_offset}")

                if offset > end_offset:
                    logger.info(f"Reached end of job at offset={offset} and end={end_offset}")
                    import sys

                    logger.info("Exiting.")
                    sys.exit(0)

        if self.msg_count % 100000 == 0:
            logger.info(
                f"msg count {self.msg_count} and block {value.block_number} "
                f"for consumer group {self.consumer_group}"
            )
        self.msg_count += 1

    def process(self, msg):

        value = msg.value()

        if value.to_address == "None":
            return

        # Pass on any invalid Tx in this service
        if value.receipt_status != 1:
            return

        # Logic that handles backfills so that they do not continue to consume records
        # past the offset that the job was set off at.
        self.handle_msg_count(msg=msg, value=value)

        # Handle audit process
        if value.to_address == settings.one_address:
            self.process_audit(value)

        # Handle verification process
        if value.to_address in CONTRACT_VERIFICATION_CONTRACTS:
            self.process_verification(value)

        # Need to check the data field if there is a json payload otherwise we are not
        # interested in it in this context
        if str(value.data) != "null":
            try:
                data = json.loads(value.data)
            except Exception:
                self.produce_json(
                    topic=settings.PRODUCER_TOPIC_DLQ,
                    key="unknown-event-content-type",
                    value=MessageToJson(value),
                )
                return
        else:
            return

        if data is not None:
            # These are contract creation Txs
            if "contentType" in data:
                if data["contentType"] in ["application/zip", "application/java"]:
                    logger.info(f"Handling contract creation hash {value.hash}.")
                    self.process_contract(data["content"], value)
                return


def transactions_worker_head(consumer_group=settings.CONSUMER_GROUP):
    with session_factory() as session:
        kafka = TransactionsWorker(
            s3_client=get_s3_client(),
            session=session,
            topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
            consumer_group=consumer_group + "-head",
            auto_offset_reset="latest",
        )
        kafka.start()


def transactions_worker_tail(consumer_group, partition_dict):
    with session_factory() as session:
        kafka = TransactionsWorker(
            partition_dict=partition_dict,
            s3_client=get_s3_client(),
            session=session,
            topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
        )
        kafka.start()
