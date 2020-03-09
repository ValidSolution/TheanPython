# -*- coding: utf-8 -*-

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def httppost(url, values):
    request = Request(url, urlencode(values).encode())
    return urlopen(request)


def httpgetwithparam(url, param):
    index = 0
    finalurl = url
    for key in param.keys():
        if index > 0:
            finalurl += "&"
        else:
            finalurl += "?"
        value = params.get(key)
        finalurl += str(key) + "=" + str(value)
        index += 1
    return httpget(finalurl)


def httpget(url):
    return urlopen(url)


if __name__ == "__main__":
    desurl = 'http://ip.taobao.com/service/getIpInfo.php'
    params = {
        'ip': "8.8.8.8"
    }
    response = httpgetwithparam(desurl, params)
    resStr = response.read().decode()
    print(resStr)
    res = json.loads(resStr)
    print(res["data"]["country"])

