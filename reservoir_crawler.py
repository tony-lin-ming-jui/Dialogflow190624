import re
import urllib.request
from bs4 import BeautifulSoup
import pandas
import numpy
def dam():
    url="https://www.wra.gov.tw/"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    list_d=[]
    for data in soup.select('div.WaterInfo tr td'):    
        #print(data.text)
        list_d.append(data.text.replace('\xa0', ''))
    list_da=list_d[:-36]
    #print(list_da)
    #print(len(list_da))

    list_dam=[]
    for i in range(0,len(list_da),5):
        list_dam.append(list_da[i]+":\n")
        a="水位(公尺):"
        list_dam.append(a+list_da[i+1]+"\n")
        b="滿水位(公尺):"
        list_dam.append(b+list_da[i+2]+"\n")
        c="蓄水率:"
        list_dam.append(c+list_da[i+3]+"\n")
        d="記錄時間:\n"
        list_dam.append(d+list_da[i+4]+"\n")
        #list_dam.append("\n")
    #print(list_dam)
    u="參考資料:url=https://www.wra.gov.tw/"
    list_dam.append(u)
    dams=''.join(list_dam)
    return dams

if __name__ == "__main__":
    dam()
