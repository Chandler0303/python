import requests
import json
import execjs
import time
from datetime import datetime
import random

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


# src: weixin_mini
# merchant-id: 6267a80eed218542786f1494
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/9079

# xweb_xhr: 1
# ver: 4.2.3
# Accept: */*
# Sec-Fetch-Site: cross-site
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://servicewechat.com/wxad60dd8123a62329/277/page-frame.html
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9


contextJs = execjs.compile(js_from_file('./piaoxingqiu.js'))
session = requests.session()
requestUrl = 'https://m.piaoxingqiu.com'
comHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/9079',
    'Sec-Ch-Ua-Platform': "Android",
    'Src':'weixin_mini',
    'Terminal-Src': 'WEIXIN_MINI',
    'merchant-id': '6267a80eed218542786f1494',
    'Access-Token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNp8UUuPgjAQ_i9z5lAKtsWbshpJNBpWDp5IsUMk4ZVSNusa__u2aFZPe_ym32umN-jkaC5JW3Ywb8e69mAcUD_wDYrqJ-4UwhzWm22-Aw-GsVj-DRllXAqCqKgvZiHlgpV-GIWWZ5VpVzvSMjutUjtpzDlz1soJg5KWIiBMBYwXhBAfQ8HLp_BFmwVCyYCWTKGcaEQJSQq4T7x9j1qa7l-utJbm2tsivq2A-nyRrXlf9wv1UHUtzKkHvdSmMhMCZoX43Vcaj1Xj5DzkkRA2xnp7cNYozeuJRjyIKGMz6zJcB4PN80TxIslPSR5v99lHPp0iP2RpvFl8rvLDdnFc79PdI-k9wvrbni3WbrXXt7TSxTl8_wUAAP__.NfN_7HCIoueS4R9FwGtA7lEk6H3fqv-cF_MPiGMm_P2OCZ9EBLzbiN3q9F0KP3ZNI9SVECfvX2bNrkm97pxP4HKUVylm5dsdySBUMTNi8UjPKlLbBLY99NR-u8CFuiZQ0njlE6-anOqcnjUKj08CWXnQQO24w1W2-VDudMUwW8A'
}
showId = '67e0dd672bf16100013accc2'  # 演出ID
buyNum = 1
sessionIndex = 0 # 某一天的session数据下标，默认第一项
seatPlanIndex =  2 # 座位数据下标，默认第一项
skuType = 'SINGLE' #'SINGLE_SKU'
src = 'weixin_mini' # 'H5' weixin_mini
ver = '4.28.6'
orderSource = 'COMMON'



# 获取演出日期数据
def getSessionsDateDetail():
    HEADERS = {
     
    }
    url = requestUrl + "/cyy_gatewayapi/show/pub/v5/show/" + showId + "/sessions?src=" + src + "&ver=" + ver + "&source=FROM_QUICK_ORDER&isQueryShowBasicInfo=true"
    response = requests.get(url, headers=HEADERS)
    # print(response.json())
    return response.json()['data']

sessionsData = getSessionsDateDetail()
sessionData = sessionsData[sessionIndex]
# 获取演出详情数据
def getDetail():
    HEADERS = {
     
    }
    url = requestUrl + "/cyy_gatewayapi/show/pub/v5/show/" + showId + "/session/" + sessionData['bizShowSessionId'] + "/seat_plans?src=" + src + "&ver=" + ver + "&source=FROM_QUICK_ORDER"
    response = requests.get(url, headers=HEADERS)
    # print(response.json())
    return response.json()['data']['seatPlans']

seatPlans = getDetail()

# 确认订单获取用户身份信息
def getBuyerOrder():
    # shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    ticketItems = []
    for i in range(buyNum):
      ticketItems.append({
          'id':  contextJs.call('generateId')
      })

    items = [{
        'sku': {
            'qty': buyNum,
            'skuType': skuType,
            'ticketPrice': seatPlans[seatPlanIndex]['originalPrice'],
            'skuId': seatPlans[seatPlanIndex]['seatPlanId'],
            'ticketItems': ticketItems,
        },
        'spu': {
            'sessionId': sessionData['bizShowSessionId'],
            'showId': showId
        }
    }] 
    data = {
        'priorityId': '',
        'items': items,
        'src': src,
        'ver': ver,
        'orderSource': orderSource
    }
    
    url = requestUrl + "/cyy_gatewayapi/trade/buyer/order/v5/pre_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    if "data" in response.json() and response.json()["data"]:
        createOrder(items, response.json()['data'])
        return response.json()['data']
    else:
        getBuyerOrder()

# 创建订单
def createOrder(items, orderData):
    # shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    # print(items)
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    totalAmount = 0
    ticketItems = []
    ticketIndex = 0
    for i in range(buyNum):
      ticketItems.append({
        'id': items[0]['sku']['ticketItems'][ticketIndex]['id'],
        "audienceId": orderData['audiences'][ticketIndex]['id'] # 身份ID
      })
      ticketIndex = ticketIndex + 1

    items = [{
        'sku': {
            'qty': buyNum,
            'skuType': skuType,
            'ticketPrice': seatPlans[seatPlanIndex]['originalPrice'],
            'skuId': seatPlans[seatPlanIndex]['seatPlanId'],
            'ticketItems': ticketItems,
        },
        'spu': {
            'sessionId': sessionData['bizShowSessionId'],
            'showId': showId
        },
        "deliverMethod": orderData['supportDeliveries'][0]['name']
    }]
    priceItems = []
    for priceItem in orderData['priceItems']:
        totalAmount += priceItem['priceItemVal']
        priceItems.append({
            "applyTickets": [],
            "priceItemName": priceItem['priceItemName'],
            "priceItemVal": priceItem['priceItemVal'],
            "priceItemType": priceItem['priceItemType'],
            "priceItemSpecies": priceItem['priceItemSpecies'],
            "direction": priceItem['direction'],
            "priceDisplay": '￥' + str(priceItem['priceItemVal']),
        })
    data = {
        "src": src,
        "ver": ver,
        "addressParam": {},
        "locationParam": {
            "locationCityId": ""
        },
        "paymentParam": {
            "totalAmount": totalAmount,
            "payAmount": totalAmount
        },
        "priceItemParam": priceItems,
        "items": items,
        "priorityId": "",
        "many2OneAudience": {}
    }
    print(data)
    url = requestUrl + "/cyy_gatewayapi/trade/buyer/order/v5/create_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    if "data" in response.json() and response.json()['data']['orderId']:
        return response.json()['data']
    else:
        # 0.3 20次后当前网络访问次数过多。
        # 0.1 13次后当前网络访问次数过多。
        random_num = random.uniform(0.3, 0.4)
        time.sleep(0.5)
        createOrder(items, orderData)

# now = datetime.now()
# target_time = datetime(now.year, now.month, now.day, 15, 15)
# is_target_time = now.replace(microsecond=0) == target_time.replace(microsecond=0)
# is_target_time = False
# while not is_target_time:
#     now = datetime.now()
#     target_time = datetime(now.year, now.month, now.day, 15, 18)
#     is_target_time = now.replace(microsecond=0) == target_time.replace(microsecond=0)
#     time.sleep(0.5)
#     print('当前时间：', now)

getBuyerOrder()



# # 定义一个特定的日期时间
# dt = datetime.datetime(2024, 3, 21, 12, 20, 00)  # 2024年3月21日12:20:00
# # 将日期时间转换为时间戳（以秒为单位）
# setTimestamp = int(dt.timestamp())
# success = { 
#     'count': 0
# }
# while success['count'] < 1:
#     getBuyerOrder()
#     # print(setTimestamp)
#     # nowTime = datetime.datetime.now().timestamp()
#     # print(nowTime)
#     # print(seatPlans[3])
#     # print(seatPlans[4])
#     # if (nowTime == setTimestamp or nowTime > setTimestamp):
#     #     if (seatPlans[3]['canBuyCount'] > 0):
#     #             getCode(3)
#     #     if (seatPlans[4]['canBuyCount'] > 0):
#     #             getCode(4)

#     # time.sleep(5)
#     break
#     # print(success['count'])
#     # if (success['count'] > 1):
#     #     break

# 获取code（没用了）
# def getCode(plantIndex):
#     HEADERS = {
#         **comHeaders,
#         "Content-Type": "application/json"
#     }
#     ticketsData = []
#     operationsData = []
#     nums = 10000000

#     for i in range(buyNum):
#         nums2 = nums + 1
#         nums3 = nums2 + 1
#         nums = nums + 2
#         generateId = str(int(time.time())) + str(nums2)
#         id = str(int(time.time())) + str(nums3)
#         operationsData.append({
#             'id': id,
#             'snapshotId': '',
#             'ticketGenerateId': generateId
#         })
#         ticketsData.append({
#             'generateId': generateId,
#             'seatPlanId': seatPlans[plantIndex]['seatPlanId'],
#             'session': {
#                 'bizShowSessionId': sessionData['bizShowSessionId']
#             },
#             'show': {
#                 'showId': showId
#             }
#          })

#     filters = []
#     filters.append({
#         'id': sessionData['showId'],
#         'limitation': sessionData['showLimit'],
#         'limiterId': sessionData['showId'],
#         'type': 'purchaseShowLimiter'
#     })
#     filters.append({
#         'id': sessionData['bizShowSessionId'],
#         'limitation': sessionData['limitation'],
#         'limiterId': sessionData['bizShowSessionId'],
#         'type': 'purchaseSessionLimiter'
#     })
#     for plans in seatPlans:
#         plansData = {
#             'id': plans['seatPlanId'],
#             'limitation': plans['canBuyCount'],
#             'limiterId': plans['seatPlanId'],
#             'type': 'purchaseSeatPlanLimiter'
#         }
#         if (plans['seatPlanCategory'] == 'COMBO'):
#             plansData['type'] = 'fixedComboLimiter'
#         filters.append(plansData)

#     data = {
#         'bizCode': 'FHL_M',
#         'scene': {
#             'saleAssistantJson': {
#                 'deliverFee': -1,
#                 'deliverPriceItemId': '',
#                 'discounts': [{
#                     'id': 'comboDiscount',
#                     'level': 1,
#                     'type': 'comboDiscount',
#                 }],
#                 'filters': filters,
#                 'selectedSession': {
#                     'bizShowSessionId': sessionData['bizShowSessionId'],
#                     'ctSession': sessionData['ctSession'],
#                     'ctTag': sessionData.get('ctTag', ''),
#                     'sessionName': sessionData['sessionName'],
#                     'stdShowSessionId': sessionData['stdShowSessionId'],
#                     'supportSeatPicking': sessionData['supportSeatPicking'],
#                 },
#                 'selectedShow': {
#                     'seatPickType': sessionData['originalSeatPickType'],
#                     'showId': sessionData['showId'],
#                     'showName': sessionData['showName'],
#                     'stdShowId': sessionData['stdShowId']
#                 },
#                 'shoppingCart': {
#                     'currentSnapshotId': '',
#                     'isOpen': 'true',
#                     'operations': operationsData,
#                     'productSKUs': [],
#                     'tickets': ticketsData,
#                     '_combos': [],
#                     '_seatPlans': [{
#                         'originalPrice': seatPlans[plantIndex]['originalPrice'],
#                         'seatPlanId': seatPlans[plantIndex]['seatPlanId'],
#                         'seatPlanName': seatPlans[plantIndex]['seatPlanName'],
#                         'stdSeatPlanId': seatPlans[plantIndex]['stdSeatPlanId'],
#                     }],
#                     '_sessions': [{
#                         'bizShowSessionId': sessionData['bizShowSessionId'],
#                         'ctSession': sessionData['ctSession'],
#                         'ctTag': sessionData.get('ctTag', ''),
#                         'sessionName': sessionData['sessionName'],
#                         'stdShowSessionId': sessionData['stdShowSessionId'],
#                         'supportSeatPicking': sessionData['supportSeatPicking'],
#                     }],
#                     '_shows': [{
#                         'seatPickType': sessionData['originalSeatPickType'],
#                         'showId': sessionData['showId'],
#                         'showName': sessionData['showName'],
#                         'stdShowId': sessionData['stdShowId']
#                     }]
#                 },
#             }
#         },
#         'src': src,
#         'ver': ver,
#     }
#     url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/generate_code"
#     data = json.dumps(data, separators=(',', ':'))
#     response = session.post(url, headers=HEADERS, data=data)
#     # print(response.json())
#     wxaCode = response.json()['data']['wxaCode']
#     getShortCodesJSON(wxaCode)
#     return response.json()['data']['wxaCode']

# wxaCode = getCode()


# 获取订单code对应json （没用了）
# def getShortCodesJSON(wxaCode):
#     HEADERS = {
#         **comHeaders,
#         "Content-Type": "application/json"
#     }
#     url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/code/" + wxaCode + "?src=" + src + "&ver=" + ver
#     response = requests.get(url, headers=HEADERS)
#     getBuyerOrder(json.loads(response.json()['data']['param']))
#     return response.json()['data']['param']

# orderJSON = json.loads(getShortCodesJSON())



