# -*- coding: utf-8 -*-  
import urllib.request  
import demjson
import pymysql 
from bs4 import BeautifulSoup


#函数-读取指定URL数据
def getHtml(url):  
    page=urllib.request.urlopen(url)  
    html=page.read().decode(encoding='utf-8',errors='strict')
    return html  

#打开数据库连接  
db = pymysql.connect(host="localhost",user="root", password="newpdcc",db="fund",port=3306,use_unicode=True, charset="utf8")  
cur = db.cursor()  
count=cur.execute("select * from fund_jingzhi where fund_code>='050116'")
print('there has %s rows record' % count)
results=cur.fetchall()
for r in results:
    url_fhsp = 'http://fund.eastmoney.com/f10/fhsp_'+r[0]+'.html'
    html_fhsp = getHtml(url_fhsp)
    soup = BeautifulSoup(html_fhsp, "html.parser") 

    #分红
    fhTable = soup.find('table', {'class':'w782 comm cfxq'})	
    if fhTable :
        trList = fhTable.find_all('tr')
        for tr in trList: 
            tdList = tr.find_all('td')
            if len(tdList)>3:
                sql = 'replace into fund_jjfh values ("'+r[0]+'",'
                for td in tdList: 
                    sql += '"'+ td.get_text()+'",'
                sql += '"")'
                print(sql) 
                cur.execute(sql)
                db.commit()	

    #分红配额
    spTable = soup.find('table', {'class':'w782 comm fhxq'})	
    if spTable :
        trList = spTable.find_all('tr')
        for tr in trList: 
            tdList = tr.find_all('td')
            if len(tdList)>3:
                sql = 'replace into fund_jjsp values ("'+r[0]+'",'
                for td in tdList: 
                    sql += '"'+ td.get_text()+'",'
                sql += '"")'
                print(sql) 
                cur.execute(sql)
                db.commit()	

cur.close()
db.close()
