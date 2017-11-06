#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import requests
from bs4 import BeautifulSoup

def getHtmlText(url):
	try:
		headers = {'X-Requested-With': 'XMLHttpRequest',
				   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/56.0.2924.87 Safari/537.36'}
		r = requests.get(url, headers=headers, timeout=60)
		r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "产生异常"

def Handledata(html,ulist):
    print(html[:100])
    try:
        soup = BeautifulSoup(html, "html.parser")
        div1 = soup.find_all("div", class_="left")
        for sons in div1[1]("div",class_="sons"):
            name = sons("b")[0].string
            author = sons("a")[2].string
            period = sons("a")[1].string
            songs = sons("div",class_="contson")[0].text
            type = ''
            for i in range(len(sons("div",class_="tag")[0]("a"))):
                type = type + sons("div",class_="tag")[0]("a")[i].string+','

            ulist.append([len(ulist) + 1, name, author, period, songs, type])
    except:
        print("Hadnledata Error!")
        return

def intoMysql(ulist):
    db = pymysql.connect(host="112.74.32.60", user="lee", passwd="Lee_10928", db="songs", charset="utf8")
    cursor = db.cursor()

    for i in range(len(ulist)):
        u = ulist[i]
        sql = "insert into songs values('%s','%s','%s','%s','%s','%s')" % (u[0], u[1], u[2], u[3], u[4].strip(), u[5])
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
    db.close()
    print(len(ulist))
    print("插入数据成功")

if __name__ == '__main__':
    url = "http://www.gushiwen.org/default_"#105.aspx
    uinfo = []
    for i in range(5):
        if i == 0:
            ul = "http://www.gushiwen.org"
        else:
            ul = url + str(i+1) + '.aspx'
        print(ul)
        html = getHtmlText(ul)
        Handledata(html, uinfo)
        print("第%d页爬取完成"%i)
    intoMysql(uinfo)

