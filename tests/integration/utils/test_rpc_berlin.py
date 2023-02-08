import pytest

from icon_contracts.config import settings
from icon_contracts.utils import rpc

# settings.ICON_NODE_URL = "https://api.berlin.icon.community/api/v3"

CREATION_TX_HASHES = [
    "0x0a6ac5576d837b7c368023cd6b33ddf17755171a5205a22b266f466aa1b1f2c2",
    # "0xaeef4b72cae142dac5720fa81a7d167488bd62afde53ea4c4105c049dfe7ffd4",  # Berlin
]


@pytest.mark.parametrize("hash", CREATION_TX_HASHES)
def test_icx_getTransactionResult_creation(hash):

    result = rpc.icx_getTransactionResult(hash).json()
    assert isinstance(result, dict)
    # assert "txHash" in result


def test_icx_getScoreApi():
    result = rpc.icx_getScoreApi("cxcc254b11e1b14779b347ec7f392ea465c6e22b5b").json()["result"]

    assert isinstance(result, list)
    assert len(result) > 3


def test_getTrace():
    result = rpc.getTrace(
        "0xaeef4b72cae142dac5720fa81a7d167488bd62afde53ea4c4105c049dfe7ffd4"
    ).json()["result"]

    assert isinstance(result, list)
    assert len(result) > 3
