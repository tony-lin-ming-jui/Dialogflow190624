import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    #print(json.dumps(req, indent=4))
    print(req)
    res = makeWebhookResult(req)
    print("res:",res)
    res = json.dumps(res, indent=4)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    #askweather的地方是Dialogflow>Intent>Action 取名的內容
    print("天氣",req.get("queryResult").get("action"))
    if req.get("queryResult").get("action")!= "天氣如何":
        return {}
    result = req.get("queryResult")
    print("結果",result)
    parameters = result.get("parameters")
    #parameters.get("weatherlocation")的weatherlocation是Dialogflow > Entitiy
    #也就是步驟josn格式中parameters>weatherlocation
    zone = parameters.get("taiwan-city")
    print("zone",zone)
    #先設定一個回應
    #如果是Taipei,cost的位置就回應18
    cost = {'台北':'18', '高雄':'20', '台中':'10','台南':'25'}
    if zone[0]=='台北':
        speech = "今天台北溫度 " + str(zone[0]) + "是18度C"
        print("A")
    #speech就是回應的內容
    #print("str(cost[zone]")
    #speech = "The temperatrue of " + str(zone) + " is " + str(cost[zone])
        #print("Response:")
        #print(speech)
        return{
            "fulfillmentText": speech,
        }
                

     
    elif zone[0]=='高雄':
        speech = "The temperatrue of " + str(zone[0]) + "是20度C"
        return {
            "fulfillmentText": speech,
            #"speech": speech,
            #"displayText": speech,
            #"data": {},
            #"contextOut": [],
            #"source": "agent"
        }
    elif zone[0]=='台中':
        speech = "The temperatrue of " + str(zone[0]) + "是10度C"
        return{
            "fulfillmentText": speech,
        }
    elif zone[0]=='台南':
        speech = "The temperatrue of " + str(zone[0]) + "是25度C"

        return{
            "fulfillmentText": speech,
        }
    #回傳
 

if __name__ == "__main__":
    app.run(debug=True,port=9000)
