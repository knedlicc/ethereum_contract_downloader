# 🌐 Ethereum Contract Downloader 📜

A Python script for downloading Ethereum smart contract source code from Etherscan.

Check out another repo to scrape a list of contract addresses from the DexScreener: [dexscreener-scraper](https://github.com/knedlicc/dexscreener-scraper)

## 📋 Overview

This tool allows you to batch download verified Solidity smart contracts from the Ethereum blockchain using the Etherscan API. The script handles different source code formats, preserves directory structures, and organizes downloaded contracts neatly.

## ✨ Features

- 📥 Batch download of multiple contracts from a list of addresses
- 🧩 Handles both single file contracts and multi-file projects
- 📁 Preserves original directory structure of contracts
- 🔍 Identifies import statements that might need resolution
- 📝 UTF-8 encoding support for proper character handling
- ⏱️ Rate limiting to respect Etherscan API constraints

## 🛠️ Requirements

- Python 3.6+
- `requests` library

## 🚀 Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ethereum_contract_downloader
```

2. Install required dependencies:
```bash
pip install requests
```

3. Create an `eth_contracts.txt` file with one Ethereum contract address per line:
```
0x1234567890123456789012345678901234567890
0xabcdef0123456789abcdef0123456789abcdef01
```

4. Configure your Etherscan API key in the script or as an environment variable.

## ⚙️ Configuration

Edit the following variables in the script:

```python
ETHERSCAN_API_KEY = "YOUR_API_KEY"  # Get from etherscan.io
INPUT_FILE = "eth_contracts.txt"     # File with list of contract addresses
OUTPUT_DIR = "downloaded_contracts"  # Where to save the contracts
```

## 📖 Usage

Run the script:

```bash
python contract_download.py
```

The script will:
1. Read addresses from `eth_contracts.txt`
2. Fetch source code for each address using Etherscan API
3. Save contracts to the output directory with format: `ADDRESS_CONTRACTNAME/`
4. For multi-file contracts, the directory structure is preserved

## 📌 Example Output

```
Processing contract: 0x1234567890123456789012345678901234567890
Saved Token.sol for contract 0x1234567890123456789012345678901234567890
Found 3 imports in Token.sol

Processing contract: 0xabcdef0123456789abcdef0123456789abcdef01
Saved contracts/token/ERC20.sol for contract 0xabcdef0123456789abcdef0123456789abcdef01
Saved contracts/access/Ownable.sol for contract 0xabcdef0123456789abcdef0123456789abcdef01
```

## 🔮 Future Improvements

- Support for other blockchain explorers
- Parallel downloading to improve speed
- Command-line arguments for better flexibility

## ⚠️ Note

Be mindful of Etherscan API rate limits when downloading large numbers of contracts.

## 📄 License

MIT License
