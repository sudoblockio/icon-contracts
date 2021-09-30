from icon_contracts.utils.rpc import icx_getScoreApi


def test_icx_getScoreApi():
    out = icx_getScoreApi("cx63ed3c0cb33307f5477b4f014553df3cf511544c")
    assert out.status_code == 400
    out = icx_getScoreApi("cx9ab3078e72c8d9017194d17b34b1a47b661945ca")
    assert out.status_code == 200
    assert isinstance(out.json()["result"], list)
