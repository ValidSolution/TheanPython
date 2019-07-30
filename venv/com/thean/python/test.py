#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

# a = "{\"key\":\"value\"}"
res = {}
file = open("part-00063")

while 1:
    line = file.readline()
    if not line:
        break
    j = json.loads(line)
    count = res.get(j["cid"], 0)
    count += 1
    res[j["cid"]] = count
file.close()
other = 0
for i, j in res.items():
    if j > 10:
        print(i, ":\t", j)
    else:
        other += j
print("other", ":\t", other)
