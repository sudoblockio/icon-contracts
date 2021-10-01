import json
from uuid import uuid4

from google.protobuf.json_format import MessageToJson
from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.utils.contract_content import (
    find_and_load_package_json,
    unzip_content_to_dir,
)
from icon_contracts.utils.rpc import icx_call, icx_getTransactionResult
from icon_contracts.workers.db import engine
from icon_contracts.workers.kafka import Worker


class TransactionsWorker(Worker):
    def process_contract_creation(self):
        pass

    def java_contract(self, content, value):
        pass

    def python_contract(self, content: str, value: TransactionRaw):
        tx_result = icx_getTransactionResult(value.hash).json()["result"]

        address = tx_result["scoreAddress"]
        timestamp = int(value.timestamp, 16) / 1e6

        # Check if there is a contract in the DB with that address otherwise create it
        contract = self.session.get(Contract, address)

        if contract is None:
            # In order process
            logger.info(
                f"Creating new contract address = {address} at block = {value.block_number}"
            )
            contract = Contract(
                address=address,
                last_updated_block=value.block_number,
                last_updated_timestamp=timestamp,
                created_block=value.block_number,
                created_timestamp=timestamp,
                status="Submitted",
            )

        if settings.UNZIP_PYTHON_SOURCE_CODE:
            # Unzip the byte string content into a tmp directory
            # TODO: Determine what to do here
            #  1. Unzip it and push it to s3 - insecure
            #  2. Compile it and extract metadata - How?
            #  3. Do nothing - Super secure
            contract_path = unzip_content_to_dir(content, value.hash)
            package_json = find_and_load_package_json(contract_path)
            if package_json == NotADirectoryError:
                self.produce(
                    topic=f"{settings.name}-illegilable-input-contract-dlq",
                    key=value.hash,
                    value=MessageToJson(value),
                )
                return

        # Out of order processes
        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            value.block_number > contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(f"Updating contract address = {address} at block = {value.block_number}")
            if settings.UNZIP_PYTHON_SOURCE_CODE:
                contract.current_version = package_json["version"]  # noqa

            contract.name = icx_call(address, {"method": "name"}).json()["result"]
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

        # Commit the contract
        self.session.add(contract)
        self.session.commit()

    def process_audit(self, value: TransactionRaw):
        data = json.loads(value.data)

        # Contract creation events
        if "contentType" in data:
            logger.info(f"Unknown event for with hash = {value.hash}")
            # No idea what is going on here.
            self.produce(
                topic=f"{settings.name}-content-type-dlq",
                key=value.from_address,
                value=MessageToJson(value),
            )
            self.producer.poll(0)
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
                contract = Contract(address=address, status=status)
            else:
                logger.info(
                    f"Updating contract status from approval for address = {address} at block = {value.block_number}"
                )
                contract.status = status

            self.session.add(contract)
            self.session.commit()

    def process(self, msg):
        value = msg.value()

        # Pass on any invalid Tx in this service
        if value.receipt_status != 1:
            return

        # Messages are keyed by to_address
        if msg.key() == settings.one_address:
            self.process_audit(value)

        if msg.key() == settings._governance_address and value.receipt_status == 1:

            data = json.loads(value.data)

            if "contentType" in data:
                if data["contentType"] == "application/zip":
                    self.python_contract(data["content"], value)

                if data["contentType"] == "application/java":
                    self.java_contract(data["content"], value)

            return

        # if method in 'addAuditor':
        #     print()
        #
        # if method in 'removeAuditor':
        #     print()


def transactions_worker_head():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    kafka = TransactionsWorker(
        session=session,
        topic="transactions",
        consumer_group=settings.CONSUMER_GROUP_HEAD,
        auto_offset_reset="latest",
    )

    kafka.start()


def transactions_worker_tail():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    kafka = TransactionsWorker(
        session=session,
        topic="transactions",
        consumer_group=settings.CONSUMER_GROUP_TAIL,
        auto_offset_reset="earliest",
    )

    kafka.start()


if __name__ == "__main__":
    transactions_worker_head()
    # transactions_worker_tail()
