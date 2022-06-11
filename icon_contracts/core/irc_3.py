# https://sejong.tracker.solidwallet.io/contract/cxd1a990d6ad986b064a9aac1474ba0cfeff64fd32


# IRC3_MEHTHODS = [
#     {
#         "name": "Approval",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_owner",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_approved",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_tokenId",
#                 "type": "int",
#                 "indexed": "0x1"
#             }
#         ]
#     },
#     {
#         "name": "Transfer",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_from",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_tokenId",
#                 "type": "int",
#                 "indexed": "0x1"
#             }
#         ]
#     },
#     {
#         "name": "approve",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_to",
#                 "type": "Address"
#             },
#             {
#                 "name": "_tokenId",
#                 "type": "int"
#             }
#         ],
#         "outputs": []
#     },
#     {
#         "name": "getApproved",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_tokenId",
#                 "type": "int"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "Address"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "name",
#         "type": "function",
#         "inputs": [],
#         "outputs": [
#             {
#                 "type": "str"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "balanceOf",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_owner",
#                 "type": "Address"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "int"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "ownerOf",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_tokenId",
#                 "type": "int"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "Address"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "symbol",
#         "type": "function",
#         "inputs": [],
#         "outputs": [
#             {
#                 "type": "str"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "transfer",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_to",
#                 "type": "Address"
#             },
#             {
#                 "name": "_tokenId",
#                 "type": "int"
#             }
#         ],
#         "outputs": []
#     },
#     {
#         "name": "transferFrom",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_from",
#                 "type": "Address"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address"
#             },
#             {
#                 "name": "_tokenId",
#                 "type": "int"
#             }
#         ],
#         "outputs": []
#     }
# ]


IRC3_METHODS = [
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_owner", "type": "Address"}],
        "name": "balanceOf",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "name": "ownerOf",
        "outputs": [{"type": "Address"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "name": "getApproved",
        "outputs": [{"type": "Address"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_to", "type": "Address"}, {"name": "_tokenId", "type": "int"}],
        "name": "approve",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_index", "type": "int"}],
        "name": "tokenByIndex",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_owner", "type": "Address"}, {"name": "_index", "type": "int"}],
        "name": "tokenOfOwnerByIndex",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_from", "type": "Address"},
            {"indexed": "0x1", "name": "_to", "type": "Address"},
            {"indexed": "0x1", "name": "_tokenId", "type": "int"},
        ],
        "name": "Transfer",
        "type": "eventlog",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_owner", "type": "Address"},
            {"indexed": "0x1", "name": "_approved", "type": "Address"},
            {"indexed": "0x1", "name": "_tokenId", "type": "int"},
        ],
        "name": "Approval",
        "type": "eventlog",
    },
    {
        "inputs": [{"name": "_gen", "type": "str"}, {"name": "_eggTokenURI", "type": "str"}],
        "name": "mint",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "user", "type": "Address"}],
        "name": "addAdmin",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "user", "type": "Address"}],
        "name": "removeAdmin",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_to", "type": "Address"}, {"name": "_tokenId", "type": "int"}],
        "name": "transfer",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_tokenId", "type": "int"},
        ],
        "name": "transferFrom",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}, {"name": "_uri", "type": "str"}],
        "name": "setTokenURI",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_mData", "type": "str"}, {"name": "_gen", "type": "str"}],
        "name": "setPossibleESInfo",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_index", "type": "int"}, {"name": "_gen", "type": "str"}],
        "name": "getPossibleEsInfoByIndex",
        "outputs": [{"type": "dict"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}, {"name": "_attribute", "type": "str"}],
        "name": "getESInfoByToken",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "name": "getTokenURI",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "name": "getOwnerAddress",
        "outputs": [{"type": "Address"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAllOwners",
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_address", "type": "Address"}],
        "name": "setMinter",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_address", "type": "Address"}],
        "name": "removeMinter",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_address", "type": "Address"}],
        "name": "getTokensByAddress",
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_address", "type": "Address"}],
        "name": "numberOfTokensByAddress",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {"inputs": [{"name": "_msg", "type": "str"}], "name": "MessageLog", "type": "eventlog"},
]
