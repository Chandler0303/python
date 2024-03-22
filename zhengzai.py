import requests
import json
import execjs
import datetime
import time

# 获取演出信息，循环调用创建订单就可抢票

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


contextJs = execjs.compile(js_from_file('./zhengzai.js'))
session = requests.session()
comHeaders = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOTgwODkwMzIxMDAyNDk2MDA0MTAwOTg2IiwiY19hdCI6IjIwMjIxMjIzMTQ1NTA1IiwibW9iaWxlIjoiMTc2NzQxOTcwMzUiLCJuaWNrbmFtZSI6IuWuh-iIquWRmENoYW5lIiwidHlwZSI6InVzZXIiLCJleHAiOjE3MTM2ODI0NzAsImlhdCI6MTcxMTA5MDQ3MH0.2Zdqs9MNu8iDmkmy-fVEgkDXr1hsupaQ1cj6M0MvLyY'
}
showId = '3538955112060313606378398' 
enterIdList = ['1981249136437002242313008'] # 观演人
buyNum = 1
skuType = 'SINGLE' #'SINGLE_SKU'

success = { 
    'count': 0
}
# 定义一个特定的日期时间
dt = datetime.datetime(2024, 3, 21, 12, 20, 00)  # 2024年3月21日12:20:00
# 将日期时间转换为时间戳（以秒为单位）
setTimestamp = int(dt.timestamp())



# 获取演出详情数据 status 6 结算
def getPerformanceDetail():
    HEADERS = {
      **comHeaders
    }
    url = "https://kylin.zhengzai.tv/kylin/performance/partner/" + showId +"?isAgent=0"
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    return response.json()['data']['ticketTimesList']

ticketData = getPerformanceDetail()[0]['ticketList'][0]
# 获取演出观演人
def getEntersList():
    HEADERS = {
      **comHeaders
    }
    url = "https://adam.zhengzai.tv/adam/enters/list"
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    return response.json()['data']

getEntersList()


# 创建订单
def createOrder():
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }

    data = {
      'actual': ticketData['price'] * buyNum,
      'deviceFrom': 'wap', # applet
      'returnUrl': "https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=",
      'showUrl': "https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=",
      'enterIdList': enterIdList,
      'expressType': ticketData['expressType'],
      'isElectronic': ticketData['isElectronic'],
      'isExpress': ticketData['isExpress'],
      'number': buyNum,
      'payType': 'wepay', # alipay || wepay
      'performanceId': showId,
      'ticketId': ticketData['ticketsId'],
      'timeId': ticketData['timeId']
    }
    timestamp = int(datetime.datetime.now().timestamp())
    encryptedData = contextJs.call('encrypt', data)
    sign = contextJs.call('sign', encryptedData + str(timestamp))
    data = {
        'sign': sign,
        'timestamp': timestamp,
        'encryptedData': encryptedData
    }
    url = "https://order.zhengzai.tv/order/order/pre"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    # createOrder(orderJSON, orderData)
    return response.json()['data']



createOrder()



time.sleep(0.1)
