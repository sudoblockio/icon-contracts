from typing import TYPE_CHECKING, List

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.utils.rpc import icx_call, icx_getScoreApi

if TYPE_CHECKING:
    from icon_contracts.models.contracts import Contract

IRC2_METHODS = [
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
    },
    {
        "name": "symbol",
        "type": "function",
        "inputs": [],
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
    },
    {
        "name": "transfer",
        "type": "function",
        "inputs": [
            {"name": "_to", "type": "Address"},
            {"name": "_value", "type": "int"},
            {"name": "_data", "default": None, "type": "bytes"},
        ],
        "outputs": [],
    },
    {
        "name": "Mint",
        "type": "eventlog",
        "inputs": [
            {"name": "account", "type": "Address", "indexed": "0x1"},
            {"name": "amount", "type": "int"},
            {"name": "_data", "type": "bytes"},
        ],
    },
    {
        "name": "Transfer",
        "type": "eventlog",
        "inputs": [
            {"name": "_from", "type": "Address", "indexed": "0x1"},
            {"name": "_to", "type": "Address", "indexed": "0x1"},
            {"name": "_value", "type": "int", "indexed": "0x1"},
            {"name": "_data", "type": "bytes"},
        ],
    },
]


def is_irc2(abi: List[dict], address: str) -> bool:
    try:
        abi_methods = [m["name"] for m in abi]
    except TypeError:
        # We are missing ABIs for some approved contracts
        return False
    for i in IRC2_METHODS:
        if i["name"] not in abi_methods:
            # Method does not exist in the token standard
            return False

        schema = [m for m in abi if m["name"] == i["name"]][0]
        if i != schema:
            # Make sure the method schema matches the IRC2 standard
            logger.info(
                f"Contract address = {address} has a method {i['name']} "
                f"that is in the irc2 spec but the schema does not match."
            )
            return False

    return True
