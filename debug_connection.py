import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('g:/UniswapRugPredictor/.env')
url = os.getenv('WEB3_RPC_URL')
print(f"Connecting to: {url}")

w3 = Web3(Web3.HTTPProvider(url))

if w3.is_connected():
    print("SUCCESS: Connected to Ethereum Node.")
    try:
        block = w3.eth.block_number
        print(f"Current Block: {block}")
        
        print("Testing get_logs for Uniswap V2 Factory...")
        # Topic0 for PairCreated
        # 0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9
        logs = w3.eth.get_logs({
            'fromBlock': block - 5,
            'toBlock': block,
            'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
            'topics': ['0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9']
        })
        print(f"SUCCESS: Fetched {len(logs)} logs.")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print("FAILURE: Could not connect.")
