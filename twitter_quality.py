# 1. 通过和合于地址获取twitter id
# 2. todo
# 3. todo

import time
import random
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


# 获取 twitter_id
def get_twitter_id(contract_address):
    url = "https://api.catchmint.xyz/contracts/" + contract_address
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            twitter_url = response.json()['twitterUrl']
            # 判断 twitter_url 是否为空
            if twitter_url != "":
                twitter_id = twitter_url[20:]
                id = twitter_id.lower()
                time.sleep(random.random())
                # 通过 twitter_id 获取 twitter质量
                get_twitter_quality(twitter_id=id)
            else:
                print('no twitter')
        if response.status_code == 404:
            print('response.status_code == 404')
    except Exception as e:
        print(f'[get_twitter_id] failed error: {e}')


# 通过 twitter_id 获取 twitter quality
def get_twitter_quality(twitter_id):
    params = {
        'screen_name': twitter_id,
    }
    url = "https://api-app.sparktoro.com/free/basics"
    try:
        response = requests.get(
            url, params=params, headers=headers, verify=False)
        print(response.text)
        if response.status_code == 200:
            quality = response.json()
            print(quality)
    except Exception as e:
        print(f'[get_twitter_quality] failed error: {e}')


# Proof of Cheese
# https://opensea.io/collection/proof-of-cheese
# get_twitter_id("0x06971F85c9e0Ba82e9bc4c7bE54f601ddEd00835")

# FIXME
# get_twitter_quality("proof_of_cheese")
# {"error":"Not authorized currently"}
