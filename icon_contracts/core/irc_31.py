# https://sejong.tracker.solidwallet.io/contract/cx162a79cc8eb19206cebeff47e2708cfc04f589b5

IRC31_METHODS = [
    {
        "name": "ApprovalForAll",
        "type": "eventlog",
        "inputs": [
            {"name": "_owner", "type": "Address", "indexed": "0x1"},
            {"name": "_operator", "type": "Address", "indexed": "0x1"},
            {"name": "_approved", "type": "bool"},
        ],
    },
    {
        "name": "TransferBatch",
        "type": "eventlog",
        "inputs": [
            {"name": "_operator", "type": "Address", "indexed": "0x1"},
            {"name": "_from", "type": "Address", "indexed": "0x1"},
            {"name": "_to", "type": "Address", "indexed": "0x1"},
            {"name": "_ids", "type": "bytes"},
            {"name": "_values", "type": "bytes"},
        ],
    },
    {
        "name": "TransferSingle",
        "type": "eventlog",
        "inputs": [
            {"name": "_operator", "type": "Address", "indexed": "0x1"},
            {"name": "_from", "type": "Address", "indexed": "0x1"},
            {"name": "_to", "type": "Address", "indexed": "0x1"},
            {"name": "_id", "type": "int"},
            {"name": "_value", "type": "int"},
        ],
    },
    {
        "name": "URI",
        "type": "eventlog",
        "inputs": [
            {"name": "_id", "type": "int", "indexed": "0x1"},
            {"name": "_value", "type": "str"},
        ],
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "_owner", "type": "Address"}, {"name": "_id", "type": "int"}],
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
    },
    {
        "name": "balanceOfBatch",
        "type": "function",
        "inputs": [{"name": "_owners", "type": "[]Address"}, {"name": "_ids", "type": "[]int"}],
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
    },
    {
        "name": "isApprovedForAll",
        "type": "function",
        "inputs": [{"name": "_owner", "type": "Address"}, {"name": "_operator", "type": "Address"}],
        "outputs": [{"type": "bool"}],
        "readonly": "0x1",
    },
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
    },
    {
        "name": "setApprovalForAll",
        "type": "function",
        "inputs": [{"name": "_operator", "type": "Address"}, {"name": "_approved", "type": "bool"}],
        "outputs": [],
    },
    {
        "name": "tokenURI",
        "type": "function",
        "inputs": [{"name": "_id", "type": "int"}],
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
    },
    {
        "name": "transferFrom",
        "type": "function",
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_id", "type": "int"},
            {"name": "_value", "type": "int"},
            {"name": "_data", "default": None, "type": "bytes"},
        ],
        "outputs": [],
    },
    {
        "name": "transferFromBatch",
        "type": "function",
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_ids", "type": "[]int"},
            {"name": "_values", "type": "[]int"},
            {"name": "_data", "default": None, "type": "bytes"},
        ],
        "outputs": [],
    },
]
