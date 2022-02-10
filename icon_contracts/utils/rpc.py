import json

import requests

from icon_contracts.config import settings
from icon_contracts.log import logger


def post_rpc(payload: dict):
    r = requests.post(settings.ICON_NODE_URL, data=json.dumps(payload))
    if r.status_code != 200:
        logger.info(f"Error {r.status_code} with payload {payload}")
        r = requests.post(settings.BACKUP_ICON_NODE_URL, data=json.dumps(payload))
        if r.status_code != 200:
            logger.info(f"Error {r.status_code} with payload {payload} to backup")
        return r

    return r


def icx_getTransactionResult(txHash: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "icx_getTransactionResult",
        "params": {"txHash": txHash},
    }
    return post_rpc(payload)


def icx_getScoreApi(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "icx_getScoreApi",
        "params": {"address": address},
    }
    return post_rpc(payload)


def icx_call(address: str, data: dict):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "icx_call",
        "params": {
            "to": address,
            "dataType": "call",
            "data": data,
        },
    }
    return post_rpc(payload)


def icx_getBlockByHeight():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "icx_getBlockByHeight",
        "params": {"height": "0x3"},
    }
    return post_rpc(payload)


# if __name__ == '__main__':
#     x = icx_getBlockByHeight().json()
#     print(x)
