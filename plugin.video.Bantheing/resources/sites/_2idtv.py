# -*- coding: utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup

def get_chlist():
    url = 'https://dmpapi.trueid.net/cms-fnshelf/v1/gYNlz7OkBWp?fields=channel_code,thumb'#,subscription_package,subscription_tiers,subscriptionoff_requirelogin,is_premium,true_vision,slug,article_category,digital_no,catch_up,allow_catchup,time_shift,allow_timeshift,channel_info,teaser_channel,packages,drm,epg_flag'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
               'Authorization': 'Bearer 58d8d84e198c070b1a0b7d7bf4a70be4d9db446d64b717470c356e8a',
               }
    r = requests.get(url,headers=headers).json()
    print r
    jdata = r['data']['shelf_items']
    print len(jdata)
    chalist = []
    for i in jdata:
        id = i['id']
        img = i['thumb']
        title = i['title']
        churl ='https://dmpapi2.trueid.net/pk-streamer/v1/streamer?id='+id+'&appid=truetv&streamlvl=auto&langid=th'#&uid=49364413'

        chalist.append({"url": churl, "title": title ,'thumbnail':img})

    return chalist


def getsubstream(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Authorization': 'Bearer 5aaf9ade15afe0324400bacc98be816097bd42b2b5ccdc0f3475452c',
    }
    r = requests.get(url, headers=headers).json()
    jdata = r['data']
    streamurl = jdata['stream']['stream_url']
    streamlc = jdata['stream']['stream_license']
    return streamurl,streamlc




