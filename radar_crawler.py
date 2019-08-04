import re
import requests
from bs4 import BeautifulSoup
import urllib.request
#import shutil

import json
import requests

def radar():
    url = "https://www.cwb.gov.tw/V7/js/HDRadar_3600.js"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    
    pic=soup.text[20:-3].split(',')
    list_a=[]
    list_url=[]
    #list_time=[]
    for pics in pic:
        
        picss=pics.strip('\r"\n').split('"')
        list_url.append(picss[0])
        #list_time.append(picss[2])

    #print(list_url[0])
    pic_url="https://www.cwb.gov.tw"+list_url[0]
    #list_a.append(str(pic_url))
    #print(pic_url)
    radar= list_url[0]
    return pic_url


if __name__ == '__main__':
    radar()
    
