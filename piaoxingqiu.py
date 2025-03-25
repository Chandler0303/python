import requests
import json
import execjs
import time
import datetime
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
    'Access-Token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNp8UcGOgjAQ_Zc5cygFS-GGrEYTjYaVgydS7BBJEEgpm3WN_74tkpXTHt_Me2_ezDygFYO-bpuyhagZ6tqBoUf1wg8oqp-klQgRrDe7fA8O9EOx_CsyygLBCaKkLl_4NOCsdP3QNzyjTNvakpbZeZWayk1fMmstrdArack9wqTHgoIQ4qLPg3ISvmkLj0vh0ZJJFCONSC5IAc-Rd-hQCd3-yxXGUt87E8Q1EVBdrqLR83W_UPVV20BEHeiE0pUeETAjxO-uUniqblYe-JSHLll4LAwduCgUet4iPpta_b3XeJtOlMTb_LzNk90h-8jHU-THLE028ecqP-7i0_qQ7l-T5iOMv8nZYG1Xe7-lEXacxc9fAAAA__8.ONqc5KIeNPAZk27b7x8c10aKZAjwqWRGwZyklvzSjdNvqWQwigE317FR_HXBQ-CulQ0g8_5JQHZ5HWgv8cIEBvH9WNUlnnoaZX86jI-6Ved4VVHB90ORl7GMD5c2jl0dOPRZr1LmoVqQbZ3NaNQYRu5CPfuyEIilag6P2Cl7vxw'
}
showId = '67b6dc721564910001a5ef4b'  # 演出ID
buyNum = 1
sessionIndex = 0 # 某一天的session数据下标，默认第一项
seatPlanIndex =  2 # 座位数据下标，默认第一项
skuType = 'SINGLE' #'SINGLE_SKU'
src = 'weixin_mini' # 'H5' weixin_mini
ver = '4.28.6'
orderSource = 'COMMON'
# 定义一个特定的日期时间
dt = datetime.datetime(2024, 3, 21, 12, 20, 00)  # 2024年3月21日12:20:00
# 将日期时间转换为时间戳（以秒为单位）
setTimestamp = int(dt.timestamp())


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
        random_num = random.uniform(0.1, 0.35)
        time.sleep(random_num )
        createOrder(items, orderData)


getBuyerOrder()



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



