import re
import urllib.request
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
def weather():
    url = "https://www.cwb.gov.tw/V7/forecast/f_index.htm?_=1536315389251"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    ##tag1='div.NorthArea a'
    tag1='div.big01 a'
    tag2='div.big03 a'
    weather=soup.select(tag1)+soup.select(tag2)
    
    list_w=[]
    for weathers in weather:
        #print(Norths.text)
        #"".join->list轉str
        
        list_w.append("".join(re.findall('img alt="(.*?)"',str(weathers))))
        list_w.append(weathers.text)
        #print(Norths.text)
        
        #print(Norths.select('img'))
    #weather=soup.text
    #print(list_w)
    list_weather=[]
    list_we=[]
    for i in range(0,len(list_w),8):
        #list_weather.append(list_w[i+1]+" ")
        #list_weather.append("溫度"+list_w[i+3]+" ")
        #list_weather.append("降雨機率:"+list_w[i+5]+"\n")
        #list_weather.append(list_w[i+6]+"")
        #list_weather.append("\n\n")
        list_we.append(list_w[i+1]+" "+"\n"+"溫度"+list_w[i+3]+" "+"降雨機率:"+list_w[i+5]+"\n"+list_w[i+6]+" "+"\n\n")
        #list_we.append(list_w[i+1]+list_w[i+3]+list_w[i+5]+list_w[i+6])
    #print(list_weather)
    #print(list_we)
    return list_we

if __name__ == '__main__':
    weather()

#b=weather()
#print(b[0])
#a= ''.join(weather())
#print(a)

'''用來抓取其中1個縣市的資料
weather=weather()
i=0
j=5
while i<len(weather)-6:
    #print("i",i,"j",j)
    print(weather[i:j])
    i=i+5
    j=j+5
    
'''
