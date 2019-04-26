import datetime
import time


def ts2str(timestamp):
    return ts2strwithformat(timestamp, "%Y-%m-%d %H:%M:%S")


def ts2strwithformat(timestamp, format):
    arr = time.localtime(timestamp)
    return time.strftime(format, arr)


def str2ts(string):
    return str2tswithformat(string, "%Y-%m-%d %H:%M:%S")


def str2tswithformat(string, format):
    arr = time.strptime(string, format)
    return time.mktime(arr)
