from ast import Str
import requests
import json
import execjs
import time

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

    
contextJs = execjs.compile(js_from_file('./maoyan.js'))
# contextJs.call('gen_token', '123456')
# print(contextJs)
baseUrl = "https://show.maoyan.com" # https://show.maoyan.com https://wx.maoyan.com
session = requests.session()
showId = '398452'
optimus_risk_level = '71'
optimus_code = '10'
uuid = 'akc28ygmpykrlogilh446065kw75nge8qixbkvdnwatoaku8zp6g40jqq9xkmg7v'
sellChannel = '13'
cityId = '10'
token = 'AgGTHzikgrmQlQ7nNg8Htr7U1LE_Bx8LFDzV-MPDoZqlnrR8CYyj4HdrZW-mkOVI0S43DSX14g8hOwAAAAAKHwAAuD70AIqjIPrGjSUdIOknFe1bLQ9CNZfpn0Iw1fxB8pp42wDWk3v_KHFQGxMI7mRH'
csecplatform = '4'

# 获取演出日期数据
def getShowList():
    HEADERS = {
      'Cookie': '_lxsdk_cuid=18e65447c5b4-00fe610573fea9-26001851-1fa400-18e65447c5cc8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1711095978; ci=30%2C%E6%B7%B1%E5%9C%B3; featrues=[object Object]; com.sankuai.show.mmh5.static_strategy=; com.sankuai.show.mmh5.static_random=; WEBDFPID=8zvx556z0ww85500zxuu2388x5v8uw5881v3455w56897958v61u5988-2026455993641-1711095992903EWMMIMWfd79fef3d01d5e9aadc18ccd4d0c95072956; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1711162667; selectci=; _lxsdk=E6ED2800E82511EEA69CCD18DF7754BC701C3AC88A32460D84BA5F3D2CCCC34E; token=AgGTHzikgrmQlQ7nNg8Htr7U1LE_Bx8LFDzV-MPDoZqlnrR8CYyj4HdrZW-mkOVI0S43DSX14g8hOwAAAAAKHwAAuD70AIqjIPrGjSUdIOknFe1bLQ9CNZfpn0Iw1fxB8pp42wDWk3v_KHFQGxMI7mRH; com.sankuai.show.order.static_strategy=; com.sankuai.show.order.static_random=; _lx_utm=utm_source%3Dwxmyshow; _lxsdk_s=18e7337b6bd-c5f-daf-8f1%7C%7C19',
      "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }
    url = baseUrl + "/maoyansh/myshow/ajax/v2/performance/" + showId + "/shows/0?performanceId=" + showId + "&optimus_risk_level=" + optimus_risk_level + "&optimus_code=" + optimus_code + "&uuid=" + uuid + "&sellChannel=" + sellChannel + "&cityId=" + cityId + "&token=" + token + "&yodaReady=h5&csecplatform=" + csecplatform + "&csecversion=2.4.0"
    response = requests.get(url, headers=HEADERS)
    return response.json()['data']

showData = getShowList()[0]
print('----------')
print(showData)
# 获取演出日期数据
def getShowTicketsList():
    HEADERS = {
      'Cookie': '_lxsdk_cuid=18e65447c5b4-00fe610573fea9-26001851-1fa400-18e65447c5cc8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1711095978; ci=30%2C%E6%B7%B1%E5%9C%B3; featrues=[object Object]; com.sankuai.show.mmh5.static_strategy=; com.sankuai.show.mmh5.static_random=; WEBDFPID=8zvx556z0ww85500zxuu2388x5v8uw5881v3455w56897958v61u5988-2026455993641-1711095992903EWMMIMWfd79fef3d01d5e9aadc18ccd4d0c95072956; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1711162667; selectci=; _lxsdk=E6ED2800E82511EEA69CCD18DF7754BC701C3AC88A32460D84BA5F3D2CCCC34E; token=AgGTHzikgrmQlQ7nNg8Htr7U1LE_Bx8LFDzV-MPDoZqlnrR8CYyj4HdrZW-mkOVI0S43DSX14g8hOwAAAAAKHwAAuD70AIqjIPrGjSUdIOknFe1bLQ9CNZfpn0Iw1fxB8pp42wDWk3v_KHFQGxMI7mRH; com.sankuai.show.order.static_strategy=; com.sankuai.show.order.static_random=; _lx_utm=utm_source%3Dwxmyshow; _lxsdk_s=18e7337b6bd-c5f-daf-8f1%7C%7C19',
      "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }
    url = baseUrl + "/maoyansh/myshow/ajax/v2/show/" + str(showData['showId']) + "/tickets?performanceId=" + showId + "&optimus_risk_level=" + optimus_risk_level + "&optimus_code=" + optimus_code + "&uuid=" + uuid + "&sellChannel=" + sellChannel + "&cityId=" + cityId + "&token=" + token + "&yodaReady=h5&csecplatform=" + csecplatform + "&csecversion=2.4.0"
    response = requests.get(url, headers=HEADERS)
    # print(response.json())
    return response.json()['data']

ticketsData = getShowTicketsList()[1]
print('----------')
print(ticketsData)
# 创建订单
def createOrder():
    HEADERS = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': '_lxsdk_cuid=18e65447c5b4-00fe610573fea9-26001851-1fa400-18e65447c5cc8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1711095978; ci=30%2C%E6%B7%B1%E5%9C%B3; featrues=[object Object]; com.sankuai.show.mmh5.static_strategy=; com.sankuai.show.mmh5.static_random=; WEBDFPID=8zvx556z0ww85500zxuu2388x5v8uw5881v3455w56897958v61u5988-2026455993641-1711095992903EWMMIMWfd79fef3d01d5e9aadc18ccd4d0c95072956; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1711162667; selectci=; _lxsdk=E6ED2800E82511EEA69CCD18DF7754BC701C3AC88A32460D84BA5F3D2CCCC34E; token=AgGTHzikgrmQlQ7nNg8Htr7U1LE_Bx8LFDzV-MPDoZqlnrR8CYyj4HdrZW-mkOVI0S43DSX14g8hOwAAAAAKHwAAuD70AIqjIPrGjSUdIOknFe1bLQ9CNZfpn0Iw1fxB8pp42wDWk3v_KHFQGxMI7mRH; com.sankuai.show.order.static_strategy=; com.sankuai.show.order.static_random=; _lx_utm=utm_source%3Dwxmyshow; _lxsdk_s=18e7337b6bd-c5f-daf-8f1%7C%7C19',
      "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }
    data = {
      'sellChannel': 1,
      'dpCityId': 10,
      'salesPlanId': ticketsData['showTicketClassId'],
      'showId': showId,
      'performanceId': ticketsData['performanceId'],
      'tpId': ticketsData['salesPlanVO']['tpId'],
      'salesPlanSupplyPrice': ticketsData['salesPlanVO']['supplierPrice'],
      'salesPlanSellPrice': ticketsData['sellPrice'],
      'salesPlanCount': 1,
      'totalPrice': 240,
      'fetchTicketWayId': 5731415,
      'userMobileNo': 17674197035,
      'recipientMobileAreaCode': 86,
      'clientPlatform': 1,
      'clientVersion': '1.0.0',
      'needRealName': True,
      'realNameUserVOList': '[{"id":37895193,"idType":1,"idNumber":"431028199811022018","userName":"侯玲风","idTypeName":"身份证","status":1,"regionName":"","regionShow":False,"regionTitle":'',"faceCheckOrderNo":'',"unUsableReason":0,"faceCheckStatus":1,"lastFaceCheckTime":'',"prefill":False,"default": False,"originStatus":1,"isSelected":True}]',
      'recipientName': '侯玲风',
      'recipientMobile': '17674197035',
      'dpId': uuid,
      'uuid': uuid,
      '_token': 'eJylkV1PgzAUhv9LL7yxGS1fxSWLYZsJ4MaIsi+MMQwZ27B8lCow43+3aHS78sakSc953+ec05O+A2Y/gz5GMkIIgreYgT7APdTTAQS8Eg7BWFF03dBV+QqC6EwjhkyICsGGLcag/6BiGV5h9bET7kR+Ek6RrIrTEbYAwI7zoupLUrXL6x4N8zbMelFOpbKspSjPtntGr185faryVxbFg7qhbYdebFlO/TA5CR0kCnic8V9RvP+v/t+Q9I/+Yg3qd2soWIEGIWIglhHUFKOz0s4Sd3iOwOHc92fuiYRjeyEyBNFXJHj+UzcVHyGsap9kIoqdxm2O6bLem3NzOiLFrUlpJY/aqvC1oZXcbNvt5L52shdtUmh8Rt0mTt+W80tn5E6W6WJVMslqN8N9mZeB5Xpp6hiEt9pKqshttLCb1IpeyoCH1ijB9UZZB4fcndraAenMCQqWtOy53XjZ3Ak86t2ZyvHmcsKGOuNoxXldr83BAHx8Av4xuuo='
    }
    url = baseUrl + "/maoyansh/myshow/ajax/order?optimus_risk_level=" + optimus_risk_level + "&optimus_code=" + optimus_code + "&uuid=" + uuid + "&sellChannel=" + sellChannel + "&cityId=" + cityId + "&token=" + token + "&yodaReady=h5&csecplatform=" + csecplatform + "&csecversion=2.4.0"
    # data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=HEADERS, data=data)
    print(response.json())
    return response.json()

# createOrder()



