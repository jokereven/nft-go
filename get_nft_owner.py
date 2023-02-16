import requests
import urllib3
import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def get_nft_owner(contract_address):
    count = 0
    params = {
        'contractAddress': contract_address,
        'withTokenBalances': 'false',
    }
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/KTHY6dSRDoYxkAMQo0EfNEfRBCRvMO1o/getOwnersForCollection"
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        res = response.json()['ownerAddresses']
        sampled_array = random.sample(res, int(len(res) * 0.05))
        print("len(sampled_array) ==", len(sampled_array))
        for item in sampled_array:
            time.sleep(random.random())
            m = address_quality(item)
            print(m)
            if m > 0.5:
                count += 1
        print("count / len(sampled_array) ==", count / len(sampled_array))


def address_quality(address):
    url = "https://api.nftgo.io/api/v2/profile/stats/" + address + "/detail"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()['data']
        realizedProfitEth = data['realizedProfitEth']
        unrealizedProfitEth = data['unrealizedProfitEth']
        gasFeeEth = data['gasFeeEth']
        value = realizedProfitEth - unrealizedProfitEth - gasFeeEth
        return value


get_nft_owner("0xe785E82358879F061BC3dcAC6f0444462D4b5330")
