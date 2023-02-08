import pytest

from icon_contracts.utils import rpc

CREATION_TX_HASHES = [
    "0x0a6ac5576d837b7c368023cd6b33ddf17755171a5205a22b266f466aa1b1f2c2",
]


@pytest.mark.parametrize("hash", CREATION_TX_HASHES)
def test_icx_getTransactionResult_creation(hash):

    result = rpc.icx_getTransactionResult(hash).json()
    assert isinstance(result, dict)
    # assert "txHash" in result


def test_icx_getScoreApi():
    result = rpc.icx_getScoreApi("cxa1afa0580d0da7f0a40583cb2efb518d5be1d5f1").json()["result"]

    assert isinstance(result, list)
    assert len(result) > 3


def test_getTrace():
    result = rpc.getTrace(
        "0x8e621f0eeb5a15a1e513fd93cb20057b4246cd37da71987528f89ee2adbe7d9f"
    ).json()["result"]

    assert isinstance(result["logs"], list)
    assert len(result) > 1
