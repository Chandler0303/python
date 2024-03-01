from dis import code_info
from multiprocessing import context
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






# 获取首页列表数据
def getList():
    requestData = {
        "jsv": "2.7.2",
        "appKey": "12574478",
        "t": 1709263814680,
        "sign": "0df6570cab3905b986ce6aa500cc02e3",
        "api": "mtop.damai.wireless.search.search",
        "v": "1.0",
        "H5Request": "true",
        "type": "originaljson",
        "timeout": 10000,
        "dataType": "json",
        "valueType": 'original',
        "forceAntiCreep": 'true',
        "AntiCreep": 'true',
        "useH5": 'true',
        "data": {"cityId":"0","distanceCityId":"0","pageIndex":1,"pageSize":20,"categoryId":0,"dateType":0,"option":31,"sourceType":21,"returnItemOption":4,"platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}

    }
    # HEADERS = contextJs.call('getHeaders', {
    #     **comHeaderParams,
    #     'timeUuid': contextJs.call('timeUuid', 32),
    #     "url": "/wap/activity/list",
    #     "accessToken": tokenData['accessToken']
    # }, requestData)
    # print(HEADERS)
    url = "https://mtop.damai.cn/h5/mtop.damai.wireless.search.search/1.0/"
    # data = requestData
    # data = json.dumps(data, separators=(',', ':'))
    response = session.get(url, headers={}, data=requestData)
    print(response.json())
    return response.json()

getList()



