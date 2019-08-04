import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import shutil

def Satellite():
    url = "https://www.cwb.gov.tw/V7/js/s1p.js"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    #print(soup.text[20:-3])

    #pic=soup.text[20:-3].split(',')
    pic=soup.text[11:].split(',')
    #print(pic)

    list_url=[]
    list_time=[]
    for pics in pic:
        
        picss=pics.strip('\r"\n').split('"')
        list_url.append(picss[0])
        list_time.append(picss[2])

    pic_url="https://www.cwb.gov.tw"+list_url[0]
    return pic_url

'''
response = requests.get(pic_url, stream=True)
with open('Himawar.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

'''
if __name__ == '__main__':
    Satellite()
    

