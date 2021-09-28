import json

import requests

from icon_contracts.config import settings


def post_rpc(payload: dict):
    r = requests.post(settings.icon_node_url, data=json.dumps(payload)).json()
    return r


def icx_getTransactionResult(txHash: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getTransactionResult",
        "id": 1234,
        "params": {"txHash": txHash},
    }
    return post_rpc(payload)


if __name__ == "__main__":
    x = icx_getTransactionResult(
        "0x62a06d97e8affa3472d999242cf264effeaabd9744c314b987c6e345a43971d7"
    )
    # x = icx_getTransactionResult('0x0e7bdd95c8a98df06564895f483863f91be6440da303cec6527a3b1b23e7a14b')
    # x = icx_getTransactionResult('0x59e47c05ed0ba2b139096b7bc6db8be3985246f8a2b34c7c24fa4d6667a6df06')
    # x = icx_getTransactionResult('0x886d1f27116bdead7f6e90be626c899cc23497d3266ab428e06793696d34afec')
    print()
