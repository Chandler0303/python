import requests
import json
import execjs
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

# 获取演出票价
def getDetail():
    HEADERS = {
        "Host": "acs.m.taobao.com",
        "x-app-conf-v": "0",
        "x-bx-version": "6.6.240602",
        "x-pv": "6.3",
        "User-Agent": "MTOPSDK%2F2.5.3.42%20%28iOS%3B18.3.1%3BApple%3BiPhone14%2C4%29%20DeviceType%28Phone%29",
        "x-page-name": "TBHomeViewController",
        "f-refer": "mtop",
        "x-sgext": "JBJr2AL310jDE4wuJbid9the6Fr7We9Y4Fz7We1I%2B1rvX%2Bld7l%2FpXe5I6FvoW%2Bhb6FvoW%2Bhb6FvoW%2Ftb%2B1v7W%2BhI6FvoW%2Ftb%2B1r7Wvta%2B1r7Wvta%2B1v7W%2Bhb6Fv7WbwK%2B1j7W%2FtY%2BxGbB6lI%2BEvpUvhL6VP7D4c%2BjiWKPeklgD60IuU06ViHKokqmRuJKoEqmS6ZKpkqsiqaBJkqmSqZKpsimTTpXYdbhw%3D%3D",
        "x-app-ver": "8.10.5",
        "x-utdid": "ZFOAsLsW%2FcYDALeRW6qtKgUV",
        "x-uid": "2212933181550",
        "x-devid": "AgF8ygzpESxeiQgiMLYwue8Qa8PxfUZVeACKQL3eksnu",
        "x-cmd-v": "0%7C0",
        "a-orange-q": "appKey%3D23782110%26appVersion%3D8.10.5%26clientAppIndexVersion%3D1120250214134501356%26clientVersionIndexVersion%3D0",
        "Connection": "keep-alive",
        "x-falco-id": "895C66B982574716B7A80C2C722BBBFE",
        "x-sign": "izKMHp006xAAJhbFxKSxyA9alXe3VhbGHc4T8FoSpuEeqNbQQbKlADm4Z%2B9O9sjzAIOEXVkPRqrFhCLKRvdacpeikGYW1hbGFtYWxh",
        "x-appkey": "23782110",
        "x-sid": "14e0fdd294aa803f4b932f8b6741e408",
        "x-features": "11",
        "x-umt": "huwBZXdLPGL35xKVgw3jUWRZKbT8lQbN",
        "x-mini-wua": "iggRqLTsr%2FbkcYBbgh5UUfgxm9U5maoqhSNy1MYrRp4ElyX%2FgPuvT6tuRih78FQGX3KdGXJH5xbFQNaD3poFpmU4rUOaU4H%2Fcfjty3lhmOlanvhQUtAfkwQNyVTN0fUG8RKyfpikiISLco7cC5Jk0QyLyPPD0VZHsVV6e10V1ISUbG7cwW1nSI27bHU40vdvIgQM%3D",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "c-launch-info": "(null),0,1741664175988.111,0,1",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "x-ttid": "cn.damai.iphone%40damai_iphone_8.10.5",
        "x-nq": "5G",
        "x-t": "1741671142",
        "Accept-Encoding": "gzip, deflate, br"
    }
    # 不会随时间戳变化
    cookies = {
        "isg": "BAQE4v4gPzgy4YuIy9-6wpOq34b2HSiHMaGY-B6lKU-SSaATRi3FFonqjWeRymDf",
        "tfstk": "f5FtXBToMpdVULB01P6HimosY-ctB5Ua8lzWimmMhkELmoRihP4jljEQmNoglGrYMDiUjhc_SqZYuDbZiRXqMxEmxS2imO5AkDU2IZlcQndxvuyMii7ZljhatRAmjGlYluDAqgflZPzZajslq9c_UsljlsmXJd9BSjlfqMvHGA5-guoUVb8YRw3mlqt_cxtCJ4utGCMX1ptIYqGjcoMjADg-5VOX6j_-m6oeM8Onn4Vc28RXG5G-B4dxA2ua9VHtV_opGRVKWAn7W544rbuUlzMbiMAadPZTFYN1aLk_5leSF5194DDP4PPuwEKHq03DBwFX3Kks-3AlBGY2YUZrJ0bhnKJqB5gKqwQp3Kks82nl8rp23AF1.",
        "x5sec": "7b22733b32223a2238376561366432626462333039373736222c22617365727665723b33223a22307c434c2f5276723447454f3265747649434967706a5958427a62476c6b5a5859794d4d4765772f5147227d",
        "cna": "S/M5INqkuD8CAXBhUhTk2XMS",
    }
    # url = "https://acs.m.taobao.com/gw/mtop.alibaba.detail.subpage.getdetail/2.0?t=1741662421&rnd=9CD731FEDC727AFF629559D70BFE0CC6&data=%7B%22scenario%22%3A%22itemsku%22%2C%22itemId%22%3A%22893551409165%22%2C%22dataId%22%3A%22224252144%22%2C%22dataType%22%3A%222%22%2C%22cityCode%22%3A%22906%22%2C%22bizCode%22%3A%22ali.china.damai%22%2C%22exParams%22%3A%22%7B%5C%22itemId%5C%22%3A%5C%22893551409165%5C%22%2C%5C%22scenario%5C%22%3A%5C%22itemsku%5C%22%2C%5C%22bizCode%5C%22%3A%5C%22ali.china.damai%5C%22%2C%5C%22dataType%5C%22%3A%5C%222%5C%22%2C%5C%22dataId%5C%22%3A%5C%22224252144%5C%22%7D%22%2C%22comboChannel%22%3A%221%22%7D"
    url = "https://acs.m.taobao.com/gw/mtop.damai.item.detail.getdetail/1.0?t=1741671142&rnd=E0F025F9CB577AB966CFF583C855FB16&data=%7B%22comboChannel%22%3A%221%22%2C%22lng%22%3A%22113.940005%22%2C%22lat%22%3A%2222.574864%22%2C%22itemId%22%3A%22893551409165%22%2C%22cityCode%22%3A%22906%22%7D"
    response = requests.get(url, headers=HEADERS, cookies=cookies)
    print(response.json())
    return response.json()

getDetail()



# 会动态变化
# headers = {
#   "x-sgext": "JBJ%2BzBbiw13XBpg7Ma2J48xL%2FE%2FvTPtM%2F03vSvld70%2F7Sv1I%2Bkz%2BR%2FRd%2FE7%2BSPxO%2FE38TvxO%2FE78Tu9O707vTvxd%2FE78Tu9O70%2FvT%2B9P70%2FvT%2B9P707vTvxO%2FE7vTKgf703vTu9N7wSPEr1d7F7%2BGuxe%2Fh3vSJNP6kzqTepJ6kfqHeoa6k%2F8WP1IkxqTK5ownij9MJQroDfxIf1Nkz%2BdP40OnT%2BVP407jT%2BNP6Y%2FjhGNP40%2FjT%2BPN40h%2FUiTTpM%3D",
#   "x-falco-id": "78A314A8D13A41E782ACAB344AD8293F",
#   "x-sign": "izKMHp006xAALXGgT1I05kEHejfDfXGteqV0mz15wYp5w7G7JtnCa17TAIQpna%2BYZ%2BjjNj5kIcGi70WhIZw9GfDJ9w1xrXGtcZ1xrX",
#   "x-mini-wua": "i5gQigrZoYFwILj%2B1g4uL0i0O1Hhw9dk06bf9IHzTDSnY%2BF1DkECl2CpL6GppwQAduVgp%2B58aYXXxMKlZ3TRPM9%2BP5dAcpGgcjiOttBXayhbzHpwY70%2F5NiNTt3pVXAejLDRfSwjWBNA%2B8A27vgaqEzU5te2s557%2Fyu2fndbUx3hitoCob4J6WPmquB4xHMpwo9o%3D",
#   "c-launch-info": "(null),0,1741662421002.182,0,1",
#   "x-t": "1741662421",
# }



# headers = {
#   "x-sgext": "JBJr2AL310jDE4wuJbid9the6Fr7We9Y4Fz7We1I%2B1rvX%2Bld7l%2FpXe5I6FvoW%2Bhb6FvoW%2Bhb6FvoW%2Ftb%2B1v7W%2BhI6FvoW%2Ftb%2B1r7Wvta%2B1r7Wvta%2B1v7W%2Bhb6Fv7WbwK%2B1j7W%2FtY%2BxGbB6lI%2BEvpUvhL6VP7D4c%2BjiWKPeklgD60IuU06ViHKokqmRuJKoEqmS6ZKpkqsiqaBJkqmSqZKpsimTTpXYdbhw%3D%3D",
#   "x-falco-id": "895C66B982574716B7A80C2C722BBBFE",
#   "x-sign": "izKMHp006xAAJhbFxKSxyA9alXe3VhbGHc4T8FoSpuEeqNbQQbKlADm4Z%2B9O9sjzAIOEXVkPRqrFhCLKRvdacpeikGYW1hbGFtYWxh",
#   "x-mini-wua": "iggRqLTsr%2FbkcYBbgh5UUfgxm9U5maoqhSNy1MYrRp4ElyX%2FgPuvT6tuRih78FQGX3KdGXJH5xbFQNaD3poFpmU4rUOaU4H%2Fcfjty3lhmOlanvhQUtAfkwQNyVTN0fUG8RKyfpikiISLco7cC5Jk0QyLyPPD0VZHsVV6e10V1ISUbG7cwW1nSI27bHU40vdvIgQM%3D",
#   "c-launch-info": "(null),0,1741664175988.111,0,1",
#   "x-t": "1741664176"
# }



