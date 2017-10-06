import requests
import json
import time
import datetime
import socket

username = "jiten.dutia@gmail.com"
password = "@Asdf1234"
UUID = "592c6873-99db-4dc4-b57c-9941022693ca"
rigName = "Nvidia-Rig"
checkDelay = 5
rigDownCount = 0
rigLowHashrateCount = 0
count = 0
url = 'https://wap.tplinkcloud.com'
host='jaydee.duckdns.org'
port=3335

def getToken(username, password, UUID):
    payload = {"method": "login",
               "params": {"appType": "Kasa_Android", "cloudUserName": username, "cloudPassword": password,
                          "terminalUUID": UUID}}
    r = requests.post(url, data=json.dumps(payload))
    token = r.json()["result"]["token"]
    return (token)


def checkRig(token, request):
    r = requests.post(url + '?token=' + token, data=json.dumps(request))
    currentPower = json.loads(r.json()["result"]["responseData"])["emeter"]["get_realtime"]["power"]
    print(str(datetime.datetime.now()) + " --> " + rigName + ": Rig Power Intake =\033[32m " + str(currentPower) + "\033[0m W")
    if int(currentPower) <= 600:
        result = "DOWN"
    else:
        result = "ACTIVE"
    return (result)
def getDeviceID(token, rigname):
    getdevicesData = {"method": "getDeviceList"}
    r = requests.post(url + '?token=' + token, data=json.dumps(getdevicesData))
    deviceId = r.json()["result"]["deviceList"][1]["deviceId"]
    return (deviceId)


def genRequest(deviceID, request):
    commands = {'info': '{"system":{"get_sysinfo":{}}}',
                'on': '{"system":{"set_relay_state":{"state":1}}}',
                'off': '{"system":{"set_relay_state":{"state":0}}}',
                'cloudinfo': '{"cnCloud":{"get_info":{}}}',
                'wlanscan': '{"netif":{"get_scaninfo":{"refresh":0}}}',
                'time': '{"time":{"get_time":{}}}',
                'schedule': '{"schedule":{"get_rules":{}}}',
                'countdown': '{"count_down":{"get_rules":{}}}',
                'antitheft': '{"anti_theft":{"get_rules":{}}}',
                'reboot': '{"system":{"reboot":{"delay":1}}}',
                'reset': '{"system":{"reset":{"delay":1}}}',
                'emeter': '{"emeter":{"get_realtime":{}}}'
                }
    req = commands[request]
    return ({"method": "passthrough", "params": {"deviceId": deviceID, "requestData": req}})

print(str(datetime.datetime.now()) + " --> " + "Requesting User Token")
myToken = getToken(username, password, UUID)
print(str(datetime.datetime.now()) + " --> " + "Requesting Device ID")
myDeviceID = getDeviceID(myToken, rigName)
print(str(datetime.datetime.now()) + " --> " + "Checking RIG Status")
myRigStatus = checkRig(myToken, genRequest(myDeviceID, "emeter"))
print(str(datetime.datetime.now()) + " --> " + "Requesting Rig Hashrate")
myRigHashrate = getRigHashrate()
print(str(datetime.datetime.now()) + " --> RIG current hashrate is: \033[32m" + str(myRigHashrate/1000) + "\033[0m Mh/s")
print(str(datetime.datetime.now()) + " --> RIG is \033[32m" + myRigStatus + "\033[0m")
if (myRigHashrate/1000 < 145):
    print(str(datetime.datetime.now()) + " --> Rig Hash rate is below 145 threshold")
    while count <= 4:
        time.sleep(30)
        print(str(datetime.datetime.now()) + " --> Requesting current hashrate")
        myRigHashrate = getRigHashrate()
        print(str(datetime.datetime.now()) + " --> Current hashrate is : \033[32m" + str(myRigHashrate/1000) + "\033[0m Mh/s")
        rigLowHashrateCount = rigLowHashrateCount + 1
        count = count + 1
    if rigLowHashrateCount == 5:
        print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter OFF")
        req = genRequest(myDeviceID, "off")
        res = requests.post(url + '?token=' + myToken, data=json.dumps(req))
        print(str(datetime.datetime.now()) + " --> " + "Delay 30s before sending ON Signal")
        time.sleep(30)
        print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter ON")
        req = genRequest(myDeviceID, "on")
        res = requests.post(url + '?token=' + myToken, data=json.dumps(req))
count=0
if myRigStatus is "DOWN":
    print(str(datetime.datetime.now()) + " --> " + "Rig is \033[32m DOWN \033[0m . Check Rig status again in " + str(checkDelay) + "secs")
    while count <= 4:
        myRigStatus = checkRig(myToken, genRequest(myDeviceID, "emeter"))
        rigDownCount = rigDownCount + 1
        count = count + 1
        print("check " + str(count) + " : " + myRigStatus)
        time.sleep(checkDelay)
    print(str(datetime.datetime.now()) + " --> " + "Rig Online Status fail:" + str(rigDownCount))
    if rigDownCount == 5:
        print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter OFF")
        req = genRequest(myDeviceID, "off")
        res = requests.post(url + '?token=' + myToken, data=json.dumps(req))
        print(str(datetime.datetime.now()) + " --> " + "Delay 30s before sending ON Signal")
        time.sleep(30)
        print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter ON")
        req = genRequest(myDeviceID, "on")
        res = requests.post(url + '?token=' + myToken, data=json.dumps(req))
        
