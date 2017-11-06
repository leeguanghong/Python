import re
import requests
from bs4 import BeautifulSoup
def getHtmlText(rl):
	try:
		headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.87 Safari/537.36'}
		r = requests.get(rl,headers=headers,timeout=30)
		r.raise_for_status() #如果状态不是200，引发HTTPError异常
		r.encoding = r.apparent_encoding
		return r.text
	except :
		return "产生异常"

def Handledata(html,ulist):
    lis = BeautifulSoup(html, "html.parser")
    for li in lis.find_all("li"):
        name = li.find_all("span", class_="dy-name")[0].string
        num = li.find_all("span", class_="dy-num")[0].string
        #print(name, "\t", num)
        ulist.append([len(ulist)+1,name, num])

def Prin(ulist):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("序号", "名字", "人数", chr(12288)))
    for i in range(len(ulist)):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))

def Wfile(ulist,file_name):
	s = ''
	i = 0
	file=open(file_name,"a")
	for le in range(len(ulist)):
		le = ulist[i]
		s = s+str(le[0])+'\t'+str(le[1])+'\t'+str(le[2])+'\n'
		i = i+1
	file.write(s)
	file.close()

def Count(ulist):
	i = 0
	cou = []
	for la in range(len(ulist)):
		if re.search('万', ulist[i][2]):
			cou.append(float(re.sub('万', '', ulist[i][2])) * 10000)
		else:
			cou.append(float(ulist[i][2]))
		i = i + 1
	print("总观看人数为："+str(sum(cou))+" 人")

def main():
    url = "https://www.douyu.com/directory/all?page="
    file_name="C:/Users/82189/Desktop/Python/zb/douyu.txt"
    uinfo = []
    for i in range(20):
        ul = url+str(i+1)+"&isAjax=1"
        html = getHtmlText(ul)
        Handledata(html,uinfo)
        print("第" + str(i + 1) + "次操作成功")
    Count(uinfo)
    Prin(uinfo)
    Wfile(uinfo,file_name)
main()
