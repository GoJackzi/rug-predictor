import os
import csv
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
RPC_URL = os.getenv("WEB3_RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Uniswap V2 Factory Address & Topic
FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
PAIR_CREATED_TOPIC = "0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9"

def get_latest_pairs_raw(num_blocks=100):
    """
    Fetches the latest PairCreated events using raw get_logs (more robust).
    """
    if not w3.is_connected():
        print("Error: Could not connect to Ethereum Node.")
        return []

    latest_block = w3.eth.block_number
    start_block = latest_block - num_blocks
    
    print(f"Scanning blocks {start_block} to {latest_block}...")
    
    try:
        logs = w3.eth.get_logs({
            'fromBlock': start_block,
            'toBlock': latest_block,
            'address': FACTORY_ADDRESS,
            'topics': [PAIR_CREATED_TOPIC]
        })
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

    print(f"Found {len(logs)} new pairs.")
    
    pairs_data = []
    for log in logs:
        # Decode log topics (Topic0 is event hash, Topic1=token0, Topic2=token1)
        # Check if topics has enough data (sometimes unindexed params are in data)
        # Uniswap PairCreated: event PairCreated(address indexed token0, address indexed token1, address pair, uint)
        try:
            # topics[0] is signature
            token0 = "0x" + log['topics'][1].hex()[-40:]
            token1 = "0x" + log['topics'][2].hex()[-40:]
            
            # Data contains pair address (first 32 bytes) and length (second 32 bytes)
            # data hex string: 0x...
            data = log['data'].hex()
            # remove 0x
            if data.startswith('0x'): data = data[2:]
            
            # Pair is first 32 bytes (64 chars), but it's an address so last 40 chars of that
            pair_address = "0x" + data[0:64][-40:]
            
            pairs_data.append({
                'block_number': log['blockNumber'],
                'transaction_hash': log['transactionHash'].hex(),
                'token0': token0,
                'token1': token1,
                'pair_address': pair_address
            })
        except Exception as e:
            print(f"Error decoding log: {e}")
            continue
        
    return pairs_data

def save_to_csv(data, filename="uniswap_pairs.csv"):
    file_exists = os.path.exists(filename)
    keys = data[0].keys() if data else []
    
    with open(filename, 'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Saved {len(data)} rows to {filename}")

if __name__ == "__main__":
    # Fetch in small chunks to avoid API limits
    CHUNK_SIZE = 10
    TOTAL_BLOCKS = 50
    
    latest_block = w3.eth.block_number
    
    all_pairs = []
    for i in range(0, TOTAL_BLOCKS, CHUNK_SIZE):
        # We need to modify get_latest_pairs_raw to accept start/end or do it here.
        # easier to just call logic here.
        # But for speed, let's just make get_latest_pairs_raw accept optional args
        # For now, quick dirty fix:
        pass
    
    # Actually, let's just create a better main loop using the existing function structure? 
    # No, get_latest_pairs_raw calculates start from num_blocks.
    # Let's rewrite the main block to be cleaner.

def fetch_historical_chunks(total_blocks=100, chunk_size=10):
    latest_block = w3.eth.block_number
    all_pairs = []
    
    for i in range(0, total_blocks, chunk_size):
        end_block = latest_block - i
        start_block = end_block - chunk_size
        
        print(f"Fetching chunk: {start_block} to {end_block}")
        try:
             logs = w3.eth.get_logs({
                'fromBlock': start_block,
                'toBlock': end_block,
                'address': FACTORY_ADDRESS,
                'topics': [PAIR_CREATED_TOPIC]
            })
             
             # Decode logs (Reuse logic or copy paste)
             for log in logs:
                try:
                    token0 = "0x" + log['topics'][1].hex()[-40:]
                    token1 = "0x" + log['topics'][2].hex()[-40:]
                    data = log['data'].hex()
                    if data.startswith('0x'): data = data[2:]
                    pair_address = "0x" + data[0:64][-40:]
                    
                    all_pairs.append({
                        'block_number': log['blockNumber'],
                        'transaction_hash': log['transactionHash'].hex(),
                        'token0': token0,
                        'token1': token1,
                        'pair_address': pair_address
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Chunk failed: {e}")
        
        time.sleep(0.2) # Nice to API
        
    return all_pairs

if __name__ == "__main__":
    pairs = fetch_historical_chunks(total_blocks=50, chunk_size=10)
    if pairs:
        save_to_csv(pairs)
