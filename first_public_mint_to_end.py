import requests
import urllib3
import datetime
import random
import time
from web3 import Web3
from collections import Counter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

w3 = Web3(Web3.HTTPProvider(
    "https://mainnet.infura.io/v3/bb7f1a94a0174cac8c6d966fd925dbaa"))

scanApikey = "KWFPSYEEKY27TK1ZPC1X8FWP6RUSR1YIYK"

contract_address = "0x06971F85c9e0Ba82e9bc4c7bE54f601ddEd00835"

time_arr = []

# 获取15天之前的unix时间戳, 这里默认nft合约从 create 到 mint 到是没有 15 天
now = datetime.datetime.now()
delta = datetime.timedelta(days=134/1440)
target_date = now - delta
target_timestamp = int(time.mktime(target_date.timetuple()))

params = {
    'module': 'block',
    'action': 'getblocknobytime',
    'timestamp': target_timestamp,
    'closest': 'before',
    'apikey': scanApikey
}


def get_block_no_by_time():
    url = "https://api.etherscan.io/api"
    res = requests.get(url, params=params)
    if res.status_code == 200 and res.json()['status'] == '1':
        from_block_number = res.json()['result']
        return from_block_number


# from block
f = 16254165
# latest block
latest_block = 16254179
# 区块数差
diff = latest_block - int(f)
print('diff ==', diff)

# 遍历指定区块并提取交易记录
for block_number in range(int(f), latest_block + 1):
    time.sleep(random.random())
    block = w3.eth.get_block(block_number)
    print("block.transactions", len(block.transactions))
    for tx_hash in block.transactions:
        tx = w3.eth.get_transaction(tx_hash)
        if tx['to'] == contract_address:
            input_data = tx['input']
            # mint(uint256 amount)
            # mint(uint16 quantity)
            if input_data.startswith('0x23cf0a22'):
                tx_hash = tx.blockHash.hex()
                block = w3.eth.get_block(tx.blockNumber)
                timestamp = block.timestamp
                time_arr.append(timestamp)
counts = Counter(time_arr)
for item, count in counts.items():
    dt_object = datetime.datetime.fromtimestamp(item)
    print(f"{dt_object}: {count}")
