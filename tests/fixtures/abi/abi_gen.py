import json

from icon_contracts.utils.rpc import icx_getScoreApi

CONTRACTS = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619", "balanced_abi.json"),
    ("cxc39d322cd9af864f0edb0bfe9635322893e07c5b", "idol_abi.json"),
]

for i in CONTRACTS:
    with open(i[1], "w") as f:
        json.dump(icx_getScoreApi(i[0]), f)
