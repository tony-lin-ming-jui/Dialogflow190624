from flask import Flask,render_template,request,redirect,url_for,session,g,escape,Markup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#from linebot.exceptions import *
from linebot.models import *
#from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
import requests
from bs4 import BeautifulSoup
import apiai


import base64
from matplotlib.font_manager import FontProperties
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import io
import json
import pandas

import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

import random
import song_crawler
import apple
import movie_crawler
import invoice_pic_crawler
import radar_crawler
import Sticker_random
import rainfall_pic_crawler
import Satellite_pic_crawler
import weather_data
import oil_crawler_n_office
import oil_crawler_tw_new
import work_class_cancel_crawler
import work_class_cancel_crawler_notebook
import PTQS1005
import oil_crawler_of
import power_crawler_office
import reservoir_crawler

import pymysql
import os
import re

from pygame import mixer

import sys
app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)


#ESLAB小幫手
line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')
#ESlab
#line_bot_api = LineBotApi('Channel access token')
#handler = WebhookHandler('Channel secret')

webhook_url="https://6eba627d.ngrok.io"



#DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')

#DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ.get('7f8bab4149d74f52bc0e41a4f7cacae9')
CLIENT_ACCESS_TOKEN ='7f8bab4149d74f52bc0e41a4f7cacae9'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)



scheduler = BlockingScheduler()


#db = pymysql.connect("127.0.0.1","root","1qaz1qaz","linesss",charset="utf8" )
db = pymysql.connect("127.0.0.1","root","1qaz1qaz","line_db",charset="utf8" )
cursor = db.cursor()

@app.route("/voice")
def voice():
    #print("aaaaaaaaa",a)
    #if a:
    return render_template('voice.html')
@app.route('/plots')  
def oilweb():
    #if a:
    return render_template('oilweb.html')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    #sched = BlockingScheduler()
    #sched.add_job(t1, 'interval', seconds=10)#這裡設定時間，只有在第一次傳送訊息後 才會開始主動回訊息
    #sched.start()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    print("event.source.user_id:", event.source.user_id)
    ai_request = ai.text_request()
    #ai_request.lang = "en"
    #ai_request.lang = "zh-tw"
    #ai_request.session_id = event.source.user_id
    if re.findall('目前',event.message.text):
        ai_request.lang = "zh-tw"
        ai_request.session_id = event.source.user_id
        ai_request.query = event.message.text.replace('目前','今天')
        #print(event.message.text.replace('目前','今天'))
    elif re.findall('現在',event.message.text):
        ai_request.lang = "zh-tw"
        ai_request.session_id = event.source.user_id        
        ai_request.query = ai_request.query = event.message.text.replace('現在','今天')
    elif event.message.text == '停':
        mixer.music.stop()                
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已停止播放"))    
    else:
        ai_request.lang = "zh-tw"
        ai_request.session_id = event.source.user_id
        ai_request.query = event.message.text
    #ai_request.query = event.message.text
    ai_response = json.loads(ai_request.getresponse().read())
    user_intent=ai_response['result']['metadata']['intentName']
    #ai_res = ai_response.get_json(silent=True, force=True)
    #print("result",result)
    #user_intent = ai_response['result']['metadata']['intentName']
    print("ai_response",ai_response)
    #print("ai_response的action",ai_response['result']['action'])
    print("user_intent",user_intent)
    #print("user_intent",user_intent)
    #print("ai_response的taiwan-city",ai_response['result']['taiwan-city'])
    #print("結果",ai_res.get("result").get("action"))
    if user_intent == 'weather_ask':
        client=event.source.user_id
        speech=ai_response['result']['fulfillment']['speech']
        if speech!="":
            try:
                print("speech",speech)
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+speech+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/hello.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/hello.m4a')
                mixer.music.play()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=speech))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hello.m4a', duration=300000))
            except:
                print("speech",speech)
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+speech+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/hellos.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/hellos.m4a')
                mixer.music.play()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=speech))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hellos.m4a', duration=300000))
                
        else:            
            today = datetime.now()
            date_nows = today.strftime('%Y-%m-%d')
            print("date_nows",date_nows)
            day_ask=''.join(ai_response['result']['parameters']['date'])
            locat_ask=''.join(ai_response['result']['parameters']['taiwan-city'])
            print("時間",day_ask)
            print("地點",locat_ask)
            weather=weather_data.weather()
            if day_ask!=date_nows:
                msg="我只能告訴你今天的天氣QQ"
                try:                    
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+msg+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('staticsss/todaywsss.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('staticsss/todaywsss.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticsss/todaywsss.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+msg+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statica/todaywa.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statica/todaywa.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statica/todaywa.m4a', duration=300000))    
            else:
                if locat_ask =='台北':                    
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Taipei.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Taipei.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Taipeis.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Taipeis.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taipeis.m4a', duration=300000))

                elif locat_ask =='新北':                    
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/NTaipei.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/NTaipei.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/NTaipei.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/NTaipeis.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/NTaipeis.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/NTaipeis.m4a', duration=300000))

                elif locat_ask =='桃園':                    
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Taoyuan.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Taoyuan.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taoyuan.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Taoyuans.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Taoyuans.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taoyuans.m4a', duration=300000))

                elif locat_ask =='新竹':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Hsinchu.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Hsinchu.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hsinchu.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Hsinchus.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Hsinchus.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hsinchus.m4a', duration=300000))

                elif locat_ask =='苗栗':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Miaoli.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Miaoli.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Miaoli.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Miaolis.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Miaolism4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Miaolis.m4a', duration=300000))

                elif locat_ask =='台中':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Taichung.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Taichung.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taichung.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Taichungs.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Taichungs.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taichungs.m4a', duration=300000))

                elif locat_ask =='彰化':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Changhua.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Changhua.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Changhua.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Changhuas.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Changhuas.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Changhuas.m4a', duration=300000))
                elif locat_ask =='南投':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Nantou.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Nantou.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Nantou.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Nantous.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Nantous.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Nantous.m4a', duration=300000))

                elif locat_ask =='雲林':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Yunlin.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Yunlin.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yunlin.m4a', duration=300000))
                    except:        
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Yunlins.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Yunlins.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yunlins.m4a', duration=300000))

                elif locat_ask =='嘉義':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Chiayi.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Chiayi.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Chiayi.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Chiayis.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Chiayis.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Chiayis.m4a', duration=300000))

                elif locat_ask =='宜蘭':
                    try:                
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Yilan.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Yilan.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yilan.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Yilans.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Yilans.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yilans.m4a', duration=300000))

                elif locat_ask =='花蓮':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Hualie.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Hualie.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hualie.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Hualies.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Hualies.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hualies.m4a', duration=300000))

                elif locat_ask =='台東':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Taitung.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Taitung.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taitung.m4a', duration=300000))        
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Taitungs.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Taitungs.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taitungs.m4a', duration=300000))        

                elif locat_ask =='台南':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Tainan.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Tainan.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Tainan.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Tainans.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Tainans.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Tainans.m4a', duration=300000))

                elif locat_ask =='高雄':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Kaohsiung.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Kaohsiung.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kaohsiung.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Kaohsiungs.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Kaohsiungs.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Kaohsiungs.m4a', duration=300000))

                elif locat_ask =='屏東':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Pingtung.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Pingtung.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Pingtung.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Pingtungs.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Pingtungs.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Pingtungs.m4a', duration=300000))

                elif locat_ask =='連江':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Lienchiang.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Lienchiang.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Lienchiang.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Lienchiangs.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Lienchiangs.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Lienchiangs.m4a', duration=300000))

                elif locat_ask =='金門':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Kinmen.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Kinmen.m4a')
                        mixer.music.play()        
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmen.m4a', duration=300000))
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Kinmens.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Kinmens.m4a')
                        mixer.music.play()        
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmens.m4a', duration=300000))

                elif locat_ask =='澎湖':
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/Penghu.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/Penghu.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Penghu.m4a', duration=300000))        
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/Penghus.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/Penghus.m4a')
                        mixer.music.play()
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Penghus.m4a', duration=300000))        

                
            #print("開始抓天氣啦")
            #print("speech",ai_response['result']['fulfillment']['speech'])
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mes))
    elif user_intent == 'oil_ask':
        speech=ai_response['result']['fulfillment']['speech']
        client=event.source.user_id
        if speech!="":
            confirm_template_message = TemplateSendMessage(
            alt_text='Confirm alt text',
            template=ConfirmTemplate(text='油價資訊選擇', 
            actions=[
                MessageAction(label='國際油價', text='國際油價'),
                MessageAction(label='國內油價', text='國內油價'),
            ]))
            line_bot_api.reply_message(event.reply_token, confirm_template_message)       
        else:
            whereoil=''.join(ai_response['result']['parameters']['whereoil'])
            if whereoil=='國內':                
                mes="\n參考資料:https://gas.goodlife.tw/"
                oil=oil_crawler_tw_new.oil()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+oil+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/oil.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(2048):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/oil.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=oil+mes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oil.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+oil+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/oils.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/oils.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=oil+mes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oils.m4a', duration=300000))

            elif whereoil=='國際':
                
                img = io.BytesIO()
                oilof=oil_crawler_of.oilof()
                #oilof=oilof()
                #print(oilof)
                #print(list_oildate)

                list_oildate=oilof[:31]
                list_oildata=oilof[-93:]

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
                #print("======================================================================================")
                #print(jd)
                
                df=pandas.DataFrame(jd)
                df.columns = ['西德州','北海布蘭特','杜拜']

                list_r=list_oildata[0:93:3]
                list_g=list_oildata[1:93:3]
                list_b=list_oildata[2:93:3]

                #print(list_r)

                plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
                plt.rcParams['axes.unicode_minus'] = False
                plt.cla()
                plt.xticks(arange(len(list_oildate)),list_oildate)
                plt.plot(list_r,'o-',color='deeppink', label=u'西德州')
                plt.plot(list_g,'o-',color='#ADFF2F', label=u'北海布蘭特')
                plt.plot(list_b,'o-',color='deepskyblue', label=u'杜拜')
                #將數字顯示在圖上
                c = np.arange( len (list_oildate))
                for x1, y1 in zip(c,list_r ): 
                    plt.text(x1, y1 , '%.2f' % y1, ha= 'center' , va= 'bottom' )
                for x2, y2 in zip(c,list_g ): 
                    plt.text(x2, y2 , '%.2f' % y2, ha= 'center' , va= 'bottom' )
                for x3, y3 in zip(c,list_b ): 
                    plt.text(x3, y3 , '%.2f' % y3, ha= 'center' , va= 'bottom' )

                plt.xlabel(u'月/日')
                plt.ylabel(u'美元/桶')
                plt.legend(loc='upper left')#寫完 label要再加這行才會顯示例
                plt.gcf().set_size_inches(20,10)

                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()

                image_64_decode = base64.b64decode(plot_url)

                with open('static/oil.jpg', 'wb') as out_file:
                    out_file.write(image_64_decode)

                print("oilof",oilof[30])
                oilofmth=re.findall('([0-9]+)/[0-9]+',oilof[30])
                oilofday=re.findall('[0-9]+/([0-9]+)',oilof[30])
                print("oilofmth",oilofmth[0])
                print("oilofday",oilofday[0])
                m=str(oilofmth[0])+"月"+str(oilofday[0])+"日的國際油價:\n西德州:"+str(oilof[-3])+"美元\每桶\n北海布蘭特:"+str(oilof[-2])+"美元\每桶\n杜拜:"+str(oilof[-1])+"美元\每桶\n"
                #m=str(oilof[30])+"的國際油價:\n西德州:"+str(oilof[-3])+"美元\每桶\n北海布蘭特:"+str(oilof[-2])+"美元\每桶\n杜拜:"+str(oilof[-1])+"美元\每桶\n"
                u="參考資料:https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
                print(m+u)
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+m+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/nationoil.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/nationoil.m4a')
                    mixer.music.play()
                    line_bot_api.push_message(client,ImageSendMessage(original_content_url=webhook_url+"/static/oil.jpg", preview_image_url=webhook_url+"/static/oil.jpg"))
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m+u))        
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/nationoil.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+m+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/nationoils.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/nationoils.m4a')
                    mixer.music.play()
                    line_bot_api.push_message(client,ImageSendMessage(original_content_url=webhook_url+"/static/oil.jpg", preview_image_url=webhook_url+"/static/oil.jpg"))
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m+u))        
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/nationoils.m4a', duration=300000))
    elif user_intent == 'help_ask':
        client=event.source.user_id
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，如只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="你可以把我加入群組讓大家一起使用^^，另外傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oInstruction.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )         
            
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="你可以把我加入群組讓大家一起使用^^，另外傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oInstructions.m4a', duration=300000))
    elif user_intent == 'news_ask':
        client=event.source.user_id
        a=apple.apple_news()
        news_title=[]
        news_link=[]
        news_photo=[]    
        for i in range(0,len(a),3):   
            news_title.append(a[i])
            news_link.append(a[i+1])
            news_photo.append(a[i+2])

        news_group=[]    #創一個List
        #將剛剛的三個List加進來
        news_group.append(news_title)
        news_group.append(news_link)
        news_group.append(news_photo)
        #要做為key值的List
        x=['title','link','link2']
        #把兩個做成dictionary
        print("新聞幾個",len(news_title))
        dictionary = dict(zip(x,news_group))
        p=random.sample(range(len(news_title)),len(news_title))
        if len(news_title)>=10:
            try:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]+"第7"+dictionary['title'][p[6]]+"第8"+dictionary['title'][p[7]]+"第9"+dictionary['title'][p[8]]+"第10"+dictionary['title'][p[9]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/news.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(10000):
                            if block:
                                f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/news.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[6]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[6]],
                        label=dictionary['title'][p[6]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[7]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[7]],
                        label=dictionary['title'][p[7]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[8]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[8]],
                        label=dictionary['title'][p[8]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[9]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[9]],
                        label=dictionary['title'][p[9]][0:11]
                        )
                    )                
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/news.m4a', duration=300000))
            except:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]+"第7"+dictionary['title'][p[6]]+"第8"+dictionary['title'][p[7]]+"第9"+dictionary['title'][p[8]]+"第10"+dictionary['title'][p[9]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('staticss/newsss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(10000):
                            if block:
                                f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('staticss/newsss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[6]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[6]],
                        label=dictionary['title'][p[6]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[7]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[7]],
                        label=dictionary['title'][p[7]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[8]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[8]],
                        label=dictionary['title'][p[8]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[9]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[9]],
                        label=dictionary['title'][p[9]][0:11]
                        )
                    )                
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticss/newsss.m4a', duration=300000))
        else: #if len(news_title)<10 and len(news_title)>=6: else:
            try:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/newss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(4096):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/newss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    )
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/newss.m4a', duration=300000))
            except:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('staticsss/newssss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(4096):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('staticsss/newssss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    )
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticsss/newssss.m4a', duration=300000))        
    elif user_intent == 'invoice_ask':
        client=event.source.user_id
        speech=ai_response['result']['fulfillment']['speech']
        if speech!="":
            confirm_template_message = TemplateSendMessage(
            alt_text='Confirm alt text',
            template=ConfirmTemplate(text='發票期別選擇', 
            actions=[
                MessageAction(label='本期發票', text='本期發票'),
                MessageAction(label='上期發票', text='上期發票'),
            ]))
            line_bot_api.reply_message(event.reply_token, confirm_template_message)       

        else:
            invoice_time=''.join(ai_response['result']['parameters']['invoice-time'])
            print(invoice_time)
            if invoice_time=='本期':
                invoice=invoice_pic_crawler.invoice()
                print("invoice",invoice)
                line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=invoice[0], preview_image_url=invoice[0]))
            elif invoice_time=='上期':
                invoice=invoice_pic_crawler.invoice()
                print("invoice",invoice)
                line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=invoice[1], preview_image_url=invoice[1]))    
    elif user_intent == 'workclasscancel_ask':
        client=event.source.user_id
        speech=ai_response['result']['fulfillment']['speech']
        cancel=work_class_cancel_crawler_notebook.wkncls()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+cancel[0]+cancel[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/classcancel.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/classcancel.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cancel[0]+"\n"+cancel[1]+cancel[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/classcancel.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+cancel[0]+cancel[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/classcancels.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/classcancels.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cancel[0]+"\n"+cancel[1]+cancel[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/classcancels.m4a', duration=300000))
        

    elif user_intent == 'sensor_ask':
        client=event.source.user_id
        speech=ai_response['result']['fulfillment']['speech']
        if speech!="":
            mes='歡迎來404實驗室點擊PM 2點5，揮發性有機物，甲醛，二氧化碳，溫度，相對濕度，即可得到室內資訊'
            try:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/lab.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/lab.m4a')
                mixer.music.play()

                carousel_template_message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='歡迎來到404實驗室',
                                text='PM2.5、揮發性有機物、甲醛',
                                actions=[
                                    MessageAction(label='PM2.5', text='實驗室PM2.5'),
                                    MessageAction(label='揮發性有機物', text='實驗室揮發性有機物'),
                                    MessageAction(label='甲醛', text='實驗室甲醛')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='歡迎來到404實驗室',
                                text='二氧化碳、溫度、濕度',
                                actions=[
                                    MessageAction(label='二氧化碳', text='實驗室二氧化碳'),
                                    MessageAction(label='溫度', text='實驗室溫度'),
                                    MessageAction(label='相對濕度', text='實驗室相對濕度')
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/lab.m4a', duration=300000))
            except:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/labs.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/labs.m4a')
                mixer.music.play()

                carousel_template_message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='歡迎來到404實驗室',
                                text='PM2.5、揮發性有機物、甲醛',
                                actions=[
                                    PostbackAction(label='PM2.5', data='PM2.5'),
                                    PostbackAction(label='揮發性有機物', data='揮發性有機物'),
                                    PostbackAction(label='甲醛', data='甲醛')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='歡迎來到404實驗室',
                                text='二氧化碳、溫度、濕度',
                                actions=[
                                    PostbackAction(label='二氧化碳', data='二氧化碳'),
                                    PostbackAction(label='溫度', data='溫度'),
                                    PostbackAction(label='相對濕度', data='相對濕度')
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/labs.m4a', duration=300000))

        else:
            lab_sensor=''.join(ai_response['result']['parameters']['lab_sensor'])
            if lab_sensor=='pm2.5':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/PM25.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/PM25.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PM25.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值 "+PTQS[0]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/PM25s.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/PM25s.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PM25s.m4a', duration=300000))

            elif lab_sensor=='揮發性有機物':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/TVOC.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/TVOC.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/TVOC.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/TVOCs.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/TVOCs.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/TVOCs.m4a', duration=300000))

            elif lab_sensor=='甲醛':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/HCHO.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/HCHO.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/HCHO.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/HCHOs.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/HCHOs.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/HCHOs.m4a', duration=300000))

            elif lab_sensor=='二氧化碳':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/CO2.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/CO2.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/CO2.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/CO2s.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/CO2s.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/CO2s.m4a', duration=300000))
            elif lab_sensor=='濕度':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/hum.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/hum.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hum.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/hums.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/hums.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hums.m4a', duration=300000))
       
            elif lab_sensor=='溫度':
                PTQS=PTQS1005.ptq()
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/tem.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/tem.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/tem.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/tems.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/tems.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/tems.m4a', duration=300000))



    else: # 聽不懂時的回答
        msg = "我聽不懂你再講什麼，覺的桑心難過"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run(port=9000,debug =True)
