from flask import Flask,render_template,request,redirect,url_for,flash#,jsonify,session
import re
import urllib.request
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def oilof():
    url = "https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html =response.read()
    soup=BeautifulSoup(html,'lxml')

    data=re.findall("line.*=('.*)",str(soup))
    date=re.findall("d.*]=('.*)",str(soup))

    list_oildata=[]
    list_oildate=[]
    b=[]
    for datas in data:
        datass=datas.strip(";'\r")#刪除 ; '' \r
        list_oildata.append(float(datass))
        #b.append(float(datass))
    for dates in date:
        datess=dates.strip(";'\r")#刪除 ; '' \r      
        list_oildate.append(str(datess))
        #b.append(str(datess))
    #a=list_oildate+list_oildata
    #print(len(list_oildate))
    #print(len(list_oildata))

    #print(list_oildate+list_oildata)
    return list_oildate+list_oildata
'''
@app.route('/plot')  
def oilweb(oilof):
    img = io.BytesIO()
    #oilof=oilof()
    print(oilof)
    #print(list_oildate)
    #print(list_oildata)
    list_oildate=oilof[:31]
    list_oildata=oilof[-93:]
    print(list_oildate)
    print(list_oildata)


    print("======================================================================================")
    x=0
    y=3
    list_a=[]
    for i in range(0,31):    
        list_a.append(list_oildata[x:y])
        #print(list_oildata[:x])
        x=x+3
        y=y+3

    #print(list_a)
    jd=json.loads(str(list_a))
    print("======================================================================================")
    #print(jd)
    import pandas
    df=pandas.DataFrame(jd)
    df.columns = ['西德州','北海布蘭特','杜拜']
    print(df)
    print("最新國際原油價格:\n",df.iloc[30])
    print("======================================================================================")


    list_r=list_oildata[0:93:3]
    list_g=list_oildata[1:93:3]
    list_b=list_oildata[2:93:3]

    #print(list_r)

    plt.cla()
    plt.gcf().set_size_inches(20,20)
    plt.plot(list_oildate,list_r,'o-',color='deeppink')
    plt.plot(list_oildate,list_g,'o-',color='#ADFF2F')
    plt.plot(list_oildate,list_b,'o-',color='deepskyblue')    
    #plt.show
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

'''
'''
#oilof=oilof()
#oilweb(oilof)

@app.route('/plot')
def oilweb(oilof):
    img = io.BytesIO()
    
    #oilof=oilof()
    list_oildate=oilof[:31]
    list_oildata=oilof[-93:]
    print(list_oildate)
    print(list_oildata)


    print("======================================================================================")
    x=0
    y=3
    list_a=[]
    for i in range(0,31):    
        list_a.append(list_oildata[x:y])
        #print(list_oildata[:x])
        x=x+3
        y=y+3

    #print(list_a)
    jd=json.loads(str(list_a))
    print("======================================================================================")
    #print(jd)
    import pandas
    df=pandas.DataFrame(jd)
    df.columns = ['西德州','北海布蘭特','杜拜']
    print(df)
    print("最新國際原油價格:\n",df.iloc[30])
    print("======================================================================================")


    list_r=list_oildata[0:93:3]
    list_g=list_oildata[1:93:3]
    list_b=list_oildata[2:93:3]

    #print(list_r)

    plt.cla()
    plt.plot(list_oildate,list_r,'o-',color='deeppink')
    plt.plot(list_oildate,list_g,'o-',color='#ADFF2F')
    plt.plot(list_oildate,list_b,'o-',color='deepskyblue')
    plt.gcf().set_size_inches(20,20)
    #plt.show
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('plot.html', plot_url=plot_url)


'''
if __name__ == '__main__':
    #app.run(port=6000,debug =True)
    oilof()
    #oilof=oilof()
    #oilweb(oilof)
