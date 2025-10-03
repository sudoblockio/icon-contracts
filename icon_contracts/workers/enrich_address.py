
from icon_contracts.models.contracts import Contract


def enrich_contract(address: str):
    contract = self.session.get(Contract, address)

    contract = Contract(address=address)

