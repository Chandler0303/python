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
    HEADERS = {
      'Cookie': 'cna=t85lHu+Zii4CAXFYDeFVJB7e; _samesite_flag_=true; cookie2=19e27634e26076668d399bca3791b424; t=16a7e85eccd3953587ae46ed1da2f6d7; _tb_token_=73018b3e19ebe; _hvn_login=18; munb=2212933181550; csg=5cf42ebd; dm_nickname=%E9%BA%A6%E5%AD%902yhqU; usercode=183145203; havanaId=2212933181550; mtop_partitioned_detect=1; _m_h5_tk=341c2512be997f0720c34fdac07be3db_1709539302131; _m_h5_tk_enc=6afb6fa1b97a10854c78f0d26e87f344; xlly_s=1; tfstk=eqj6XHqHgfc_Sf0iO5wFFiMC2aKfl1Zzlx9AEtnZHhKOcw1lGFyG7tdflBBcgCow_6Mf96_wkiRVc-tGYNo2_5xfH_-ba7rz4OXMxnFzaur_rS-0qS-WiuWGIvHsM87L4mg11WjHPuc-e2XzhmmqmK9b5BcjcmsBB7ORCB9HKM965QLpOmBNAdT6wOIPe0RSNo0joCnXdQyQdq00XAPqr7BjlSY9Kpy8dJgVKFpHdQyQdq0DWpvUeJwIu9f..; isg=BDIyaTbqg6jymL-vzMwfEYr8g3gUwzZd-AK1cPwLXuXQj9KJ5FOGbTj9eS0z5K71',
      "Sec-Ch-Ua-Platform": "Android",
      "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }
    url = "https://mtop.damai.cn/h5/mtop.damai.item.detail.getdetail/1.0/?jsv=2.7.2&appKey=12574478&t=1709535934032&sign=bd07d2c22e2bdc5325e8da9f4c65c849&api=mtop.damai.item.detail.getdetail&v=1.0&H5Request=true&type=json&timeout=10000&dataType=json&valueType=string&forceAntiCreep=true&AntiCreep=true&useH5=true&data=%7B%22itemId%22%3A%22766026573586%22%2C%22platform%22%3A%228%22%2C%22comboChannel%22%3A%222%22%2C%22dmChannel%22%3A%22damai%40damaih5_h5%22%7D"
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    return response.json()

getList()



