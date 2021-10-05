import json
import uuid

from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
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
        contract.contract_type = "IRC2_Token"
        contract.owner_address = t["holderAddr"]

        session.add(contract)
        session.commit()

        kafka.produce(
            settings.PRODUCER_TOPIC_TOKENS, t["contractAddr"], json.dumps(contract.dict())
        )


if __name__ == "__main__":
    init_db()
