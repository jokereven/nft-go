import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


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


# address_quality("0xce4ba677aebcbb178376228801ac62bc9bea6c21")
address_quality("0xd864babec7bd14e09ad05d42ba91f58b88f634b5")
