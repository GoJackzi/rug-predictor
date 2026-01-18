import csv
import random
import time

def generate_mock_data(filename="labeled_pairs.csv", count=500):
    print(f"Generating {count} synthetic tokens for training...")
    
    headers = [
        'block_number', 'pair_address', 'token0', 'token1', 
        'creator_address', 'liquidity_eth', 'is_locked', 
        'has_mint_function', 'creator_funded_by_tornado', 
        'status', 'drop_percent'
    ]
    
    data = []
    for i in range(count):
        is_rug = random.random() < 0.8 # 80% Rugs in wild
        
        # Correlated Features
        if is_rug:
            has_mint = random.random() < 0.6
            is_locked = random.random() < 0.3
            funded_by_tornado = random.random() < 0.7
            liquidity = random.uniform(0.1, 5.0) # Low liquidity
            drop = random.uniform(-99.9, -80.0)
            status = "RUG"
        else:
            has_mint = random.random() < 0.1
            is_locked = True
            funded_by_tornado = random.random() < 0.1
            liquidity = random.uniform(5.0, 100.0) # Higher liquidity
            drop = random.uniform(-20.0, 50.0)
            status = "SAFE"
            
        row = {
            'block_number': 18000000 + i,
            'pair_address': f"0x{random.randint(0, 2**160):040x}",
            'token0': f"0x{random.randint(0, 2**160):040x}",
            'token1': "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", # WETH
            'creator_address': f"0x{random.randint(0, 2**160):040x}",
            'liquidity_eth': round(liquidity, 2),
            'is_locked': is_locked,
            'has_mint_function': has_mint,
            'creator_funded_by_tornado': funded_by_tornado,
            'status': status,
            'drop_percent': round(drop, 2)
        }
        data.append(row)

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Successfully created {filename}")

if __name__ == "__main__":
    generate_mock_data()
