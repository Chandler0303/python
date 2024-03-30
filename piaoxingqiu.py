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
comHeaders = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Sec-Ch-Ua-Platform': "Android",
    'Src':'H5',
    'Terminal-Src': 'H5',
    'Access-Token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNp8kMFOwzAQRP9lzznYseM4ORYVUakIqaIHTmgTr9VIcVw5DgKq_jtOU2hPHHc182Z3TuBxiofNYD3Uw9T3GUwjhWU-QdN9P3hDUMPj0_b9GTIYp2b1t1S5KlEzIpNzXci81MpyWcmkS86d72fRav-23qWNi-1-RpvZKGxutWDKCFU2jDFOUpf2arzJCqENitwqQ3iRMaORNXDOgD6PXaDXzqUMXnLFNeNaFFJcEC9HChj9vxhMaW0gjDcKqyr1Sxm_xkhu-XRpxlFoDzjE-7bSGff5GXxQGDs_QC2WKgd0V8D5BwAA__8.YnCjfYljrAAEZ-sQiWHmav_J5yA2hLTxiGlZLCscSNd2urtlFVftejpTH5MPHmlZxcE4rm7-nuSwFGr6VFSy190FNvahwVRuF8nvrcXSovIHsvXTf9gj_4Havuv1QGDmH7lCOGW25z6_0KBOuT_JTtDa8DJ4HecoLrYHpKndnNo'
}
showId = '65d9bc7b862ec60001ddd211' 
buyNum = 1
sessionIndex = 0
skuType = 'SINGLE' #'SINGLE_SKU'
success = { 
    'count': 0
}
src = 'H5'
ver = '4.2.1-20240322110808'
# 定义一个特定的日期时间
dt = datetime.datetime(2024, 3, 21, 12, 20, 00)  # 2024年3月21日12:20:00
# 将日期时间转换为时间戳（以秒为单位）
setTimestamp = int(dt.timestamp())


# 获取演出详情数据
def getSessionsDetail():
    HEADERS = {
     
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v5/show/" + showId + "/sessions?src=" + src + "&ver=" + ver + "&source=FROM_QUICK_ORDER&isQueryShowBasicInfo=true"
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    return response.json()['data']

sessionsData = getSessionsDetail()
sessionData = sessionsData[sessionIndex]

# 获取演出详情数据
def getSessionDetail():
    HEADERS = {
     
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v5/show/" + showId + "/session/" + sessionData['bizShowSessionId'] + "/seat_plans?src=" + src + "&ver=" + ver + "&source=FROM_QUICK_ORDER"
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    return response.json()['data']['seatPlans']

seatPlans = getSessionDetail()


# 获取code
def getCode(plantIndex):
    HEADERS = {
        **comHeaders,
        "Content-Type": "application/json"
    }
    ticketsData = []
    operationsData = []
    nums = 10000000

    for i in range(buyNum):
        nums2 = nums + 1
        nums3 = nums2 + 1
        nums = nums + 2
        generateId = str(int(time.time())) + str(nums2)
        id = str(int(time.time())) + str(nums3)
        operationsData.append({
            'id': id,
            'snapshotId': '',
            'ticketGenerateId': generateId
        })
        ticketsData.append({
            'generateId': generateId,
            'seatPlanId': seatPlans[plantIndex]['seatPlanId'],
            'session': {
                'bizShowSessionId': sessionData['bizShowSessionId']
            },
            'show': {
                'showId': showId
            }
         })

    filters = []
    filters.append({
        'id': sessionData['showId'],
        'limitation': sessionData['showLimit'],
        'limiterId': sessionData['showId'],
        'type': 'purchaseShowLimiter'
    })
    filters.append({
        'id': sessionData['bizShowSessionId'],
        'limitation': sessionData['limitation'],
        'limiterId': sessionData['bizShowSessionId'],
        'type': 'purchaseSessionLimiter'
    })
    for plans in seatPlans:
        plansData = {
            'id': plans['seatPlanId'],
            'limitation': plans['canBuyCount'],
            'limiterId': plans['seatPlanId'],
            'type': 'purchaseSeatPlanLimiter'
        }
        if (plans['seatPlanCategory'] == 'COMBO'):
            plansData['type'] = 'fixedComboLimiter'
        filters.append(plansData)

    data = {
        'bizCode': 'FHL_M',
        'scene': {
            'saleAssistantJson': {
                'deliverFee': -1,
                'deliverPriceItemId': '',
                'discounts': [{
                    'id': 'comboDiscount',
                    'level': 1,
                    'type': 'comboDiscount',
                }],
                'filters': filters,
                'selectedSession': {
                    'bizShowSessionId': sessionData['bizShowSessionId'],
                    'ctSession': sessionData['ctSession'],
                    'ctTag': sessionData.get('ctTag', ''),
                    'sessionName': sessionData['sessionName'],
                    'stdShowSessionId': sessionData['stdShowSessionId'],
                    'supportSeatPicking': sessionData['supportSeatPicking'],
                },
                'selectedShow': {
                    'seatPickType': sessionData['originalSeatPickType'],
                    'showId': sessionData['showId'],
                    'showName': sessionData['showName'],
                    'stdShowId': sessionData['stdShowId']
                },
                'shoppingCart': {
                    'currentSnapshotId': '',
                    'isOpen': 'true',
                    'operations': operationsData,
                    'productSKUs': [],
                    'tickets': ticketsData,
                    '_combos': [],
                    '_seatPlans': [{
                        'originalPrice': seatPlans[plantIndex]['originalPrice'],
                        'seatPlanId': seatPlans[plantIndex]['seatPlanId'],
                        'seatPlanName': seatPlans[plantIndex]['seatPlanName'],
                        'stdSeatPlanId': seatPlans[plantIndex]['stdSeatPlanId'],
                    }],
                    '_sessions': [{
                        'bizShowSessionId': sessionData['bizShowSessionId'],
                        'ctSession': sessionData['ctSession'],
                        'ctTag': sessionData.get('ctTag', ''),
                        'sessionName': sessionData['sessionName'],
                        'stdShowSessionId': sessionData['stdShowSessionId'],
                        'supportSeatPicking': sessionData['supportSeatPicking'],
                    }],
                    '_shows': [{
                        'seatPickType': sessionData['originalSeatPickType'],
                        'showId': sessionData['showId'],
                        'showName': sessionData['showName'],
                        'stdShowId': sessionData['stdShowId']
                    }]
                },
            }
        },
        'src': src,
        'ver': ver,
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/generate_code"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    # print(response.json())
    wxaCode = response.json()['data']['wxaCode']
    getShortCodesJSON(wxaCode)
    return response.json()['data']['wxaCode']

# wxaCode = getCode()


# 获取订单code对应json
def getShortCodesJSON(wxaCode):
    HEADERS = {
        **comHeaders,
        "Content-Type": "application/json"
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/code/" + wxaCode + "?src=" + src + "&ver=" + ver
    response = requests.get(url, headers=HEADERS)
    getBuyerOrder(json.loads(response.json()['data']['param']))
    return response.json()['data']['param']

# orderJSON = json.loads(getShortCodesJSON())


# 确认订单获取用户身份信息
def getBuyerOrder(orderJSON):
    # print(orderJSON['saleAssistantJson']['shoppingCart'])
    shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    ticketItems = []
    ticketIndex = 0
    for ticket in shoppingCart['tickets']:
      ticketItems.append({
          'id': ticket['generateId']
      })
      ticketIndex = ticketIndex + 1

    items = [{
        'sku': {
            'qty': buyNum,
            'skuType': skuType,
            'ticketPrice': shoppingCart['_seatPlans'][0]['originalPrice'],
            'skuId': ticket['seatPlanId'],
            'ticketItems': ticketItems,
        },
        'spu': {
            'sessionId': ticket['session']['bizShowSessionId'],
            'showId': ticket['show']['showId']
        }
    }] 
    data = {
        'priorityId': '',
        'items': items,
        'src': src,
        'ver': ver
    }
    
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v5/pre_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    if "data" in response.json() and response.json()["data"]:
        createOrder(orderJSON, response.json()['data'])
        return response.json()['data']
    else:
        getBuyerOrder(orderJSON)

# orderData = getBuyerOrder()

# 创建订单
def createOrder(orderJSON, orderData):
    shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    totalAmount = 0
    ticketItems = []
    ticketIndex = 0
    for ticket in shoppingCart['tickets']:
      ticketItems.append({
        'id': ticket['generateId'],
        "audienceId": orderData['audiences'][ticketIndex]['id']
      })
      ticketIndex = ticketIndex + 1

    items = [{
        'sku': {
            'qty': buyNum,
            'skuType': skuType,
            'ticketPrice': shoppingCart['_seatPlans'][0]['originalPrice'],
            'skuId': ticket['seatPlanId'],
            'ticketItems': ticketItems,
        },
        'spu': {
            'sessionId': ticket['session']['bizShowSessionId'],
            'showId': ticket['show']['showId']
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
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v5/create_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    if "data" in response.json() and response.json()['data']['orderId']:
        return response.json()['data']
    # else:
    #     createOrder(orderJSON, orderData)

# createOrder()

while success['count'] < 1:
    getCode(3)
    # print(setTimestamp)
    # nowTime = datetime.datetime.now().timestamp()
    # print(nowTime)
    # print(seatPlans[3])
    # print(seatPlans[4])
    # if (nowTime == setTimestamp or nowTime > setTimestamp):
    #     if (seatPlans[3]['canBuyCount'] > 0):
    #             getCode(3)
    #     if (seatPlans[4]['canBuyCount'] > 0):
    #             getCode(4)

    time.sleep(0.1)
    break
    # print(success['count'])
    # if (success['count'] > 1):
    #     break


