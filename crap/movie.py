#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import numpy as np
import requests

def getip():
  fp = open('host.txt', 'r')
  text = fp.readlines()
  ip_list = []
  for item in text:
    ip = item.strip('\n').split('\t')
    #proxy = 'http://' +  ip[0] + ':' + ip[1]
    proxy = ip[0]
    ip_list.append(proxy)
  return ip_list

#得到页面全部内容
def askURL(url, proxys):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = headers = { 'User-Agent' : user_agent }
    
    rand = int(np.floor(np.random.rand() * len(proxys)))
    chosen_ip = proxys[rand]
    print('proxy:' + chosen_ip)
    
    proxy = urllib.request.ProxyHandler({'http':chosen_ip})
    # construct a new opener using your proxy settings
    opener = urllib.request.build_opener(proxy)
    # install the openen on the module-level
    urllib.request.install_opener(opener)
    
    req = urllib.request.Request(url, headers=headers)

    html_cont = ""
    try:
        #response = urllib.request.urlopen(request)#取得响应
        response = urllib.request.urlopen(req)
        html_cont = response.read()#获取网页内容
        print('reponse success')
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html_cont

#获取相关内容
def getData(baseurl):
    #找到评论标题
    pattern_title = re.compile(r'<a class="subject-title".+>(.+)<')
    #找到评论全文链接
    pattern_link = re.compile(r'<a class="title-link".+href="(.+review.*?)"')
    #找到作者

    #去除标签
    remove = re.compile(r'<.+?>')
    
    data_list = []
    
    # get proxy ip
    ip_pool = getip()
    
    for i in range(0,1):
        url = baseurl + str(i)#更新url
        
        html = askURL(url, ip_pool)
        soup = BeautifulSoup(html)
        #找到每一个影评项
        while len(soup.find_all(class_='main review-item')) == 0:
          print('failed')
          html = askURL(url, ip_pool)
          soup = BeautifulSoup(html)
          
        for item in soup.find_all(class_='main review-item'):
            item = str(item)#转换成字符串
            
            title = re.findall(pattern_title,item)[0]
            
            print('get title:' + title)
                       
            # fetch the link to the comment page
            reviewlink = re.findall(pattern_link,item)[0]
            
            content = askURL(reviewlink, ip_pool)
            if len(content) == 0:
              print('failed in html')
              continue
            content = BeautifulSoup(content)
            desc = content.find_all('div',class_='review-content clearfix')[0]
            
            
            target = desc.find_all('p')
            if len(target) == 0:
              print('failed in finding comment')
              continue
            target = re.sub(remove,'',str(target[0]))#去掉标签
            print('get comment')
            
            data_list.append(title)
            data_list.append(target)
            
    return data_list

#将相关数据写入excel中
def saveData(data_list, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('豆瓣最受欢迎影评', cell_overwrite_ok=True)
    col = ('影片名', '影评')
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    i = 0
    j = 1
    while i < len(data_list):
      sheet.write(j, 0, data_list[i])
      sheet.write(j, 1, data_list[i+1])
      i = i + 2
      j = j + 1
    
    book.save(savepath)

def main():
    baseurl='http://movie.douban.com/review/best/?start='
    print('start...')
    data_list = getData(baseurl)
    print('done.')
    savapath = u'./movie_comments.csv'
    print('saving...')
    saveData(data_list, savapath)
    print('done')

main()