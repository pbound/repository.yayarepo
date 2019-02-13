# -*- coding: utf-8 -*-
import json, requests, urllib
from base64 import b64decode
func =''
baseurl = b64decode('aHR0cDovL2FwaXNlcnZpY2UucHNpc2F0LmNvbS9hcGkvUHNpQ2FyZS8=')
def getchadetail(id):
    url = baseurl+'GetChannelDetail'
    headers = {
            'username': 'PsiCare',
            'password': 'dq3JTzXfz9eMYvPW',
            'secretkey': '4jeMW5',
            'function': 'GetChannelDetail',
            }

    para = { 'bitrates': '300',
            'channel_id': id
              }

    r = requests.post(url,data=json.dumps(para), headers=headers)
    # print r.content
    jdata = r.json()
    ch_url = jdata['channel']['channel_url']
    return ch_url
def getstreams():
    url = baseurl+'GetAllChannelList'
    headers = {
               'username': 'PsiCare',
               'password': 'dq3JTzXfz9eMYvPW',
               'secretkey': '4jeMW5',
               'function': 'GetAllChannelList'
               }
    r = requests.post(url, data=json.dumps({}), headers=headers)
    jdata = r.json()
    chlist = jdata['channels']


    strmlist = []
    for ch in chlist:
        churl = ch['channel_id']
        strmlist.append({"url": str(churl) , "title": ch['channel_description'],'thumbnail':ch['channel_logo']})
    return strmlist


# get_tfch()
print getstreams()