import json
from typing import Optional

import requests

from icon_contracts.config import settings
from icon_contracts.log import logger


class JsonRpcException(Exception):
    def __init__(self, payload: dict, error: dict):
        self.message = (
            f"Error calling method=`{payload['method']}` with "
            f"params=`{payload['params']}` \n"
            f"Response Error={error}"
        )
        super().__init__(self.message)


def post_rpc(payload: dict) -> Optional[dict]:
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


def icx_getBalance(address: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getBalance",
        "id": 1234,
        "params": {"address": address},
    }
    return post_rpc(payload)


def getBonderList(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getBonderList",
                "params": {
                    "address": address,
                },
            },
        },
    }
    return post_rpc(payload)


def getBond(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getBond",
                "params": {
                    "address": address,
                },
            },
        },
    }
    return post_rpc(payload)


def getScoreStatus(address: str):
    payload = {
        "id": 1001,
        "jsonrpc": "2.0",
        "method": "icx_getScoreStatus",
        "params": {"address": address},
    }
    return post_rpc(payload)


def getTrace(tx_hash: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "debug_getTrace",
        "params": {
            "txHash": tx_hash,
        },
    }
    r = requests.post(settings.ICON_NODE_URL + "d", data=json.dumps(payload))
    if r.status_code != 200:
        r = requests.post(settings.BACKUP_ICON_NODE_URL + "d", data=json.dumps(payload))
    return r


def getTransactionByHash(hash: str):
    payload = {
        "id": 1001,
        "jsonrpc": "2.0",
        "method": "icx_getTransactionByHash",
        "params": {"txHash": hash},
    }
    return post_rpc(payload)


# if __name__ == "__main__":
#     x = icx_getBalance("hxb86afed8db896012664b0fa6c874fe0e3001edaf").json()
#     x = getBonderList("hx0b047c751658f7ce1b2595da34d57a0e7dad357d").json()
#     x = getBond("hx0b047c751658f7ce1b2595da34d57a0e7dad357d").json()
#     x = icx_getBlockByHeight().json()
#     print(x)
