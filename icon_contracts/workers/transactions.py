import json
import os
import shutil
from typing import Any

from google.protobuf.json_format import MessageToJson
from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.metrics import Metrics
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.utils.contract_content import (
    get_contract_name,
    get_s3_client,
    upload_to_s3,
    zip_content_to_dir,
)
from icon_contracts.utils.rpc import icx_call, icx_getTransactionResult
from icon_contracts.workers.db import engine, session_factory
from icon_contracts.workers.kafka import Worker

metrics = Metrics()


class TransactionsWorker(Worker):
    # Need to pipe this in due to bug in boto
    s3_client: Any = None

    partition_dict: dict = None

    # Metrics
    msg_count: int = 0
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    def java_contract(self, content, value):
        pass

    def python_contract(self, content: str, value: TransactionRaw):
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
                # status="Submitted",
            )
            # There could be a race condition here to update this record
            self.session.merge(contract)
            self.session.commit()
            # try:
            #     self.session.commit()
            #     self.session.refresh(contract)
            # except:
            #     self.session.rollback()
            #     raise

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

        # Condition where we have already updated the record
        if (
            value.block_number < contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(
                f"Updating contract creation for address = {address} at block = {value.block_number}"
            )
            contract.created_block = value.block_number
            contract.created_timestamp = timestamp

        # Method that classifies the contract based on ABI for IRC2 stuff
        contract.extract_contract_details()

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
        # try:
        #     self.session.commit()
        #     self.session.refresh(contract)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.close()

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

        # Audit related events
        if data["method"] in ["acceptScore", "rejectScore"]:
            address = icx_getTransactionResult(data["params"]["txHash"]).json()["result"][
                "scoreAddress"
            ]

            # Make the status the address in case there is some funky situation
            # we don't know about -> proxy for dead letter queue
            status = address
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
                    # last_updated_timestamp=timestamp, # Out on purpose for subsequent logic
                    # created_block=value.block_number,
                    # created_timestamp=int(value.timestamp, 16),
                )
            else:
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

    def process(self, msg):

        value = msg.value()

        if value.to_address == "None":
            return

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

        # Pass on any invalid Tx in this service
        if value.receipt_status != 1:
            return

        # Handle audit process
        if value.to_address == settings.one_address:
            self.process_audit(value)

        # if value.to_address == settings.governance_address:
        if value.data.startswith('{"contentType": "application/'):
            data = json.loads(value.data)

            if data["contentType"] == "application/zip":
                logger.info(f"Handling python contract creation hash {value.hash}.")
                self.python_contract(data["content"], value)

            if data["contentType"] == "application/java":
                logger.info(f"Handling java contract creation hash {value.hash}.")
                self.java_contract(data["content"], value)

            return

        # if method in 'addAuditor':
        #     print()
        #
        # if method in 'removeAuditor':
        #     print()


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
