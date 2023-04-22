import pytest

from icon_contracts.models.contracts import Contract


def test_extract_contract_details_creation():
    contract = Contract(address="cx3be2043b46ef12f8653dfda01225253b708f1cd9")
    contract.creation_hash = "0x780589bd21ea5af76b6a46a08cc8acdf63bae2af0aa6daa0af839f6ab3aa4e6b"
    contract.extract_contract_details()

    assert contract.created_block


CONTRACT_CLASSIFICATIONS = [
    "cxb0b6f777fba13d62961ad8ce11be7ef6c4b2bcc6",
]


@pytest.mark.parametrize("address", CONTRACT_CLASSIFICATIONS)
def test_classify_contract_contract(address):
    """Non-tokens."""
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.contract_type


TOKEN_CLASSIFICATIONS_IRC2 = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", "BALN"),
    ("cx0bb718a35e7fc8faffe6faf82b32f6f7cb5e7c81", "CHIU"),
    ("cx82e9075445764ef32f772d11f5cb08dae71d463b", "ITD"),
]


@pytest.mark.parametrize("address,symbol", TOKEN_CLASSIFICATIONS_IRC2)
def test_classify_contract_irc2(address, symbol):
    contract = Contract()
    contract.address = address
    contract.extract_contract_details()
    assert contract.symbol == symbol
    assert contract.token_standard == "irc2"
    assert contract.is_token


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
    # "cx30f18d26f45d990112a4cd4825c0b79af73aac7c",  # Missing "name" method
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
