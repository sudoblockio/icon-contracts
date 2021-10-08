import json
import uuid

from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_processed_pb2 import ContractProcessed
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.workers.db import engine
from icon_contracts.workers.kafka import Worker


def init_db():
    with open("tokens.json") as f:
        tokens = json.load(f)

    # PG
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    # Kafka - Output to topic. Other services depend on this service to
    # classify contracts as tokens. The tokens service operates off a
    # known set of contracts.
    kafka = Worker(consumer_group=str(uuid.uuid4()), topic=settings.CONSUMER_TOPIC_LOGS)

    for t in tokens["data"]:
        logger.info(f"Parsing {t['name']}")

        contract = session.get(Contract, t["contractAddr"])
        if contract is None:
            contract = Contract()

        contract.address = (t["contractAddr"],)
        contract.name = (t["name"],)
        contract.symbol = (t["symbol"],)
        contract.contract_type = "IRC2"
        contract.owner_address = t["holderAddr"]

        session.add(contract)
        session.commit()

        contract_processed = ContractProcessed(
            address=contract.address,
            owner_address=contract.owner_address,
            timestamp=0,
            block_number=0,
            name=contract.name,
            symbol=contract.symbol,
            decimals=contract.decimals,
            contract_type=contract.contract_type,
            current_version=contract.current_version,
            last_updated_block=0,
            last_updated_timestamp=0,
            created_block=0,
            created_timestamp=0,
            status="Submitted",
        )

        kafka.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            t["contractAddr"],  # Keyed on address for init - hash for Tx updates
            contract_processed,
        )


if __name__ == "__main__":
    init_db()
