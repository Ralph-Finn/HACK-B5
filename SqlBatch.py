import http.client
import json
import http
import hashlib
import urllib.request
import random
import pymysql.cursors
import csv

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

def writeSql():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 使用cursor()方法获取操作游标
    cursor = connection.cursor()
    csvfile = open("./music.csv", "w")
    writer = csv.writer(csvfile)
    # SQL 查询语句
    sql = "SELECT * FROM music"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        # name = row[0]
        try:
            if(row['名称']!=''):
                name = row['名称']
            commit  = row['评论']
            if len(row['评论'])>400:
                commit = commit[0:400]
            eng = getTrans(commit)
            eng = eng + eng + eng+ eng+ eng
            inp_dict = getRes(eng)
            person = getPerson(inp_dict)
            print(person)
            writer.writerow([name,person[0], person[1],person[2],person[3],person[4],row['评论']])
        except:
            print('erro')
    connection.close()

writeSql()

