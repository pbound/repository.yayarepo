# -*- coding: utf-8 -*-
import json
import re
from base64 import b64decode

import requests
from bs4 import BeautifulSoup

def get_chlist():
    url = b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3Bib3VuZC9yZXBvc2l0b3J5LnlheWFyZXBvL21hc3Rlci9sb294')
    r = requests.get(url)
    ddata=b64decode(r.text)
    # print type(ddata)
    # data = json.dumps(ddata)  # dict to string
    jdata = json.loads(ddata)  # string to json
    chalist = []
    for p in jdata['data']:
        title = p['nam_channel_th']
        thumnail = p['channel_image']
        url= p['url_live'] + '?uuid=1eaebbc3-9af0-4d24-9c87-dd47236793e8&device=android'

#
        chalist.append({"url": url, "title": title, 'thumbnail': thumnail})
    return chalist



# if __name__ == '__main__':
#     print get_chlist()
print get_chlist()