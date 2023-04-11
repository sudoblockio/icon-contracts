import pytest

from icon_contracts.config import settings
from icon_contracts.utils.rpc import (
    getScoreStatus,
    icx_call,
    icx_getScoreApi,
    icx_getTransactionResult,
)

AUDIT_TX_HASHES = [
    "0x85fff93f669f778254d8a4e484683ccb457b0e0c0d6ec61e410401c13bb0c162",
    "0x00fe47fbdb47603e7637dad21f952bb6a144c8a21fd0ced93a56e489ad8dca97",
]


@pytest.mark.parametrize("hash", AUDIT_TX_HASHES)
def test_icx_getTransactionResult_audit(hash):
    result = icx_getTransactionResult(hash).json()["result"]
    assert isinstance(result, dict)
    assert result["to"] == settings.one_address


CREATION_TX_HASHES = [
    "0x0a6ac5576d837b7c368023cd6b33ddf17755171a5205a22b266f466aa1b1f2c2",
]


@pytest.mark.parametrize("hash", CREATION_TX_HASHES)
def test_icx_getTransactionResult_creation(hash):
    result = icx_getTransactionResult(hash).json()
    assert isinstance(result, dict)


TX_HASHES = [
    "0x325b2652e539f47ccd9849ab2eeba3379bc42a44be16f0ef5767dfc7c88152a1",
]


@pytest.mark.parametrize("hash", TX_HASHES)
def test_icx_getTransactionResult(hash):
    result = icx_getTransactionResult(hash).json()["result"]
    assert isinstance(result, dict)
    assert "txHash" in result


def test_icx_getScoreApi():
    result = icx_getScoreApi("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619").json()["result"]
    assert isinstance(result, list)
    assert len(result) > 3

    out = icx_getScoreApi("cx221cad4d4a88f03f24457c82209d66160275ed4b")
    assert out.status_code == 200
    assert isinstance(out.json()["result"], list)


def test_icx_call():
    result = icx_call("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", {"method": "name"}).json()[
        "result"
    ]
    assert result == "Balance Token"


def test_getScoreStatus():
    # address = "cxbdcc8e15406998d99c4927fecfde99f7c1404358"  # btp internal contract
    address = "cxba7a8271d85ed673d27574a30e3261e147902e92"
    result = getScoreStatus(address).json()["result"]
    assert result == "Balance Token"
