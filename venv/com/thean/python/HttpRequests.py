#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests


def httpget(url, value):
    return requests.get(url, params=value)


def httppost(url, value):
    return requests.post(url, params=value)


desurl = 'http://ip.taobao.com/service/getIpInfo.php'
params = {
    'ip': "8.8.8.8"
}
response = httppost(desurl, params)
resStr = response.json()
print(resStr)
print(resStr["data"]["country"])


