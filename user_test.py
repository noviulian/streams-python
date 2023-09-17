from moralis import streams

# use pickle persistence to store the stream ids
import pickle

# TODO: in production use environment variables
MORALIS_API_KEY = "YOUR KEY"
WEBHOOK_URL = "https://webhook.site/afe0d37f-85db-47ce-86b4-d5a046304467"

TRANSFER_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    }
]


BALANCEOF_FROM_ABI = {
    "constant": True,
    "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"internalType": "uint256", "name": "fromBalance", "type": "uint256"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function",
}

BALANCEOF_TO_ABI = {
    "constant": True,
    "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"internalType": "uint256", "name": "toBalance", "type": "uint256"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function",
}

FROM_BALANCE_TRIGGER = {
    "contractAddress": "$contract",
    "functionAbi": BALANCEOF_FROM_ABI,
    "inputs": ["$from"],
    "type": "erc20transfer",
}

TO_BALANCE_TRIGGER = {
    "contractAddress": "$contract",
    "functionAbi": BALANCEOF_TO_ABI,
    "inputs": ["$to"],
    "type": "erc20transfer",
}

TRIGGERS = [FROM_BALANCE_TRIGGER, TO_BALANCE_TRIGGER]

NEW_STREAM_BODY = {
    "description": "Wallet Triggers",
    "tag": "Wallet Triggers",
    "topic0": ["Transfer(address,address,uint256)"],
    "allAddresses": False,
    "includeNativeTxs": True,
    "includeContractLogs": False,
    "includeInternalTxs": False,
    "includeAllTxLogs": False,
    "getNativeBalances": [],
    "abi": TRANSFER_ABI,
    "triggers": TRIGGERS,
}


class MoralisWeb3:
    API_KEY = MORALIS_API_KEY
    WEBHOOK_URL = WEBHOOK_URL
    STREAM_ID_FILE = "stream_id.p"
    BUSD_TESTNET = "0x91687aD93860Be0c1C9849bdf81efa6B272f1dAf"

    def create_new_stream(self, chain_ids: list = None):
        # TODO: Check all active chains and add them to the chain_ids list

        body = NEW_STREAM_BODY
        body["webhookUrl"] = WEBHOOK_URL
        body["chainIds"] = chain_ids if chain_ids else ["0x61"]

        result = streams.evm_streams.create_stream(api_key=self.API_KEY, body=body)

        # add id to pickle file
        pickle.dump(result["id"], open(self.STREAM_ID_FILE, "wb"))

        # ADD TRIGGERS TO STREAM
        # streams.evm_streams.update_stream(api_key=self.API_KEY, params={ "id": result["id"] }, body={ "triggers": TRIGGERS })

        print(result)
        return result["id"]


if __name__ == "__main__":
    mor = MoralisWeb3()
    mor.create_new_stream()
