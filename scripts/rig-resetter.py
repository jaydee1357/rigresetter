import json
import requests
import socket
import time
import datetime

def getToken(username, password, UUID):
    payload = {"method": "login",
               "params": {"appType": "Kasa_Android",
                          "cloudUserName": username,
                          "cloudPassword": password,
                          "terminalUUID" : UUID}}
    r = requests.post(url, data=json.dumps(payload))
    token = r.json()["result"]["token"]
    return (token)

def getDeviceID(token, rigname):
   getdevicesData = {"method": "getDeviceList"}
   r = requests.post(url + '?token=' + myToken, data=json.dumps(getdevicesData))
   res = r.json()["result"]["deviceList"]
   for device in res:
      if device["alias"]==rigName:
         return(device["deviceId"])

def getRigPowerUsage(token, request):
    r = requests.post(url + '?token=' + token, data=json.dumps(request))
    currentPower = json.loads(r.json()["result"]["responseData"])["emeter"]["get_realtime"]["power"]
    return (currentPower)

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

def getRigHashrate(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(30)
    try:
       s.connect((host, port))
       s.send('{"id":0,"jsonrpc":"2.0","method":"miner_getstat1"}'.encode("utf-8"))
       j=s.recv(2048)
       s.close()
       resp=json.loads(j.decode("utf-8"))
       resp=resp['result']
       hashes = int(resp[2].split(';')[0])
       return(hashes)
    except socket.error:
       return(0)

conf_file = open('config.json')
conf_json = json.load(conf_file)
UUID = conf_json["UUID"]
url = conf_json["json_url"]
username = conf_json["tp_link_username"]
password = conf_json["tp_link_password"]
rigs = conf_json["rigs"]
checkDelay = conf_json["check_delay"]
print(str(datetime.datetime.now()) + " --> " + "Requesting User Token")
myToken = getToken(username, password, UUID)
count = 0
rigCheckFailCount = 0

print("********************************************************************")

for rig in rigs:
   rigName = rig["rig_name"]
   rigHost = rig["rig_ip"]
   rigPort = rig["rig_port"]
   rigMinHashrate = rig["rig_min_hashrate"]
   rigMinPower = rig["rig_min_power_usage"]
   rigMaxPower = rig["rig_max_power_usage"]
   print(str(datetime.datetime.now()) + " --> " + "Requesting Device ID: " + rigName)
   myDeviceID = getDeviceID(myToken, rigName)
   print(str(datetime.datetime.now()) + " --> " + "Checking Rig Status: " + rigName)
   myRigPower = getRigPowerUsage(myToken, genRequest(myDeviceID, "emeter"))
   myRigHashrate = getRigHashrate(rigHost,rigPort)/1000
   print(str(datetime.datetime.now()) + " --> CHECK " + str(count+1) + ": " + rigName + " Power: " + str(myRigPower) + " W")
   print(str(datetime.datetime.now()) + " --> CHECK " + str(count+1) + ": " + rigName + " Hashrate: " + str(myRigHashrate) + " Mh/s")
   if (myRigHashrate <= rigMinHashrate) | (myRigPower <= rigMinPower) | (myRigPower >= rigMaxPower):
      while (count <= 4):
         time.sleep(checkDelay)
         myRigHashrate = getRigHashrate(rigHost,rigPort)
         myRigPower = getRigPowerUsage(myToken, genRequest(myDeviceID, "emeter"))
         print(str(datetime.datetime.now()) + " --> CHECK " + str(count+1) + ": " + rigName + " Power: " + str(myRigPower) + " W")
         print(str(datetime.datetime.now()) + " --> CHECK " + str(count+1) + ": " + rigName + " Hashrate: " + str(myRigHashrate) + " Mh/s")
         rigCheckFailCount = rigCheckFailCount + 1
         count = count + 1
      if rigLowHashrateCount == 5:
         print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter OFF")
         req = genRequest(myDeviceID, "off")
         print(str(datetime.datetime.now()) + " --> " + "Delay 30s before sending ON Signal")
         res = requests.post(url + '?token=' + myToken, data=json.dumps(req))
         time.sleep(30)
         req = genRequest(myDeviceID, "on")
         print(str(datetime.datetime.now()) + " --> " + "Turning TP-Link Adapter ON")
         res = requests.post(url + '?token=' + myToken, data=json.dumps(req))

print("********************************************************************")
