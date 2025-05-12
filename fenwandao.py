import requests
import json
import datetime
import time
import schedule


baseUrl = 'https://api.livelab.com.cn'

session = requests.session()
comHeaders = {
    "platform-type": "%E7%BA%B7%E7%8E%A9%E5%B2%9B%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F",
    "x-fwd-anonymousId": "ocXac5NDmchqbV1gA1dwrTLMsaKo",
    "platform-version": "3.6.0",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJjdCI6MTc0NzA1NTA4NTA1MSwic3ViIjoiTDIxMTk2MjI0NyIsImF1ZCI6IkxJVkVMQUIiLCJpc3MiOiJUSUNLRVQiLCJtaWQiOjE5NjA2NTksInR5cGUiOiJhcHBsZXQiLCJpYXQiOjE3NDcwNTUwODUsImRpZCI6IkZDOUM5ODBDLUM1QTItNDFEMS05NkQ2LUUzNDA2MkNFOEJBMiIsImtleSI6IkxJVkVMQUIifQ.t0cnds_O8C57kyo5EQsdXnaFwDXv7kdhP-Qmk3_CnitdnI4ckPSB6pcf9ztQ4YPps39ymlNW5-SMFstcW8PYvw",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.59(0x18003b28) NetType/WIFI Language/zh_CN"
}
projectId = '7469731373' 


def getPerforms():
    HEADERS = {
      **comHeaders
    }
    url = baseUrl + "/performance/app/project/get_performs?project_id=" + projectId
    response = requests.get(url, headers=HEADERS)
    print(response.json()['data']['performInfos'][0]['performInfo'][0]['seatPlans'][1])
    return response.json()['data']

seatPlans = getPerforms()['performInfos'][0]['performInfo'][0]['seatPlans'][1]



def createOrder():
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }

    data = {"deliveryType":1,"contactName":"侯玲风","contactPhone":"17674197035","combineTicketVos":None,"ordinaryTicketVos":None,"payment":seatPlans['price'] * 2,"totalPrice":seatPlans['price'] * 2,"performId":seatPlans['performId'],"projectId":projectId,"privilegeCodeList":[],"audienceCount":2,"frequentIds":[43650095,43650104],"seatPlanIds":[seatPlans['seatPlanId']],"blackBox":":0"}
    url = baseUrl + "/order/app/center/v3/create"
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=HEADERS, data=data, json=data)
    print(data)
    print(response.json())
    if response.json()['code'] == 10000:
        print('success')
    else:
        # time.sleep(0.03)
        createOrder()


schedule.every().day.at("00:06").do(createOrder)


while True:
    schedule.run_pending()

