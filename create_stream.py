from moralis import streams

ERC20_transfer_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "type": "event",
    }
]

BALANCE_OF_ABI = {
    "constant": True,
    "inputs": [{"name": "_owner", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "balance", "type": "uint256"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function",
}


FROM_BALANCE_TRIGGER = {
    "contractAddress": "$contract",
    "functionAbi": BALANCE_OF_ABI,
    "inputs": ["$from"],
    "type": "erc20transfer",
}

TO_BALANCE_TRIGGER = {
    "contractAddress": "$contract",
    "functionAbi": BALANCE_OF_ABI,
    "inputs": ["$to"],
    "type": "erc20transfer",
}
NEW_STREAM_BODY = {
    "description": "Wallet Triggers 2",
    "tag": "Wallet Triggers 2",
    "topic0": ["transfer(address,address,uint256)"],
    "allAddresses": False,
    "includeNativeTxs": True,
    "includeContractLogs": False,
    "includeInternalTxs": False,
    "includeAllTxLogs": False,
    "getNativeBalances": [],
    "abi": ERC20_transfer_ABI,
    "webhookUrl": "https://webhook.site/afe0d37f-85db-47ce-86b4-d5a046304467",
    "chainIds": ["0x61"],
    "triggers": [FROM_BALANCE_TRIGGER, TO_BALANCE_TRIGGER],
}

api_key = "YOUR_API_KEY"


results = streams.evm_streams.create_stream(api_key=api_key, body=NEW_STREAM_BODY)
print(results)
