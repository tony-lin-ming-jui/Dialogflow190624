import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import shutil
def rainfall():
    url="https://www.cwb.gov.tw/V7/observe/rainfall/dam.htm"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    for img in re.findall('<img src="(.*?)"',str(soup)):
    #img=re.findall('<img src="(.*?)"',str(soup))
        #print("https://www.cwb.gov.tw/V7/observe/rainfall/"+img)

        ID="https://www.cwb.gov.tw/V7/observe/rainfall/"+img
    #print(ID)
    return ID
'''
response = requests.get(ID, stream=True)

#下載圖片
with open('rainfall.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
'''
if __name__ == '__main__':
    rainfall()
