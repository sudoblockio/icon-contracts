import pytest

from icon_contracts.config import settings
from icon_contracts.utils.rpc import icx_call, icx_getScoreApi, icx_getTransactionResult

AUDIT_TX_HASHES = [
    # "0x85fff93f669f778254d8a4e484683ccb457b0e0c0d6ec61e410401c13bb0c162",
    "0x00fe47fbdb47603e7637dad21f952bb6a144c8a21fd0ced93a56e489ad8dca97",
]


@pytest.mark.parametrize("hash", AUDIT_TX_HASHES)
def test_icx_getTransactionResult_audit(hash):
    result = icx_getTransactionResult(hash).json()["result"]
    assert isinstance(result, dict)
    assert result["to"] == settings.one_address
    # assert "txHash" in result


CREATION_TX_HASHES = [
    # "0x0a6ac5576d837b7c368023cd6b33ddf17755171a5205a22b266f466aa1b1f2c2",
    "0xaeef4b72cae142dac5720fa81a7d167488bd62afde53ea4c4105c049dfe7ffd4",  # Berlin
]


@pytest.mark.parametrize("hash", CREATION_TX_HASHES)
def test_icx_getTransactionResult_creation(hash):

    settings.ICON_NODE_URL = "https://api.berlin.icon.community/api/v3"

    result = icx_getTransactionResult(hash).json()
    assert isinstance(result, dict)
    # assert "txHash" in result


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
    out = icx_getScoreApi("cx63ed3c0cb33307f5477b4f014553df3cf511544c")

    t = out.json()
    # assert out.status_code == 400
    out = icx_getScoreApi("cx221cad4d4a88f03f24457c82209d66160275ed4b")
    assert out.status_code == 200
    assert isinstance(out.json()["result"], list)
    t = out.json()

    print()


def test_icx_call():
    result = icx_call("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", {"method": "name"}).json()[
        "result"
    ]
    assert result == "Balance Token"


# def test_icx_call_sejong_issues():
#     from icon_contracts.config import settings
#     # settings.ICON_NODE_URL = "https://api.sejong.icon.community/api/v3"
#     # settings.ICON_NODE_URL = "http://108.61.103.8:9010/api/v3"
#     # settings.ICON_NODE_URL = "https://sejong.net.solidwallet.io/api/v3"
#     # settings.BACKUP_ICON_NODE_URL = settings.ICON_NODE_URL
#     settings.ICON_NODE_URL = "https://api.icon.community/api/v3"
#
#     score_api = icx_getScoreApi("cx79a1d066c9bab28090d9fc621a8212ca681a3553").json()
#     assert score_api
#
#     # # settings.ICON_NODE_URL = "https://api.sejong.icon.community/api/v3"
#     # settings.ICON_NODE_URL = "https://sejong.net.solidwallet.io/api/v3"
#     # settings.BACKUP_ICON_NODE_URL = settings.ICON_NODE_URL
#     #
#     # score_api = icx_getScoreApi("cx79a1d066c9bab28090d9fc621a8212ca681a3553").json()
#     # assert score_api
#
#     call = icx_call("cx79a1d066c9bab28090d9fc621a8212ca681a3553", {"method": "name"}).json()
#     assert call
#
#     # result = icx_call("cx79a1d066c9bab28090d9fc621a8212ca681a3553", {"method": "name"}).json()[
#     #     "result"
#     # ]
#     # assert result
#
#
# # def test_icx_call_contract_verfication():
# #     result = icx_call("cx8a0e64b6b5a84b3f65a9ca12b1e14fe4667ea80b", {"method": "version"}).json()[
# #         "result"
# #     ]
# #     # assert isinstance(result, list)
# #     # assert len(result) > 3
# #     assert result == "Balance Token"
