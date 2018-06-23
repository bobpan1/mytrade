# -*- coding: utf-8 -*-  
import urllib.request  
import demjson
import pymysql 
import time
from bs4 import BeautifulSoup


#函数-读取指定URL数据
def getHtml(url):  
    page=urllib.request.urlopen(url,timeout=10)  
    html=page.read().decode(encoding='utf-8',errors='strict')
    return html  

#打开数据库连接  
db = pymysql.connect(host="localhost",user="root", password="",db="fund",port=3306,use_unicode=True, charset="utf8")  
cur = db.cursor()  
count=cur.execute("select * from fund_jingzhi where fund_code>='004000'")
print('there has %s rows record' % count)
results=cur.fetchall()
for r in results:
	for year in range(2001,2017) :
		for m in range(1,5):
			month = m*3
			url_jjcc = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code='+r[0]+'&topline=&year='+str(year)+'&month='+str(month)
			print(url_jjcc)
			while True:
				try:
					html_jjcc = getHtml(url_jjcc)
					break
				except Exception as e:
					print("HOST REJECT ERROR, Waiting...")
					time.sleep(20)
			
			soup = BeautifulSoup(html_jjcc, "html.parser") 

			#股票持仓清单
			fhTable = soup.find_all('table', {'class':'w782 comm tzxq t2'})	
			for tb in fhTable: 
				trList = tb.find_all('tr')
				for tr in trList: 
					tdList = tr.find_all('td')
					if len(tdList)>3:
						sql = 'replace into fund_jjcc values ("'+r[0]+'","'+str(year)+'","'+str(month)+'",'
						for td in tdList: 
							tdStr = td.get_text().replace(",","");
							sql += '"'+ tdStr +'",'
						sql += '"")'
						print(sql) 
						cur.execute(sql)
						db.commit()	

    

cur.close()
db.close()
