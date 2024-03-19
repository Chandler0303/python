from dis import code_info
from multiprocessing import context
from pickle import TRUE
from xmlrpc.client import Boolean
import requests
import json
import execjs
from urllib.parse import quote
import time

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


contextJs = execjs.compile(js_from_file('./index.js'))
session = requests.session()
comHeaders = {
    'Access-Token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNp8kEtPwzAQhP_LnnPwI340x6IikEBIFT1wQk68ViPFduU4CKj633GaQnviuKuZb3bnCNFMef8YXIQmTMNQwTRiWuYjtP33XbQIDdw_PL0_QwXj1K7_lpJJZTRBtIxqUTOlpaP1qi664tzGYRatd2-bbdn43O1mtJ2N3DGnOZGWS9USQijWWrmL8SoTXFvDmZMWzVlGrDakhVMF-HnoE772vmRQRcWKK8UpF-KMeDlgMjn-izElrUto8pVClOC_lPFrzOiXT5dmPKZub0K-bauccZtfwQemsY8BGrZUGYy_AE4_AAAA__8.huotUEDJqu_KYltlaf_ydTVUcrWRscpnMNlk6TAJs0XPIHY1oToBMt2qffdrUG784qFuqf8RZ7vZs8s2yipoJzqkmnVd4jatowKcJ2tS-2EcWENJidkNE3ziSPdaZsNFAqYAIgmeSrEbxi9lp7xV0NtwPqapwLlUm9CU9SP458s'
}
showId = '65d83d1d19b6c7000161e2e9'
plantIndex = 2
skuType = 'SINGLE' #'SINGLE_SKU'



# 获取演出详情数据
def getSessionsDetail():
    HEADERS = {
     
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v5/show/" + showId + "/sessions?src=WEB&ver=4.1.2-20240305183007&source=FROM_QUICK_ORDER&isQueryShowBasicInfo=true"
    response = requests.get(url, headers=HEADERS)
    return response.json()['data']

sessionsData = getSessionsDetail()
sessionData = sessionsData[0]

# 获取演出详情数据
def getSessionDetail():
    HEADERS = {
     
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v5/show/" + showId + "/session/" + sessionData['bizShowSessionId'] + "/seat_plans?src=H5&ver=4.1.2-20240305183007&source=FROM_QUICK_ORDER"
    response = requests.get(url, headers=HEADERS)
    return response.json()['data']['seatPlans']

seatPlans = getSessionDetail()


# 获取code
def getCode():
    HEADERS = {
        **comHeaders,
        "Content-Type": "application/json"
    }
    generateId = str(int(time.time())) + '100000001'
    id = str(int(time.time())) + '100000002'
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
      filters.append({
        'id': plans['seatPlanId'],
        'limitation': plans['canBuyCount'],
        'limiterId': plans['seatPlanId'],
        'type': 'purchaseSeatPlanLimiter'
      })

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
                    'operations': [{
                        'id': id,
                        'snapshotId': '',
                        'ticketGenerateId': generateId
                    }],
                    'productSKUs': [],
                    'tickets': [{
                        'generateId': generateId,
                        'seatPlanId': seatPlans[plantIndex]['seatPlanId'],
                        'session': {
                            'bizShowSessionId': sessionData['bizShowSessionId']
                        },
                        'show': {
                            'showId': showId
                        }
                    }],
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
        'src': 'H5',
        'ver': '4.1.2-20240305183007',
    }
    # print(data)
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/generate_code"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    # print(response.json())
    return response.json()['data']['wxaCode']

wxaCode = getCode()


# 获取订单code对应json
def getShortCodesJSON():
    HEADERS = {
        **comHeaders,
        "Content-Type": "application/json"
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/home/pub/v3/wxapps/short_codes/code/" + wxaCode + "?src=H5&ver=4.1.2-20240305183007"
    response = requests.get(url, headers=HEADERS)
    return response.json()['data']['param']

orderJSON = json.loads(getShortCodesJSON())









# 确认订单获取用户身份信息
def getBuyerOrder():
    print(orderJSON['saleAssistantJson']['shoppingCart'])
    shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    items = []
    for ticket in shoppingCart['tickets']:
      items.append({
        'sku': {
            'qty': 1,
            'skuType': skuType,
            'ticketPrice': shoppingCart['_seatPlans'][0]['originalPrice'],
            'skuId': ticket['seatPlanId'],
            'ticketItems': [{
                'id': ticket['generateId']
            }],
        },
        'spu': {
            'sessionId': ticket['session']['bizShowSessionId'],
            'showId': ticket['show']['showId']
        }
    }) 
    data = {
        'priorityId': '',
        'items': items,
        'src': 'H5',
        'ver': '4.1.2-20240305183007'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v5/pre_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()['data']

orderData = getBuyerOrder()

# 创建订单
def createOrder():
    shoppingCart = orderJSON['saleAssistantJson']['shoppingCart']
    HEADERS = {
        "Content-Type": "application/json",
        **comHeaders,
    }
    totalAmount = 0
    items = []
    for ticket in shoppingCart['tickets']:
      items.append({
        'sku': {
            'qty': 1,
            'skuType': skuType,
            'ticketPrice': shoppingCart['_seatPlans'][0]['originalPrice'],
            'skuId': ticket['seatPlanId'],
            'ticketItems': [{
                'id': ticket['generateId'],
                "audienceId": orderData['audiences'][0]['id']
            }],
        },
        'spu': {
            'sessionId': ticket['session']['bizShowSessionId'],
            'showId': ticket['show']['showId']
        },
        "deliverMethod": orderData['supportDeliveries'][0]['name']
    })
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
            "priceDisplay": '￥' + priceItem['priceItemName'],
        })
    data = {
        "src": "H5",
        "ver": "4.1.2-20240305183007",
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
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v5/create_order"
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()['data']

createOrder()

