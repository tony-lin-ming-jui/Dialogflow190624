import re
import urllib.request
from bs4 import BeautifulSoup
import pandas
import requests
def movie():
    res= requests.get('https://movies.yahoo.com.tw/')
    soup = BeautifulSoup(res.text, 'html.parser')   
    content1 = ""
    list_title=[]
    list_link=[]
    list_img=[]
    for data in soup.select('div.movielist_info h2 a'):
        #print(index)
        title = data.text
        link = data['href']
        list_title.append(title)
        list_link.append(link)
        content1 += '{}\n{}\n'.format(title, link)
    #print(content1)
    #print(type(content1))
    
    content2 = ""
    for data in soup.select('div.movie_foto img'):
        #if index == 20:
            #print(content2)
        img=data['src']
        #print(data['src'])    
        list_img.append(img)
        content2 +='{}\n'.format(img)
    #print(content2)

    #content1[0][0]+content2[0][0]
    #print("list_title\n",list_title)
    #print("list_link\n",list_link)
    #print("list_img\n",list_img)
    list_ALL=[]
    for i in range(0,len(list_title)):
        A=list_title[i]+list_link[i]+list_img[i]
        list_ALL.append(list_title[i])
        
        list_ALL.append(list_link[i])
        
        list_ALL.append(list_img[i])

        #print(A)
    #print(list_ALL)
    #print(list_title)        
    return list_ALL


a=movie()
news_title=[]
news_link=[]
news_img=[]    
for i in range(0,len(a),3):   
    news_title.append(a[i])
    news_link.append(a[i+1])
    news_img.append(a[i+2])

news_group=[]    #創一個List
    #將剛剛的三個List加進來
news_group.append(news_title)
news_group.append(news_link)
news_group.append(news_img)
#print(len(news_title))
#print(news_group)
x=['title','link','link2']
    #把兩個做成dictionary
dictionary = dict(zip(x,news_group))

if __name__ == '__main__':
    movie()
