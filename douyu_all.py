import requests
import json
def getHtmlText(rl):
	try:
		headers = {'X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/56.0.2924.87 Safari/537.36'}
		r = requests.get(rl,headers=headers,timeout=50)
		r.raise_for_status() #如果状态不是200，引发HTTPError异常
		r.encoding = r.apparent_encoding
		return r.text
	except :
		return "产生异常"

def Handledata(html,ulist):
        rl = json.loads(html)
        mylist = rl['data']['rl']
        for n in mylist:
                ulist.append([len(ulist)+1,n['nn'], n['ol']])


def Prin(ulist):
        tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
        print(tplt.format("序号", "名字", "人数", chr(12288)))
        for i in range(len(ulist)):
                u = ulist[i]
                print(tplt.format(u[0], u[1], u[2], chr(12288)))

def Count(ulist):
	cou = []
	for i in range(len(ulist)):
		cou.append(float(ulist[i][2]))
	print("总观看人数为："+str(sum(cou))+" 人")

if __name__ == '__main__':
    url = "https://www.douyu.com/gapi/rkc/directory/0_0/"
    uinfo = []
    for i in range(3):
        ul = url+str(i+1)
        html = getHtmlText(ul)
        Handledata(html,uinfo)
        print("第" + str(i + 1) + "页爬取成功"+url)
    Count(uinfo)
    Prin(uinfo)
