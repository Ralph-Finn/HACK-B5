# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:39:15 2017

@author: lenovo
"""

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
url = 'http://www.xicidaili.com/wn/'
s = requests.get(url,headers = headers)
soup = BeautifulSoup(s.text,'lxml')
ips = soup.select('#ip_list tr')
fp = open('host.txt','w')

for i in ips:
    try:
        ipp = i.select('td')
        ip = ipp[1].text
        host = ipp[2].text
        fp.write(ip)
        fp.write(':')
        fp.write(host)
        fp.write('\n')
        print('good')
    except Exception as e :
        print ('no ip !')
        
fp.close()

