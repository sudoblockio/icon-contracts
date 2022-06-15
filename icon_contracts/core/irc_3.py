# https://sejong.tracker.solidwallet.io/contract/cxd1a990d6ad986b064a9aac1474ba0cfeff64fd32


IRC3_METHODS = [
    {
        "name": "Approval",
        "type": "eventlog",
        "inputs": [
            {"name": "_owner", "type": "Address", "indexed": "0x1"},
            {"name": "_approved", "type": "Address", "indexed": "0x1"},
            {"name": "_tokenId", "type": "int", "indexed": "0x1"},
        ],
    },
    {
        "name": "Transfer",
        "type": "eventlog",
        "inputs": [
            {"name": "_from", "type": "Address", "indexed": "0x1"},
            {"name": "_to", "type": "Address", "indexed": "0x1"},
            {"name": "_tokenId", "type": "int", "indexed": "0x1"},
        ],
    },
    {
        "name": "approve",
        "type": "function",
        "inputs": [{"name": "_to", "type": "Address"}, {"name": "_tokenId", "type": "int"}],
        "outputs": [],
    },
    {
        "name": "getApproved",
        "type": "function",
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "outputs": [{"type": "Address"}],
        "readonly": "0x1",
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "_owner", "type": "Address"}],
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
    },
    {
        "name": "ownerOf",
        "type": "function",
        "inputs": [{"name": "_tokenId", "type": "int"}],
        "outputs": [{"type": "Address"}],
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
        "inputs": [{"name": "_to", "type": "Address"}, {"name": "_tokenId", "type": "int"}],
        "outputs": [],
    },
    {
        "name": "transferFrom",
        "type": "function",
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_tokenId", "type": "int"},
        ],
        "outputs": [],
    },
]
