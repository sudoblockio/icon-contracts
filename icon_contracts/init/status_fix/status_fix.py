import json

import requests
from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.workers.db import engine
from icon_contracts.workers.kafka import Worker


def get_old_tracker_contracts() -> list:
    """
    There is a bug with a ~100 contracts where the status shows rejected. This is
    grabbing the old status's and then later we need to update the DB and emit messages
    to kafka for the addresses service to update it's records.
    """
    contracts = []
    for i in range(0, 11):
        url = f"https://tracker.icon.foundation/v3/contract/list?page={i}&count=100"
        r = requests.get(url)
        if r.status_code == 200:
            response = r.json()["data"]
            contracts = contracts + response
        else:
            print(f"Ending at iteration {i}.")
            break

    # with open('old-contracts.json', 'w') as f:
    #     json.dump(contracts, f)

    return contracts


def fix_db():
    old_contracts = get_old_tracker_contracts()

    # with open("old-contracts.json") as f:
    #     old_contracts = json.load(f)

    kafka = Worker()

    # PG
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    for c in old_contracts:

        if c["status"] == "1":
            status = "Accepted"
        else:
            status = "Rejected"

        contract = session.get(Contract, c["address"])
        if contract is None:
            print(f"Contract {c['address']} not found ")
            continue

        contract.status = status

        session.add(contract)
        session.commit()

        # contract = Contract()
        # contract.address = "foo"
        # contract.name = "foo"
        # contract.is_token = False

        kafka.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            contract.address,  # Keyed on hash
            # Convert the pydantic object to proto
            contract_to_proto(contract),
        )


if __name__ == "__main__":
    fix_db()
