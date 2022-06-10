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
        "name": "totalSupply",
        "type": "function",
        "inputs": [],
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "_owner", "type": "Address"}],
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
    },
    # {
    #     "name": "Mint",
    #     "type": "eventlog",
    #     "inputs": [
    #         {"name": "account", "type": "Address", "indexed": "0x1"},
    #         {"name": "amount", "type": "int"},
    #         {"name": "_data", "type": "bytes"},
    #     ],
    # },
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

IRC31_METHODS = [
    {
        "name": "ApprovalForAll",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_owner",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_operator",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_approved",
                "type": "bool"
            }
        ]
    },
    {
        "name": "TransferBatch",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_operator",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_from",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_to",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_ids",
                "type": "bytes"
            },
            {
                "name": "_values",
                "type": "bytes"
            }
        ]
    },
    {
        "name": "TransferSingle",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_operator",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_from",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_to",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_id",
                "type": "int"
            },
            {
                "name": "_value",
                "type": "int"
            }
        ]
    },
    {
        "name": "URI",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_id",
                "type": "int",
                "indexed": "0x1"
            },
            {
                "name": "_value",
                "type": "str"
            }
        ]
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [
            {
                "name": "_owner",
                "type": "Address"
            },
            {
                "name": "_id",
                "type": "int"
            }
        ],
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "balanceOfBatch",
        "type": "function",
        "inputs": [
            {
                "name": "_owners",
                "type": "[]Address"
            },
            {
                "name": "_ids",
                "type": "[]int"
            }
        ],
        "outputs": [
            {
                "type": "list"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "isApprovedForAll",
        "type": "function",
        "inputs": [
            {
                "name": "_owner",
                "type": "Address"
            },
            {
                "name": "_operator",
                "type": "Address"
            }
        ],
        "outputs": [
            {
                "type": "bool"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "setApprovalForAll",
        "type": "function",
        "inputs": [
            {
                "name": "_operator",
                "type": "Address"
            },
            {
                "name": "_approved",
                "type": "bool"
            }
        ],
        "outputs": []
    },
    {
        "name": "tokenURI",
        "type": "function",
        "inputs": [
            {
                "name": "_id",
                "type": "int"
            }
        ],
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "transferFrom",
        "type": "function",
        "inputs": [
            {
                "name": "_from",
                "type": "Address"
            },
            {
                "name": "_to",
                "type": "Address"
            },
            {
                "name": "_id",
                "type": "int"
            },
            {
                "name": "_value",
                "type": "int"
            },
            {
                "name": "_data",
                "default": null,
                "type": "bytes"
            }
        ],
        "outputs": []
    },
    {
        "name": "transferFromBatch",
        "type": "function",
        "inputs": [
            {
                "name": "_from",
                "type": "Address"
            },
            {
                "name": "_to",
                "type": "Address"
            },
            {
                "name": "_ids",
                "type": "[]int"
            },
            {
                "name": "_values",
                "type": "[]int"
            },
            {
                "name": "_data",
                "default": null,
                "type": "bytes"
            }
        ],
        "outputs": []
    }
]

IRC3_MEHTHODS = [
    {
        "name": "Approval",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_owner",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_approved",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_tokenId",
                "type": "int",
                "indexed": "0x1"
            }
        ]
    },
    {
        "name": "Transfer",
        "type": "eventlog",
        "inputs": [
            {
                "name": "_from",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_to",
                "type": "Address",
                "indexed": "0x1"
            },
            {
                "name": "_tokenId",
                "type": "int",
                "indexed": "0x1"
            }
        ]
    },
    {
        "name": "approve",
        "type": "function",
        "inputs": [
            {
                "name": "_to",
                "type": "Address"
            },
            {
                "name": "_tokenId",
                "type": "int"
            }
        ],
        "outputs": []
    },
    {
        "name": "getApproved",
        "type": "function",
        "inputs": [
            {
                "name": "_tokenId",
                "type": "int"
            }
        ],
        "outputs": [
            {
                "type": "Address"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [
            {
                "name": "_owner",
                "type": "Address"
            }
        ],
        "outputs": [
            {
                "type": "int"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "ownerOf",
        "type": "function",
        "inputs": [
            {
                "name": "_tokenId",
                "type": "int"
            }
        ],
        "outputs": [
            {
                "type": "Address"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "symbol",
        "type": "function",
        "inputs": [],
        "outputs": [
            {
                "type": "str"
            }
        ],
        "readonly": "0x1"
    },
    {
        "name": "transfer",
        "type": "function",
        "inputs": [
            {
                "name": "_to",
                "type": "Address"
            },
            {
                "name": "_tokenId",
                "type": "int"
            }
        ],
        "outputs": []
    },
    {
        "name": "transferFrom",
        "type": "function",
        "inputs": [
            {
                "name": "_from",
                "type": "Address"
            },
            {
                "name": "_to",
                "type": "Address"
            },
            {
                "name": "_tokenId",
                "type": "int"
            }
        ],
        "outputs": []
    }
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
