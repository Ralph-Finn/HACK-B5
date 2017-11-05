#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.error
import urllib.parse
import json
import xlwt

def saveData(name_list, content_list, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('网易云音乐', cell_overwrite_ok=True)
    col = ('歌曲名', '用户评论')
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(len(name_list)):
      sheet.write(i+1, 0, name_list[i])
      sheet.write(i+1, 1, content_list[i])
    
    book.save(savepath)

def get_all_hotSong():  #获取热歌榜所有歌曲名称和id
   url='http://music.163.com/discover/toplist?id=3778678' #网易云云音乐热歌榜url
   html=urllib.request.urlopen(url).read().decode('utf8') #打开url
   html=str(html)  #转换成str
   pat1=r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>' #进行第一次筛选的正则表达式
   result=re.compile(pat1).findall(html)  #用正则表达式进行筛选
   result=result[0]  #获取tuple的第一个元素
  
   pat2=r'<li><a href="/song\?id=\d*?">(.*?)</a></li>' #进行歌名筛选的正则表达式
   pat3=r'<li><a href="/song\?id=(\d*?)">.*?</a></li>' #进行歌ID筛选的正则表达式
   hot_song_name=re.compile(pat2).findall(result) #获取所有热门歌曲名称
   hot_song_id=re.compile(pat3).findall(result) #获取所有热门歌曲对应的Id
  
   return hot_song_name,hot_song_id

def get_hotComments(hot_song_name, hot_song_id):
   url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + hot_song_id + '?csrf_token=' #歌评url
   header={ #请求头部
   'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  }
   #post请求表单数据
   data={'params':'zC7fzWBKxxsm6TZ3PiRjd056g9iGHtbtc8vjTpBXshKIboaPnUyAXKze+KNi9QiEz/IieyRnZfNztp7yvTFyBXOlVQP/JdYNZw2+GRQDg7grOR2ZjroqoOU2z0TNhy+qDHKSV8ZXOnxUF93w3DA51ADDQHB0IngL+v6N8KthdVZeZBe0d3EsUFS8ZJltNRUJ','encSecKey':'4801507e42c326dfc6b50539395a4fe417594f7cf122cf3d061d1447372ba3aa804541a8ae3b3811c081eb0f2b71827850af59af411a10a1795f7a16a5189d163bc9f67b3d1907f5e6fac652f7ef66e5a1f12d6949be851fcf4f39a0c2379580a040dc53b306d5c807bf313cc0e8f39bf7d35de691c497cda1d436b808549acc'}
   postdata=urllib.parse.urlencode(data).encode('utf8') #进行编码
   request=urllib.request.Request(url,headers=header,data=postdata)
   reponse=urllib.request.urlopen(request).read().decode('utf8')
   json_dict=json.loads(reponse) #获取json
   hot_commit=json_dict['hotComments'] #获取json中的热门评论
   name_list = []
   commit_list = []
   for item in hot_commit:
     name_list.append(hot_song_name)
     commit_list.append(item['content'])
   return name_list, commit_list
  
"""
   fhandle=open('./song_comments.csv','a', encoding='utf-8') #写入文件
   fhandle.write(hot_song_name+':'+'\n')
  
   for item in hot_commit:
    num+=1
    fhandle.write(item['content'] + '\n')
   fhandle.write('\n==============================================\n\n')
   fhandle.close()
  
  """

def main():
  hot_song_name,hot_song_id=get_all_hotSong() #获取热歌榜所有歌曲名称和id
  book = xlwt.Workbook(encoding='utf-8', style_compression=0)
  sheet = book.add_sheet('网易云音乐', cell_overwrite_ok=True)
  col = ('歌曲名', '用户评论')
  for i in range(0, len(col)):
     sheet.write(0, i, col[i])
  num=0
  name_list = []
  commit_list = []
  while num < len(hot_song_name): #保存所有热歌榜中的热评
     print('正在抓取第%d首歌曲热评...'%(num+1))
     add_name_list, add_commit_list = get_hotComments(hot_song_name[num],hot_song_id[num])
     name_list += add_name_list
     commit_list += add_commit_list
     print('第%d首歌曲热评抓取成功'%(num+1))
     num+=1
  saveData(name_list, commit_list, './music.csv')
  


main()