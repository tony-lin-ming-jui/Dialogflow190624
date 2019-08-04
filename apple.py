import requests
import urllib.request
from bs4 import BeautifulSoup
import random
import re
def apple_news():
    
    res= requests.get('https://tw.appledaily.com/new/realtime')
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = []
    for index, data in enumerate(soup.select('div.item a')):
        if index == 20:           
            return content
          
        title = data.find('img')['alt'].replace("\u3000", " ", 1)
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content.append(title)
        content.append(link)
        content.append(link2)
    
    #print(content)
    return content
apple_news()

a=apple_news()
news_title=[]
news_link=[]
news_photo=[]    
for i in range(0,len(a),3):   
    news_title.append(a[i])
    news_link.append(a[i+1])
    news_photo.append(a[i+2])

#print(news_title)

news_group=[]    #創一個List
    #將剛剛的三個List加進來
news_group.append(news_title)
news_group.append(news_link)
news_group.append(news_photo)
    #要做為key值的List
x=['title','link','link2']
    #把兩個做成dictionary
dictionary = dict(zip(x,news_group))
#print(len(news_group))
#print(len(news_title))
#if len(news_title)>10:
    #p=random.sample(len(news_title),10)
    
    #for i in range(0,len(news_title)):
        #print(dictionary['link2'][i])
        #print(dictionary['link'][i])
        #print(dictionary['title'][i][0:8])  


#else:
    #p=random.sample(range(len(news_title)),len(news_title))
    #for i in range(0,len(news_title)):
        #print(dictionary['link2'][i])
        #print(dictionary['link'][i])
        #print(dictionary['title'][i][0:8])  




'''
print(dictionary['link2'][0])
print(dictionary['link'][0])
print(dictionary['title'][0][0:8])  

print(dictionary['link2'][1])
print(dictionary['link'][1])
print(dictionary['title'][1][0:8])

print(dictionary['link2'][2])
print(dictionary['link'][2])
print(dictionary['title'][2][0:8])

print(dictionary['link2'][3])
print(dictionary['link'][3])
print(dictionary['title'][3][0:8])
      
print(dictionary['link2'][4])
print(dictionary['link'][4])
print(dictionary['title'][4][0:8])

print(dictionary['link2'][5])
print(dictionary['link'][5])
print(dictionary['title'][5][0:8])

print(dictionary['link2'][6])
print(dictionary['link'][6])
print(dictionary['title'][6][0:8])

print(dictionary['link2'][7])
print(dictionary['link'][7])
print(dictionary['title'][7][0:8])

print(dictionary['link2'][8])
print(dictionary['link'][8])
print(dictionary['title'][8][0:8])

print(dictionary['link2'][9])
print(dictionary['link'][9])
print(dictionary['title'][9][0:8])
'''
if __name__ == '__main__':
    apple_news()
