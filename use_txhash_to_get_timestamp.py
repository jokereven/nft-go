from datetime import datetime
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(
    "https://mainnet.infura.io/v3/bb7f1a94a0174cac8c6d966fd925dbaa"))

# 获取交易信息
tx_hash = Web3.toBytes(
    hexstr='0x448f757a77be81d2c9d30f0f4c6da6743b4cd7af91e7a538b2ce7b6130084675')
tx = w3.eth.get_transaction(tx_hash)

# 获取交易所在块的信息
block = w3.eth.get_block(tx.blockNumber)

# 获取交易时间
timestamp = block.timestamp
tx_time = datetime.fromtimestamp(timestamp)

print(f'Transaction time: {tx_time}')
