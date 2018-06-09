# -*- coding: utf-8 -*-
import json,plugintools

import os
import requests
import sys
import xbmcgui
from bs4 import BeautifulSoup
from base64 import b64decode

baseurl = b64decode('aHR0cHM6Ly93d3cudml1LmNvbS9vdHQvdGgvaW5kZXgucGhw')
srbaseurl = b64decode('aHR0cHM6Ly93d3cudml1LmNvbS9vdHQvdGgvaW5kZXgucGhwP3I9dm9kL2FqYXgtZGV0YWlsJnBsYXRmb3JtX2ZsYWdfbGFiZWw9d2ViJmFyZWFfaWQ9NCZsYW5ndWFnZV9mbGFnX2lkPTQmcHJvZHVjdF9pZD0=')
fbaseurl = b64decode('aHR0cHM6Ly9kZnA2cmdsZ2pxc3prLmNsb3VkZnJvbnQubmV0L2luZGV4LnBocD9yPXYxL3NlYXJjaC92aWRlbyZsYW5ndWFnZV9mbGFnX2lkPTQ=')
stmbaseurl = b64decode('aHR0cHM6Ly9kMWsydXM2NzFxY29hdS5jbG91ZGZyb250Lm5ldC9kaXN0cmlidXRlX3dlYl90aC5waHA/Y2NzX3Byb2R1Y3RfaWQ9')
caturl = baseurl + '?r=category/series-category&platform_flag_label=web&area_id=4&language_flag_id=4&'
def getgenre():
    r = requests.get(baseurl)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('ul', {'class': "v-nav test"})
    li = ul.findAll('a', {'class': ''})
    seriesList = []
    # print (li)
    for link in li:
        catid = link.get('data-id')
        surl = caturl+'category_id=' + str(catid) + '&length=14'
        # print link.text.replace('\n', '')
        # print link.get('href')
        seriesList.append({'title': link.text.replace('\n', ''), 'url': surl})

    return seriesList



def getseries(url):
    response = requests.get(url)
    todos = json.loads(response.text)
    data = todos['data']['series']
    total = todos['data']['category_series_total'][0]['series_total']
    seriesList = []
    for serie in data:
        seurl = baseurl + '?r=vod/ajax-detail&platform_flag_label=web&area_id=4&language_flag_id=4&product_id='+str(serie['product_id'])
        # seurl = stmbaseurl +str(serie['product_id'])
        seriesList.append({'title':serie['name'], 'url': seurl,
                           'thumbnail': serie['cover_image_url']})

    next = getnext(url,total)
    if next != None:
        nurl = url + '&offset='+str(next)
        seriesList.append({'title': u"Next", 'url': nurl})
    return seriesList

def getepisode(url):
    # print url
    epurl = url[:-5]
    # print epurl
    response = requests.get(url)
    jdata = json.loads(response.text)
    # print todos == response.json()
    jseries = jdata['data']['series']
    episodes = jseries ['product']
    # print type(episodes)
    eplist = []
    for ep in episodes:
        url = epurl+ep['product_id']
        eplist.append({'title': ep['number']+'.'+ep['synopsis'] , 'url': url,
                           'thumbnail': ep['cover_image_url']})
    return eplist
def download_subtitle(url):
    dest = plugintools.get_temp_path() + 's.srt'
    fi = open(dest, "w")
    fi.write(plugintools.read(url))
    fi.close()

def getquality(url):
    response = requests.get(url)
    jdata = json.loads(response.text)
    qualist = jdata['data']['stream']['url']
    # print type(qualist)
    sourcelist = []
    for key in qualist:
        # print key
        # print qualist[key]
        sourcelist.append({"title": key[1:], "url": qualist[key]})

    return sourcelist






def getstreams(url,title=None):
    response = requests.get(url)
    jdata = json.loads(response.text)
    # print todos == response.json()
    curproduct = jdata['data']['current_product']
    # print len(curproduct)
    sub = curproduct['subtitle']
    # print len(sub)
    if sub != []:
        for s in sub:
            if s['is_default'] == 1:
                subtitleurl = s['url']
                download_subtitle(subtitleurl)
    else:
        del_sub()

    ccsproid = curproduct['ccs_product_id']
    # print 'ccs_product_id= ' + ccsproid
    qurl = stmbaseurl + ccsproid

    return getquality(qurl)

def getnext(url,total):
    offset = url.split('&')
    length = 12
    # offset = 26
    # offset = offset+length
    if 'offset' in  offset[-1]:
        offsetnum = offset[-1].split('=')[-1]
        offsetnum = int(offsetnum)+12

    else:
        offsetnum = 26
    print offsetnum

    if offsetnum <= total:
        return offsetnum

def del_sub():
    try:
        os.remove(plugintools.get_temp_path() + 's.srt')
    except OSError:
        None

def getsearch(arg):
    url = baseurl+'?r=vod/jsonp'
    payload = {"platform_flag_label":"web","limit":12,"page":1}
    payload['url'] = fbaseurl
    payload["keyword"]=arg
    headers = {'content-type': 'application/json'}
    source = requests.post(url, data=json.dumps(payload), headers=headers).json()
    sresult = source['data']['series']
    sourcelist = []
    if sresult !=[]:
        for result in sresult:
            sourcelist.append({"title": result['name'], "url": srbaseurl+result['product_id'],'thumbnail':result['cover_image_url']})

    return sourcelist
