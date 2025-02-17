from itertools import count
import requests
import json
import execjs
import time
import datetime

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


    
contextJs = execjs.compile(js_from_file('./index.js'))
session = requests.session()
count = 0
requestUrl = 'https://wap.showstart.com/v3' # https://wap.showstart.com/v3 (h5) https://api3.showstart.com（miniweix）
st_flpv = contextJs.call('uuid')
token = contextJs.call('uuid', 32)
sign = '7a4fe6f2485df7c95111d54a959602aa' # 用户个人签名
userId = '3577537' # 用户个人id 3577537
idToken = '56aae441ee5bb97d6612140cf9bcb818' # 用户idtoken 会经常刷新
activityId = '224035' # 演出ID
ticketId = '4d5015f529654b29a1cbe439e33ff692' # 具体化某一场演出的id
ticketNum = 1
commonPerfomerIds = [22813295] # 需要绑定的观演人 1018110
comHeaderParams = {
    "st_flpv": st_flpv,
    "sign": sign,
    "userId": userId,
    "token": token,
    "idToken": idToken
}



# 获取token
def getToken(sign = ''):
    requestData = {
        "st_flpv": st_flpv,
        "sign": sign,
        "trackPath": ''
    }
    HEADERS = contextJs.call('getHeaders', {
        "url": "/waf/gettoken",
        'timeUuid': contextJs.call('timeUuid', 32),
        **comHeaderParams,
    }, requestData)
    print(HEADERS)
    url = requestUrl + "/waf/gettoken"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return {
        "accessToken": response.json()['result']['accessToken']['access_token'], 
        "idToken": response.json()['result']['idToken']['id_token']
    }

tokenData = getToken()

# 获取首页列表数据
def getList():
    requestData = {
        "activityType": 1379,
        "cityCode": "755",
        "cityType": 0,
        "couponCode": "",
        "isHome": 1,
        "isNew": 0,
        "pageNo": 1,
        "pageSize": 10,
        "sign": sign,
        "st_flpv": st_flpv,
        "style": '',
        "trackPath": '',

    }
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        'timeUuid': contextJs.call('timeUuid', 32),
        "url": "/wap/activity/list",
        "accessToken": tokenData['accessToken']
    }, requestData)
    # print(HEADERS)
    url = requestUrl + "/wap/activity/list"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()

# getList()

# 获取用户演出订单
def getUserList():
    requestData = {
        "history": 1,
        "pageNo": 1,
        "sign": sign,
        "st_flpv": st_flpv,
        "trackPath": '',

    }
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        'timeUuid': contextJs.call('timeUuid', 32),
        "url": "/order/wap/order/list",
        "accessToken": tokenData['accessToken']
    }, requestData)
    print(HEADERS)
    url = requestUrl + "/order/wap/order/list"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()

# getUserList()

# 查看演出日期列表
def getActivityTicket():
    requestData = {
        "activityId": activityId,
        "coupon": '',
        "sign": sign,
        "st_flpv": st_flpv,
        "trackPath": '',

    }
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        'timeUuid': contextJs.call('timeUuid', 32),
        "url": "/wap/activity/V2/ticket/list",
        "accessToken": tokenData['accessToken']
    }, requestData)
    # print(HEADERS)
    url = requestUrl + "/wap/activity/V2/ticket/list"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    # 返回的saleStatus 为 1 可购买
    return response.json()

getActivityTicket()

# 获取观演人列表
def cpList():
    requestData = {
        "ticketId": ticketId,
        "sign": sign,
        "st_flpv": st_flpv,
        "trackPath": '',

    }
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        'timeUuid': contextJs.call('timeUuid', 32),
        "url": "/wap/cp/list",
        "accessToken": tokenData['accessToken']
    }, requestData)
    url = requestUrl + "/wap/cp/list"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()

cpList()

# 确定订单
def orderConfirm():
    requestData = {
        "sequence": activityId,
        "ticketId": ticketId,
        "ticketNum": ticketNum,
        "sign": sign,
        "st_flpv": st_flpv,
        "trackPath": '',

    }
    timeUuid = contextJs.call('timeUuid', 32)
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        'timeUuid': timeUuid,
        "url": "/order/wap/order/confirm",
        "accessToken": tokenData['accessToken']
    }, requestData)
    url = requestUrl + "/order/wap/order/confirm"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    # print(response.json())
    orderInfoVo = response.json()['result']['orderInfoVo']
    createOrder(orderInfoVo)



# 创建订单
def createOrder(orderInfoVo):
  
    ticketType = 1
    ticketTypeView = ["实体票寄送", "实体票自取"]
    timeUuid = contextJs.call('timeUuid', 32)
    formData = {
        'orderDetails': [{
            'goodsType': 1,
            'skuType': orderInfoVo['ticketPriceVo']['ticketType'],
            'num': ticketNum, # orderInfoVo['ticketPriceVo']['transformNum'],
            'goodsId': orderInfoVo['activityId'],
            'skuId': orderInfoVo['ticketPriceVo']['ticketId'],
            'price': orderInfoVo['ticketPriceVo']['price'],
            'goodsPhoto': orderInfoVo['poster'],
            'dyPOIType':  orderInfoVo['ticketPriceVo']['dyPOIType'],
            'goodsName': orderInfoVo['title'],
            'douyinPoiId': '' # orderInfoVo['douyinPoiId'],
        }],
        'commonPerfomerIds': commonPerfomerIds, # 观演人ID
        'areaCode': orderInfoVo['areaCode'],
        'telephone': orderInfoVo['telephone'],
        'addressId': "",
        'teamId': "",
        'couponId': "", # 优惠券
        'checkCode': '',
        'source': 0,
        'discount': 0,  # 折扣价格
        'sessionId': orderInfoVo['sessionId'],
        'freight': 0, # orderInfoVo['freight'],
        'amountPayable': orderInfoVo['ticketPriceVo']['price'] * ticketNum,
        'totalAmount': orderInfoVo['ticketPriceVo']['price'] * ticketNum,
        'partner': '',
        'orderSource': 1,
        'videoId': '',
        'payVideotype': '',
        "st_flpv": st_flpv,
        "sign": sign,
        'trackPath': '',
    }

    key = contextJs.call('setKey', {
        "token": comHeaderParams['token'],
        "timeUuid": timeUuid,
    })
    requestData = {'q': contextJs.call('encrypt', formData, key['k'])}
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        "timeUuid": timeUuid,
        "url": "/nj/order/order",
        "accessToken": tokenData['accessToken']
    }, requestData)
    url = requestUrl + "/nj/order/order"
    data = json.dumps(requestData, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    if response.json()['state'] == '1':
        count = 100
    else:
        createOrder(orderInfoVo)
    return response.json()


for i in range(1):
     # now = datetime.datetime.now()
     # if now.hour == 11 and now.minute == 59:
     #     orderConfirm()
     # if now.hour == 12:
     #     orderConfirm()
    orderConfirm()
    time.sleep(0.3)
    if count > 0:
        break


# 下单订单查询
def orderList():
    timeUuid = contextJs.call('timeUuid', 32)
    key = contextJs.call('setKey', {
        "token": comHeaderParams['token'],
        "timeUuid": timeUuid
    })
    requestData = {'q': contextJs.call('encrypt', {
        'pageNo':1,
        'pageSize':100,
        'totalAmount':"40.00",
        'goodsId': activityId,
        'goodsType':1,
        'ticketId': ticketId,
        'st_flpv':st_flpv,
        'sign':sign,
        'trackPath':""
    }, key['k'])}
    HEADERS = contextJs.call('getHeaders', {
        **comHeaderParams,
        "timeUuid": timeUuid,
        "url": "/nj/coupon/order_list",
        "accessToken": tokenData['accessToken']
    }, requestData)

    url = requestUrl + "/nj/coupon/order_list"
    data = requestData
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    return response.json()

# orderList()
