# -*- coding: utf-8 -*-

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


desurl = 'http://ip.360.cn/IPQuery/ipquery'
params = {
    'ip': "8.8.8.8"
}
response = httpgetwithparam(desurl, params)
print(response.status)
print(response.reason)
print(response.read())
print(response.getheaders())


