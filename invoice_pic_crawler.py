import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import shutil
def invoice():
    
    invoice_url = "https://bluezz.com.tw/"
    request = urllib.request.Request(invoice_url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')
    #print(soup.select('.blog_pic'))
    pic=soup.select('.blog_pic')
    picss=re.findall('src="(.*?)"',str(pic))
    print(picss) #[0]就是這期發票對獎號碼[1]就是上一期發票對獎號碼
    #response = requests.get(picss[0], stream=True)
    #with open('invoice.jpg', 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)
    #del response
    return(picss)
if __name__ == '__main__':
    invoice()
