import math
import pymysql.cursors
import csv
import numpy as np
import json
import http
import hashlib
import urllib.request
import random

def oulide(A,B):
    oulide =0
    for i in range(5):
        oulide += math.sqrt(pow((A[i] - B[i]),2))
    return oulide


def searchBest(personality,type):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 使用cursor()方法获取操作游标
    cursor = connection.cursor()
    #csvfile = open("./books.csv", "w")
    sql = "SELECT * FROM "+type
    cursor.execute(sql)
    results = cursor.fetchall()
    best = 5
    bestName = "NULL"
    bestComment = "NULL"
    for row in results:
        # name = row[0]
        try:
            ax = oulide([row['O'],row['C'],row['E'],row['A'],row['R']],personality)
            if(best > ax):
                best = ax
                bestName = row['name']
                bestComment = row['comment']
        except:
            print('erro')
    connection.close()
    return bestName,bestComment

def getRes(payload):
    conn = http.client.HTTPSConnection("gateway.watsonplatform.net")
    headers = {
        'content-type': "text/plain",
        'accept': "application/json",
        'authorization': "Basic ZTgwNDQwMjctYThlZC00NTg3LTlkOTctY2UwOTBmNmRkMjRhOjJrb1p4TWtxekVlUg==",
        'cache-control': "no-cache",
        'postman-token': "3510cf13-a1e3-9b43-3bae-d3ae259e8915"
        }
    conn.request("POST", "/personality-insights/api/v3/profile?version=2017-10-13", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    print(type(data))
    inp_dict = json.loads(data)
    #inp_dict=json.dumps(data)
    #print(type(inp_dict))
    #print (inp_dict)
    return inp_dict

def getPerson(inp_dict):
    big_5 = list2 = [0.0, 0.0, 0.0, 0.0, 0.0 ]
    big_5[0] = inp_dict["personality"][0]['percentile']
    big_5[1] = inp_dict["personality"][1]['percentile']
    big_5[2] = inp_dict["personality"][2]['percentile']
    big_5[3] = inp_dict["personality"][3]['percentile']
    big_5[4] = inp_dict["personality"][4]['percentile']
    return big_5

def getTrans(content):
    appid = '20171104000092704'    #参考百度翻译后台，申请appid和secretKey
    secretKey = 'bHgGMizBAVNDbRW1MKpD'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content                  #文本文件中每一行作为一个翻译源
    fromLang = 'zh'                         #中文
    toLang = 'en'                             #英文
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    sign = sign.encode('UTF-8')
    m1 = hashlib.md5()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
    #response是HTTPResponse对象
    response = httpClient.getresponse()
    html= response.read().decode('UTF-8')
    target2 = json.loads(html)
    src = target2["trans_result"][0]["dst"]
    print(src)#取得翻译后的文本结果,测试可删除注释
    #print('翻译成功，请查看文件')
    return src

def getPersonality():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    results = cursor.fetchall()
    personality =[0.0,0.0,0.0,0.0,0.0]
    personality = np.array(personality)
    num =0
    for row in results:
        try:
            commit  = row['contents']
            if len(row['contents'])>300:
                commit = commit[0:300]
            eng = getTrans(commit)
            eng = eng + eng + eng+ eng+ eng
            inp_dict = getRes(eng)
            person = np.array(getPerson(inp_dict))
            personality += person
            print(personality)
            num=num+1
        except:
            print('erro')
    personality = personality/num
    print(personality)
    connection.close()


def getRecommend(personality):
    bestBook, bestBookComment = searchBest(personality,"bookAll")
    bestMovie, bestMovieComment = searchBest(personality, "movieAll")
    bestMusic, bestMusicComment = searchBest(personality, "musicAll")
    data={}
    data['bestBook'] = bestBook
    data['bestBookComment'] = bestBookComment
    data['bestMovie'] = bestMovie
    data['bestMovieComment'] = bestMovieComment
    data['bestMusic'] = bestMusic
    data['bestMusicComment'] = bestMusicComment
    print(data)
    return data

def data():
    personality = [ 0.86105896 ,0.17707479 , 0.2697406 ,  0.20524916 , 0.44194282]
    data = getRecommend(personality)
    return data

#data()