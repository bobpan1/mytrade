# -*- coding: utf-8 -*-  
import urllib.request  
import demjson
import pymysql 


#函数-读取指定URL数据
def getHtml(url):  
    page=urllib.request.urlopen(url)  
    html=page.read().decode(encoding='utf-8',errors='strict')
    return html  

#读取“天天基金网-基金净值清单”
url='http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|&dt=1508468784145&atfc=&onlySale=0'  
jsonstr = getHtml(url)

#解析JSON数据
jsonstr = jsonstr.replace('var db=','')
data = demjson.decode(jsonstr)


#打开数据库连接  
db = pymysql.connect(host="localhost",user="root", password="newpdcc",db="fund",port=3306,use_unicode=True, charset="utf8")  
  
# 使用cursor()方法获取操作游标  
cur = db.cursor()  

#开始插入数据库
for t in range(0,len(data['datas'])):

    sql = 'insert into fund_jingzhi values ('
    for i in range(0,len(data['datas'][t])):
	    sql += ('"'+ data['datas'][t][i]+'",')
    sql += '"")'
    print(sql)  
    cur.execute(sql)
    db.commit()

cur.close()
db.close()
