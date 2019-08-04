import requests
import urllib.request
import time
import pandas
from bs4 import BeautifulSoup

def wkncls():
    url="https://www.dgpa.gov.tw/typh/daily/nds.html?uid=31"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    #time=soup.select('h4')
    list_t=[]
    for time in soup.select('h4'):
        times=time.text.split()
    #print(times[0]+" "+times[1])
    time_now=times[0]+" "+times[1]
    ##print(time_now)
    list_t.append(time_now)
    df=pandas.read_html(url)
    dfs=df[0][:-1]
    #print(dfs.iloc[0,0])
    #print(dfs.iloc[1,1])
    #print('dfs:',dfs)
    if dfs.empty:
        message="無停班停課訊息"
        list_t.append(message)
        list_t.append("\n參考資料:https://www.dgpa.gov.tw/typh/daily/nds.html?uid=31")        
    else:
        for i in range(0,len(dfs)):
            message=dfs.iloc[i,0]+dfs.iloc[i,1]
            list_t.append(message)
            list_t.append("\n參考資料:https://www.dgpa.gov.tw/typh/daily/nds.html?uid=31")
    #print(list_t)
    return list_t
'''
    for i in range(0,len(dfs)):
        #print(dfs.iloc[i,0]+dfs.iloc[i,1])

        try:
            print(dfs.iloc[i,0]+dfs.iloc[i,1])
            message=dfs.iloc[i,0]+dfs.iloc[i,1]
            list_t.append(message+"\n參考資料:https://www.dgpa.gov.tw/typh/daily/nds.html?uid=31")
        except:
            print("無停班停課訊息")
            message="無停班停課訊息"
            list_t.append(message+"\n參考資料:https://www.dgpa.gov.tw/typh/daily/nds.html?uid=31")

    print(list_t)

    return(list_t)
    #return''
'''


if __name__ == '__main__':
    wkncls()
    
#cancel=wkncls()
#print(cancel[0]+"\n"+cancel[1])



