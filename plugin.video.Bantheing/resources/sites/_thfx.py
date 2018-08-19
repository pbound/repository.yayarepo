# -*- coding: utf-8 -*-
import json, requests

url = 'http://38.37.unlimit-livestream.com:3000/user/tvShowShelf/liveShelf/getallcat'
response = requests.get(url)
todos = json.loads(response.text)
collections = todos['result']['collections']

def get_gen():
    for collec in collections:
        print collec['_id']
        print collec['name']['th']

def getstreams():
    strmlist = []
    for tstrm in collections:
        contents = tstrm['contents']
        for ch in contents:
            title = ch['name']['th']
            thumnail  = 'http://cdn.thflix.com/' + ch['poster']
            url = ch['liveUrl']
            strmlist.append({"url": url, "title": title, 'thumbnail': thumnail})
    return strmlist

