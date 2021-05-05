import requests
from requests.auth import HTTPBasicAuth
import json
from base64 import b64encode

userAndPass = b64encode(b"username:password").decode("ascii")

url = "https://my.iot-ticket.com/api/v1/process/write/xxxxxxxxxxxxxxxxxxxxxx"
#Example of payload  payload = [{"name":"testi2", "v":23, "path":"username/example2", "unit":"c"}]
headers = {"Content-Type": "application/json", "Authorization": "Basic %s" % userAndPass}

def ruuvitagsend(payloadin, state):
    #Send RuuviTAG sensor value and status to IOT-ticket
    payloadtemp = {"name":"temperature", "v":0, "path":"username/GreenHouse", "unit":"c"}
    payloadhumid = {"name":"humidity", "v":0, "path":"username/GreenHouse", "unit":"%"}
    payloadstatus = {"name":"operational", "v":0, "path":"username/GreenHouse", "unit":"boolean"}
    payloadtemp["v"] = payloadin["temperature"]
    payloadhumid["v"] = payloadin["humidity"]
    payloadstatus["v"] = state
    payloadout = [payloadtemp, payloadhumid, payloadstatus]
    r = requests.post(url, headers=headers, data=json.dumps(payloadout))
    print(r.status_code)
    if(r.ok):
        print("RuuviTag Temp send")
    else:
       #If response code is not ok (200), print the resulting http error code with description
        r.raise_for_status()

def templightsend(lightvalue, state):
    #Send light sensor value and status to IOT-ticket
    payloadlight = {"name":"temp_light_light", "v":0, "path":"username/GreenHouse", "unit":"lux"}
    payloadstatus = {"name":"temp_light_operational", "v":0, "path":"username/GreenHouse", "unit":"boolean"}
    payloadlight["v"] = lightvalue
    payloadstatus["v"] = state
    payloadout = [payloadlight, payloadstatus]
    r = requests.post(url, headers=headers, data=json.dumps(payloadout))
    print(r.status_code)
    if(r.ok):
        print("Temp/Light sensor data send")
    else:
       #If response code is not ok (200), print the resulting http error code with description
        r.raise_for_status()



