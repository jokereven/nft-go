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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

w3 = Web3(Web3.HTTPProvider(
    "https://mainnet.infura.io/v3/bb7f1a94a0174cac8c6d966fd925dbaa"))

url = "https://api.etherscan.io/api"

contract_address = "0x26d6c3e7aefce970fe3be5d589dbabfd30026924"

arr = []
ca_arr = []

scanApikey = "KWFPSYEEKY27TK1ZPC1X8FWP6RUSR1YIYK"


def get_owner():
    params = {
        'module': 'contract',
        'action': 'getabi',
        'address': contract_address,
        'apikey': scanApikey
    }
    res = requests.get(url, params=params)
    if res.status_code == 200 and res.json()['status'] == '1':
        abi = res.json()['result']
        contract = w3.eth.contract(address=contract_address, abi=abi)
        functions = dir(contract.functions)
        if 'owner' in functions:
            owner = contract.functions.owner().call()
            print("contract_address:", contract_address,
                  "contract_owner:", owner)

# total_volume


def total_volume(contract_address):
    skip = 0
    volume_sum = 0
    while True:
        params = {
            'contract': contract_address,
            'skip': skip,
            'limit': 10
        }
        url = 'https://branch4-data-farmer-api.nftgo.dev/api/v1/contract/transfer'
        response = requests.get(
            url, params=params, headers=headers, verify=False)
        time.sleep(random.random() * 2)
        if response.status_code == 200:
            res = response.json()['list']
            if res != []:
                for item in res:
                    volume = item['order']['platform']['price']
                    volume_sum += volume
                    print('skip:', skip, 'volume_sum:', volume_sum)
                skip += 10
            else:
                return volume_sum


# Get Contract Creator
get_creater_params = {
    'module': 'contract',
    'action': 'getcontractcreation',
    'contractaddresses': contract_address,
    'apikey': scanApikey
}
get_creater_res = requests.get(url, params=get_creater_params)
if get_creater_res.status_code == 200 and get_creater_res.json()['status'] == '1':
    contract_creater = get_creater_res.json()['result'][0]['contractCreator']
    # 查看creater创建的其他nft合约
    contract_creater = w3.toChecksumAddress(contract_creater)
    print("contract_creater ==", contract_creater)
    tx_count = w3.eth.get_transaction_count(contract_creater)
    # 轮询查询
    print("tx_count ==", tx_count)
    page = tx_count / 25
    page = math.ceil(page)
    skip = 1
    while True:
        tx_params = {
            'module': 'account',
            'action': 'txlist',
            'address': contract_creater,
            'startblock': 0,
            'endblock': 99999999,
            'page': skip,
            'offset': 25,
            'sort': 'asc',
            'apikey': scanApikey
        }
        tx = requests.get(url, params=tx_params)
        time.sleep(random.random() * 2)
        if tx.status_code == 200 and tx.json()['status'] == '1':
            result = tx.json()['result']
            for item in result:
                _inputData = item['input']
                txHash = item['hash']
                methodId = item['methodId']
                ca = item['contractAddress']
                if methodId.startswith("0x6"):
                    ca_arr.append(ca)
                    arr.append(txHash)
            skip += 1
            if skip > page:
                break
    for c in ca_arr:
        tc = total_volume(c)
        print('contract_address:', contract_address, 'total_volume:', tc)
