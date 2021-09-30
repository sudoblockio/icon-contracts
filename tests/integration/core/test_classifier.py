import pytest

from icon_contracts.models.contracts import Contract

CONTRACT_CLASSIFICATIONS = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", "BALN"),
    ("cx0bb718a35e7fc8faffe6faf82b32f6f7cb5e7c81", "CHIU"),
]


@pytest.mark.parametrize("address,symbol", CONTRACT_CLASSIFICATIONS)
def test_classify_contract(address, symbol):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.symbol == symbol
    assert contract.contract_type != "Contract"
