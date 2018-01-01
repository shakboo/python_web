#!/usr/bin/python
#coding=utf-8

import requests
import re

page = 1
url = "http://www.qiushibaike.com/hot/page/" + str(page)

resp = requests.get(url)
try:
    resp.content
except:
    print("%s %s" % (resp.status_code,resp.reason))