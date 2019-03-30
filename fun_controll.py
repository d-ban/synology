import requests
import json

synoUrl = 'http://x.x.me:5000'
username = 'xxx'
passwd = 'xxxx'


def auth():
    url = synoUrl + "/webapi/auth.cgi"
    payload = "api=SYNO.API.Auth&method=login&version=2&account=" + \
        username + "&passwd=" + passwd + "&session=session430623482&format=sid"
    response = requests.request("POST", url, data=payload)
    json_data = json.loads(response.text)
    sid = json_data['data']['sid']
    storeSid = open("sid.txt", "w")
    storeSid.write(sid)
    storeSid.close()
    print sid
    return sid


def sys_temp(sid):
    url = synoUrl + "/webapi/entry.cgi"
    payload = "api=SYNO.Core.System&method=info&version=2&_sid=" + sid
    response = requests.request("POST", url, data=payload)
    json_data = json.loads(response.text)
    if json_data['success']:
        sys_temp = json_data['data']['sys_temp']
        return sys_temp
    else:
        auth()


def sys_temp_storage(sid):
    url = synoUrl + "/webapi/entry.cgi"
    payload = "api=SYNO.Core.System&method=info&type=storage&version=2&_sid=" + sid
    response = requests.request("POST", url, data=payload)
    json_data = json.loads(response.text)
    if json_data['success']:
        sys_temp = json_data['data']['hdd_info'][0]['temp']
        return sys_temp
    else:
        auth()


def fullfan(sid):
    url = synoUrl + "/webapi/entry.cgi"
    payload = "mode=sequential&api=SYNO.Entry.Request&method=request&version=1&compound=%5B%7B%0A%20%20%22api%22%3A%20%22SYNO.Core.Hardware.FanSpeed%22%2C%0A%20%20%22method%22%3A%20%22set%22%2C%0A%20%20%22version%22%3A%20%221%22%2C%0A%20%20%22dual_fan_speed%22%3A%20%22fullfan%22%0A%7D%5D&_sid=" + sid
    response = requests.request("POST", url, data=payload)
    json_data = json.loads(response.text)
    if json_data['success']:
        return json_data['success']
    else:
        auth()


def coolfan(sid):
    url = synoUrl + "/webapi/entry.cgi"
    payload = "mode=sequential&api=SYNO.Entry.Request&method=request&version=1&compound=%5B%7B%0A%20%20%22api%22%3A%20%22SYNO.Core.Hardware.FanSpeed%22%2C%0A%20%20%22method%22%3A%20%22set%22%2C%0A%20%20%22version%22%3A%20%221%22%2C%0A%20%20%22dual_fan_speed%22%3A%20%22coolfan%22%0A%7D%5D&_sid=" + sid
    response = requests.request("POST", url, data=payload)
    json_data = json.loads(response.text)
    if json_data['success']:
        return json_data['success']
    else:
        auth()


try:
    with open('sid.txt') as f:
        key = f.readlines()
        sid = key[0]
        sys_temp_storage = sys_temp_storage(sid)
        if sys_temp_storage > 30:
            fullfan(sid)
        else:
            coolfan(sid)
        print sys_temp_storage
        print sys_temp(sid)
except Exception as e:
    auth()
