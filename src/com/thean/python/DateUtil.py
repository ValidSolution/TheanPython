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


datetime.datetime(1500099889)
dt = datetime.datetime(2018, 5, 28, 12, 15, 45)
while dt.second != 56:
    date = dt.strftime('%Y-%m-%d %H:%M:%S')
    print(date)
    dt = dt + datetime.timedelta(seconds=1)
