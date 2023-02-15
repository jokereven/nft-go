# 1. 通过合约地址获取合约owner
# 2. 查询owner创建的其他nft情况

import urllib3
from datetime import datetime

import time
import requests
import random
from eth_abi import decode_abi
from web3 import Web3
import json
import math

w3 = Web3(Web3.HTTPProvider(
    "https://mainnet.infura.io/v3/bb7f1a94a0174cac8c6d966fd925dbaa"))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

lid_arr = []

contract_address = "0xB3c7B1f310E2325B15B53c9fBA257D0330a2E315"

scanApikey = "KWFPSYEEKY27TK1ZPC1X8FWP6RUSR1YIYK"

params = {
    'module': 'contract',
    'action': 'getabi',
    'address': contract_address,
    'apikey': scanApikey
}

url = "https://api.etherscan.io/api"

res = requests.get(url, params=params)

if res.status_code == 200 and res.json()['status'] == '1':
    abi = res.json()['result']
    contract = w3.eth.contract(address=contract_address, abi=abi)
    functions = dir(contract.functions)
    if 'owner' in functions:
        owner = contract.functions.owner().call()
        # 查看owner创建的其他nft合约
        tx_count = w3.eth.get_transaction_count(owner)
        # 轮询查询
        page = tx_count / 25
        page = math.ceil(page)
        skip = 1
        while True:
            tx_params = {
                'module': 'account',
                'action': 'txlist',
                'address': owner,
                'startblock': 0,
                'endblock': 99999999,
                'page': skip,
                'offset': 25,
                'sort': 'asc',
                'apikey': scanApikey
            }
            tx = requests.get(url, params=tx_params)
            time.sleep(random.random())
            if tx.status_code == 200 and res.json()['status'] == '1':
                result = tx.json()['result']
                for item in result:
                    _inputData = item['input']
                    lid = len(_inputData)
                    print(lid)
                    lid_arr.append(lid)
                skip += 1
                if skip > page:
                    break
        print(lid_arr, len(lid_arr))
