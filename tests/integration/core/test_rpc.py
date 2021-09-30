from icon_contracts.utils.rpc import icx_call, icx_getScoreApi, icx_getTransactionResult


def test_icx_getTransactionResult():
    result = icx_getTransactionResult(
        "0x62a06d97e8affa3472d999242cf264effeaabd9744c314b987c6e345a43971d7"
    )
    assert isinstance(result, dict)
    assert "txHash" in result


def test_icx_getScoreApi():
    result = icx_getScoreApi("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619")
    assert isinstance(result, list)
    assert len(result) > 3


def test_icx_call():
    result = icx_call("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", {"method": "name"})
    # assert isinstance(result, list)
    # assert len(result) > 3
    assert result == "Balance Token"
