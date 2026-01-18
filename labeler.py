import csv
import os
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("WEB3_RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Uniswap V2 Pair ABI (Just getReserves)
PAIR_ABI = '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]'

def get_token_price(pair_address, block_number):
    """
    Returns the price of Token0 in terms of Token1 at a specific block.
    """
    try:
        contract = w3.eth.contract(address=pair_address, abi=PAIR_ABI)
        reserves = contract.functions.getReserves().call(block_identifier=block_number)
        
        reserve0 = reserves[0]
        reserve1 = reserves[1]
        
        if reserve0 == 0 or reserve1 == 0:
            return 0
            
        return reserve1 / reserve0 # Price of Token0 in Token1
    except Exception as e:
        # print(f"Error getting price for {pair_address}: {e}")
        return None

def label_data(input_file="uniswap_pairs.csv", output_file="labeled_pairs.csv"):
    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    labeled_rows = []
    print(f"Labeling {len(rows)} tokens...")
    
    current_block = w3.eth.block_number

    for row in rows:
        pair_address = row['pair_address']
        creation_block = int(row['block_number'])
        
        # Check price 100 blocks after creation (approx 20 mins)
        start_price = get_token_price(pair_address, creation_block + 100)
        
        # Check price now
        end_price = get_token_price(pair_address, current_block)
        
        status = "UNKNOWN"
        drop_percent = 0.0
        
        if start_price and end_price and start_price > 0:
            change = (end_price - start_price) / start_price
            drop_percent = change * 100
            
            # Simple Heuristic Labeling
            if change < -0.90: # 90% Drop
                status = "RUG"
            elif change > -0.50: # Dropped less than 50% (or went up)
                status = "SAFE"
            else:
                status = "VOLATILE" # 50-90% drop, maybe soft rug or just bad coin
        
        row['status'] = status
        row['drop_percent'] = round(drop_percent, 2)
        labeled_rows.append(row)
        print(f"Pair {pair_address[:6]}... Status: {status} ({row['drop_percent']}%)")
        time.sleep(0.1) # Rate limit nice

    # Save
    keys = labeled_rows[0].keys()
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(labeled_rows)
    print(f"Saved labeled data to {output_file}")

if __name__ == "__main__":
    label_data()
