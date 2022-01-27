from icon_contracts.utils.rpc import icx_call, icx_getScoreApi, icx_getTransactionResult

# def test_icx_getTransactionResult():
#     result = icx_getTransactionResult(
#         "0xdac72f387487f31c5e158aa592952e3b9933f925126ede3eaa52d9c6a7d598c0"
#     ).json()
#     assert isinstance(result, dict)
#     assert "txHash" in result


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
    # assert isinstance(result, list)
    # assert len(result) > 3
    assert result == "Balance Token"


# def test_icx_call_contract_verfication():
#     result = icx_call("cx8a0e64b6b5a84b3f65a9ca12b1e14fe4667ea80b", {"method": "version"}).json()[
#         "result"
#     ]
#     # assert isinstance(result, list)
#     # assert len(result) > 3
#     assert result == "Balance Token"
