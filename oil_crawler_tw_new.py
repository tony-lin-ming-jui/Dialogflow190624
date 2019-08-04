import re
import urllib.request
from bs4 import BeautifulSoup
import pandas
import requests
def oil():
    res= requests.get("https://gas.goodlife.tw/")
    res.encoding = 'utf-8'
    soup=BeautifulSoup(res.text,'lxml')
    time=soup.select('.timeago')
    list_oil=[]
    #print(time)
    for time in soup.select('.timeago'):
        
        list_oil.append("更新時間: "+time.text)

    for data in soup.select('#main li'):
        oil=data.text.strip()
        a=re.sub('\s','',oil)
        r=a.replace("92:", "92油價 ")
        x=r.replace("98:", "98油價 ")
        y=x.replace(":", " ")
        list_oil.append(y)
        
    z="{0[0]}\n{0[10]}{0[11]}\n{0[12]}\n中油油價\n{0[13]}元\n{0[14]}元\n{0[15]}元\n{0[16]}元\n台塑油價\n{0[17]}元\n{0[18]}元\n{0[19]}元\n{0[20]}元".format(list_oil)
    #a="{0[0]}\n中油油價\n{0[13]}元 {0[14]}元 {0[15]}元 {0[16]}元\n台塑油價\n{0[17]}元 {0[18]}元 {0[19]}元 {0[20]}元".format(list_oil)
    #如果網也改格式掛掉就試試看a 應該是字數太多掛掉或特殊字元符號掛掉
    #print(z)
    return z
if __name__ == '__main__':
    oil()