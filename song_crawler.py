import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas
def ranking():
    url = 'http://www.hitoradio.com/newweb/chart_1_1.php'
    list_rank=[]
    for i in range(1,4):
        #print (i)
        if i==1:
            #print("Hito中文歌曲排行")
            list_rank.append("Hito中文歌曲排行")
        elif i==2:
            #print("\nHito西洋歌曲排行")
            list_rank.append("Hito西洋歌曲排行")
        elif i==3:
            #print("\nHito日亞歌曲排行")
            list_rank.append("Hito日亞歌曲排行")
        new_link = re.sub('chart_1_\d+.php','chart_1_%d.php'%i, url)#1~3頁 \d表示數字
        #new_link = re.sub('chart_1_\d+.php','chart_1_%d.php'%i, url, re.S)
        #print (new_link)
        df=pandas.read_html(new_link)
        x=df[4][5][0].split()

        list_rank.append("名次:1 "+x[0][3:]+"  "+x[2][3:])
        #print("名次:1 "+x[0][3:]+"  "+x[2][3:])
        #print("===========================================================================")
        #print(df[5])

        for j in range(5,14):

            rank="名次:"+str(j-3)+" "+df[j][5][0]
            list_rank.append("名次:"+str(j-3)+" "+df[j][5][0])
            #print("名次:"+str(j-3)+" "+df[j][5][0])
            #print(rank)
    return list_rank
if __name__ == '__main__':
    ranking()



