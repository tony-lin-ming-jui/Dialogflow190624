import re
import urllib.request
from bs4 import BeautifulSoup
import pandas
import requests
def oil():
    res= requests.get("https://gas.goodlife.tw/")
    soup=BeautifulSoup(res.text,'lxml')
    oil=soup.select('#main')
    list_o=[]
    for oils in oil:        
        oilss=oils.text.split()
        #a=oils.text
        #print(oils.text)
    #b='\n'.join(oilss)
    #print("b",b)
    #print(a)
    #print(type(a))
    #print(oilss)
    x="{0[0]}\n{0[1]} {0[2]}\n{0[26]}{0[27]}{0[28]}{0[29]}\n{0[30]}{0[31]}{0[32]}{0[33]}{0[34]}{0[35]}{0[36]}{0[37]},{0[38]}".format(oilss)
    #aa="{0[26]}{0[27]}{0[28]}{0[29]}".format(oilss)
    #aa="{0[30]}{0[31]}{0[32]}{0[33]}{0[34]}{0[35]}{0[36]}".format(oilss)
    y="{0[39]}{0[40]}{0[41]}\n\n{0[42]}{0[43]}{0[44]}  {0[45]}{0[46]}  {0[47]}{0[48]}".format(oilss)
    z="{0[49]}{0[50]}{0[51]}:{0[52]} {0[53]}{0[54]}{0[55]}  {0[56]}{0[57]}  {0[58]}{0[59]}".format(oilss)
    #print(x+"\n"+y+"\n"+z)
    oil=x+y+"\n"+z
    #print(aa)
    
    #print("\n\n")
    #print(x)
    #print(y)
    print(oil)
    #print("{0[0]}{0[1]} {0[2]}\n{0[30]}{0[31]}{0[32]}{0[33]}{0[34]}{0[35]}{0[36]}{0[37]}{0[26]}{0[27]}{0[28]}{0[29]},{0[38]}{0[39]}{0[40]}{0[41]}".format(oilss))
    #print("{0[42]}:{0[43]}{0[44]}  {0[45]}{0[46]}  {0[47]}{0[48]}  {0[49]}{0[50]}".format(oilss))
    #print("{0[51]}:{0[52]}{0[53]}  {0[54]}{0[55]}  {0[56]}{0[57]}  {0[58]}{0[59]}".format(oilss))
    #print('x',x)
    #print('\ny',y)
    #print('\nz',z)
    

    #print(oil)
    return oil

if __name__ == '__main__':
    oil()
