import pytest

from icon_contracts.models.contracts import Contract

TOKEN_CLASSIFICATIONS_IRC2 = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", "BALN"),
    ("cx0bb718a35e7fc8faffe6faf82b32f6f7cb5e7c81", "CHIU"),
]


@pytest.mark.parametrize("address,symbol", TOKEN_CLASSIFICATIONS_IRC2)
def test_classify_contract_irc2(address, symbol):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.symbol == symbol
    assert contract.token_standard == "irc2"


CONTRACT_CLASSIFICATIONS = ["cxb799844c58d5e5afb08ad4078566a78bd82d932c"]


@pytest.mark.parametrize("address", CONTRACT_CLASSIFICATIONS)
def test_classify_contract_contract(address):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.contract_type == "Contract"


IRC3_CONTRACTS = [
    "cx57d7acf8b5114b787ecdd99ca460c2272e4d9135",
    "cx943cf4a4e4e281d82b15ae0564bbdcbf8114b3ec",
]


@pytest.mark.parametrize("address", IRC3_CONTRACTS)
def test_classify_contract_irc3(address):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.token_standard == "irc3"


IRC31_CONTRACTS = [
    "cx30f18d26f45d990112a4cd4825c0b79af73aac7c",
    "cx384018e03aa8b739472c7a0645b70df97550e2c2",
    "cx45cf0c108c3df650b1c28d9e2fdc8b4d068cb2fa",
    "cx5f1cc357f2304fb2646e20211adbe137ab5852dd",
    "cx7fc67030a7eb46aa176a15267b600d48e11ef44b",
    "cx8e51beac285e664d74d457bb8fbbbb693bf1b97d",
]


@pytest.mark.parametrize("address", IRC31_CONTRACTS)
def test_classify_contract_irc31(address):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.token_standard == "irc31"
