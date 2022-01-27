import pytest

from icon_contracts.models.contracts import Contract

TOKEN_CLASSIFICATIONS = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", "BALN"),
    ("cx0bb718a35e7fc8faffe6faf82b32f6f7cb5e7c81", "CHIU"),
]


@pytest.mark.parametrize("address,symbol", TOKEN_CLASSIFICATIONS)
def test_classify_contract(address, symbol):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.symbol == symbol
    assert contract.contract_type != "Contract"


CONTRACT_CLASSIFICATIONS = ["cxb799844c58d5e5afb08ad4078566a78bd82d932c"]


@pytest.mark.parametrize("address", CONTRACT_CLASSIFICATIONS)
def test_classify_contract(address):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.contract_type == "Contract"
