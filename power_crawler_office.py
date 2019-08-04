import re
import urllib.request
from bs4 import BeautifulSoup
import pandas
import requests

def power():
    resa= requests.get("http://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genloadareaperc.csv")
    resb= requests.get("http://www.taipower.com.tw/d006/loadGraph/loadGraph/data/reserve.csv")
    #print(resa.text)
    #print(resy.text)
    powera=resa.text.strip("\r\n")
    powerb=resb.text.strip("\r\n,,,")
    for poweras in powera:
        poweras=powera.split(',')
    #print(poweras)
    #print("======================================================================================")
    #print(list(poweras))
    powerax=list(poweras)
    #print(powerax)
    list_al=[]
    #print("時間：{0[0]}:\n北部即時用電量:{0[2]}萬瓩\n中部即時用電量:{0[4]}萬瓩\n南部即時用電量:{0[6]}萬瓩\n東部即時用電量:{0[8]}萬瓩".format(powerax))
    a1="更新時間：{0[0]}\n北部即時用電量:{0[2]}萬瓩\n中部即時用電量:{0[4]}萬瓩\n南部即時用電量:{0[6]}萬瓩\n東部即時用電量:{0[8]}萬瓩".format(powerax)
    #print("參考資料:http://www.taipower.com.tw/TC/page.aspx?mid=206&cid=403&cchk=1f5269ec-633e-471c-9727-22345366f0be\n")
    poweraxx=float(powerax[2])+float(powerax[4])+float(powerax[6])+float(powerax[8])
    poweraxx=(round(poweraxx,1))#小數點第一位
    #print("全台及時總用電量",poweraxx)
    poweraxx="全台及時總用電量"+str(poweraxx)
    #print(poweraxx)
    #print(a1)
    u1="參考資料:http://www.taipower.com.tw/TC/page.aspx?mid=206&cid=403&cchk=1f5269ec-633e-471c-9727-22345366f0be\n"
    list_al.append(a1)
    list_al.append(poweraxx)
    list_al.append(u1)
    list_powerb=[]
    for powerbs in powerb:
        powerbs=powerb.strip("\r\n")
        list_powerb.append(powerbs)
        powerbss=powerbs.split()
    #print(powerbss[-1:])
    lastp=powerbss[-1:]

    for lastpp in lastp:
        lastpp=lastpp
        #print(lastpp)
    lastppp=lastpp.split(",")
    #print("日期：{0[0]}\n系統運轉淨尖峰供電能力:{0[1]}萬瓩\n系統瞬時尖峰負載(瞬時值):{0[2]}萬瓩\n備轉容量率:{0[3]}%".format(lastppp))
    a2="日期：{0[0]}\n系統運轉淨尖峰供電能力:{0[1]}萬瓩\n系統瞬時尖峰負載(瞬時值):{0[2]}萬瓩\n備轉容量率:{0[3]}%".format(lastppp)
    #print("參考資料:http://www.taipower.com.tw/TC/page.aspx?mid=206&cid=405&cchk=e1726094-d08c-431e-abee-05665ab1c974")
    u2="參考資料:http://www.taipower.com.tw/TC/page.aspx?mid=206&cid=405&cchk=e1726094-d08c-431e-abee-05665ab1c974"
    list_al.append(a2)
    list_al.append(u2)
    #print(list_al)
    return list_al

if __name__ == '__main__':
    power()
