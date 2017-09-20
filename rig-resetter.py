import requests
import json
import time

username = "jiten.dutia@gmail.com"
password = "@Asdf1234"
UUID = "592c6873-99db-4dc4-b57c-9941022693ca"
rigName = "Rig1"
checkDelay = 120
rigDownCount = 0
count = 0
url = 'https://wap.tplinkcloud.com'

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
    if int(currentPower) <= 600:
        result = "DOWN"
    else:
        result = "UP"
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


myToken = getToken(username, password, UUID)
myDeviceID = getDeviceID(myToken, rigName)
myRigStatus = checkRig(myToken, genRequest(myDeviceID, "emeter"))
print(myRigStatus)

if myRigStatus is "DOWN":
    while count <= 4:
        myRigStatus = checkRig(myToken, genRequest(myDeviceID, "emeter"))
        rigDownCount = rigDownCount + 1
        count = count + 1
        print("check " + str(count) + " : " + myRigStatus)
        time.sleep(checkDelay)
    print(rigDownCount)
    if rigDownCount == 5:
        req = genRequest(myDeviceID, "off")
        requests.post(url + '?token=' + myToken, data=json.dumps(req))
        time.sleep(30)
        req = genRequest(myDeviceID, "on")
        requests.post(url + '?token=' + myToken, data=json.dumps(req))
