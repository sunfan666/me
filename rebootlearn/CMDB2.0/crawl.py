#/usr/bin/env python
#coding:utf-8
import requests
from pyquery import PyQuery as pq
url = 'http://movie.douban.com/top250'
res = requests.get(url)
print res.text

