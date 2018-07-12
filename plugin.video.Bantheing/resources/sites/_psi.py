# -*- coding: utf-8 -*-
import json, requests, urllib
from base64 import b64decode

baseurl = b64decode('aHR0cDovL2xpdmUucHNpdHYudHYv')
def loadblance(host):
    url = baseurl+'curl_loadbalancer.php?host='+host[7:].replace('lb_box','lb')
    response = requests.get(url).content
    # print response
    return response.split('=')[1]

def getstreams():
    url = b64decode('aHR0cDovL3BzaXR2LnR2L2FwaS9DaGFubmVscw==')
    HEADERS = urllib.urlencode({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
                                'Referer': baseurl})
    response = requests.get(url)
    todos = json.loads(response.text)
    dictodo =todos['result']['channels']
    hosturl = loadblance(dictodo[0]['nodes'][0]['host'])
    folder = dictodo[0]['nodes'][0]['folder']

    strmlist = []
    for ch in dictodo:
        urlString = "http://" + hosturl + ":1935/" +folder+ "/" + ch['streamer'] + "_" + '600' + "/playlist.m3u8"
        churl = urlString + '|%s' % HEADERS
        strmlist.append({"url": churl, "title": ch['name'],'thumbnail':ch['logo']})
    return strmlist





# get_tfch()