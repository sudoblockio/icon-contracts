from icon_contracts.utils.rpc import icx_call, icx_getScoreApi, icx_getTransactionResult


def test_icx_getTransactionResult():
    result = icx_getTransactionResult(
        "0x62a06d97e8affa3472d999242cf264effeaabd9744c314b987c6e345a43971d7"
    ).json()["result"]
    assert isinstance(result, dict)
    assert "txHash" in result


def test_icx_getScoreApi():
    result = icx_getScoreApi("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619").json()["result"]
    assert isinstance(result, list)
    assert len(result) > 3
    out = icx_getScoreApi("cx63ed3c0cb33307f5477b4f014553df3cf511544c")
    assert out.status_code == 400
    out = icx_getScoreApi("cx9ab3078e72c8d9017194d17b34b1a47b661945ca")
    assert out.status_code == 200
    assert isinstance(out.json()["result"], list)


def test_icx_call():
    result = icx_call("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", {"method": "name"}).json()[
        "result"
    ]
    # assert isinstance(result, list)
    # assert len(result) > 3
    assert result == "Balance Token"
