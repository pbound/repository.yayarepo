# -*- coding: utf-8 -*-
import json
import re
from base64 import b64decode

import requests
from bs4 import BeautifulSoup

def get_chlist():
    url = b64decode('aHR0cDovL3d3dy5tdnR2LmNvLnRoL2lvcy9jaGFubmVsc19lcGcucGhw')
    r = requests.get(url).json()
    jdata = r['channels']
    chalist = []
    for i in jdata:
        url = i['stream']
        thumnail = i['icon']
        title = i['name']
    #
        chalist.append({"url": url, "title": title, 'thumbnail': thumnail})
    return chalist


# print get_chlist()