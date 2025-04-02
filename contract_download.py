import requests
import json
import time
import os
import re
            
def get_contract_source(address, api_key):
    url = f"https://api.etherscan.io/v2/api?chainId=1"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        # response.encoding = 'utf-8'
        data = response.json()
        # data = json.loads(response.content.decode('utf-8'))
        if data["status"] == "1" and data["result"][0]["SourceCode"]:
            return data["result"][0]
        return None
    except Exception as e:
        print(f"Error fetching contract {address}: {str(e)}")
        return None

def extract_and_save_contracts(address, contract_data, output_dir):
    contract_name = contract_data.get("ContractName", "Unknown")
    source_code = contract_data.get("SourceCode", "")
    
    if not source_code:
        print(f"No source code found for {address}")
        return
    
    # Create a folder for this contract
    contract_dir = os.path.join(output_dir, f"{address}_{contract_name}")
    os.makedirs(contract_dir, exist_ok=True)
    
    try:
        # Check if the source code is JSON formatted (multiple files)
        if source_code.startswith('{') and source_code.endswith('}'):
            # Try to parse as JSON
            try:
                # Some contracts have double JSON encoding
                if source_code.startswith('{{') and source_code.endswith('}}'):
                    source_code = source_code[1:-1]
                
                source_json = json.loads(source_code)
                
                # Handle standard JSON output format
                if "sources" in source_json:
                    for file_path, file_info in source_json["sources"].items():
                        file_content = file_info.get("content", "")
                        if file_content:
                            # Preserve directory structure
                            full_path = os.path.join(contract_dir, file_path)
                            os.makedirs(os.path.dirname(full_path), exist_ok=True)
                            with open(full_path, 'w', encoding='utf-8') as f:
                                f.write(file_content)
                            print(f"Saved {file_path} for contract {address}")
                    return
                
                # If it's a simple dict with filenames as keys
                for file_name, content in source_json.items():
                    if isinstance(content, str):
                        # Check if there's path information in the key
                        if '/' in file_name or '\\' in file_name:
                            full_path = os.path.join(contract_dir, file_name)
                            os.makedirs(os.path.dirname(full_path), exist_ok=True)
                            with open(full_path, 'w',encoding='utf-8') as f:
                                f.write(content)
                        else:
                            with open(os.path.join(contract_dir, file_name), 'w', encoding='utf-8') as f:
                                f.write(content)
                        print(f"Saved {file_name} for contract {address}")
                return
            except json.JSONDecodeError:
                # Not valid JSON, treat as a single file
                pass
        
        # If we get here, treat as a single Solidity file
        main_file = os.path.join(contract_dir, f"{contract_name}.sol")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(source_code)
        print(f"Saved {contract_name}.sol for contract {address}")
        
    except Exception as e:
        print(f"Error processing contract {address}: {str(e)}")
        

def main():
    # Configure these variables
    ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"
    INPUT_FILE = "eth_contracts.txt"
    OUTPUT_DIR = "downloaded_contracts"
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Read addresses from file
    with open(INPUT_FILE, 'r') as f:
        addresses = [addr.strip() for addr in f.readlines() if addr.strip()]
    
    for pair_address in addresses:
        print(f"Processing contract: {pair_address}")
        
        # Get contract source code using the base token address
        contract_data = get_contract_source(pair_address, ETHERSCAN_API_KEY)
        
        if contract_data:
            extract_and_save_contracts(pair_address, contract_data, OUTPUT_DIR)
        else:
            print(f"Failed to get contract data for address {pair_address}")
        
        # Add delay to respect rate limits
        time.sleep(0.5)  # Increased delay to account for multiple API calls

if __name__ == "__main__":
    main()