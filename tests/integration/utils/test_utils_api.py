import pytest

from icon_contracts.utils.api import get_first_tx

FIRST_TXS = [
    ["cx9ab3078e72c8d9017194d17b34b1a47b661945ca", 1564592023695863],
    ["cxbdcc8e15406998d99c4927fecfde99f7c1404358", 1667118795967960],
    # Contract with 4M records timesout with count
    ["cx502c47463314f01e84b1b203c315180501eb2481", None],
]


# @pytest.mark.parametrize("address,first_tx", FIRST_TXS)
# def test_get_first_tx(address: str, first_tx: int):
#     result = get_first_tx(address=address)
#
#     assert result == first_tx
