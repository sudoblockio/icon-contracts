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
