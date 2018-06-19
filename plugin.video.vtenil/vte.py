# -*- coding: utf-8 -*-
import json,plugintools
import os
import re
import requests
import xbmcaddon
from bs4 import BeautifulSoup
from base64 import b64decode
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonpath= addon.getAddonInfo('path')
nextimg =  addonpath + r'\icon.png'

baseurl = b64decode('aHR0cHM6Ly90di5saW5lLm1l')
s_baseurl = b64decode('aHR0cHM6Ly9nbG9iYWwtbnZhcGlzLmxpbmUubWUvbGluZXR2L3JtY25tdi92b2RfcGxheV92aWRlb0luZm8uanNvbj9rZXk9')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0','referer':baseurl}
def getgenre():
    r = requests.get(baseurl)
    r.encoding = "utf-8"
    respon = re.findall('<a href="(.c.\w.*?)".*ent.*\s><em>(.*?)<',r.text)
    # print respon
    seriesList = []
    # print (li)
    for link in respon:
    #     catid = link.get('data-id')
        surl = baseurl+link[0]+'/channels/1'
        # print link.text.replace('\n', '')
        # print link.get('href')
        seriesList.append({'title': link[1], 'url': surl})
    #
    return seriesList

def getseries(url):
    r = requests.get(url,headers=headers).text
    # print r.content
    data  = re.findall('data-src="(.*?).ty.*alt="(.*?)".*\n.*\n.*\n.*\n.*\n.*href=.(.*?).\s', r)
    # print data
    seriesList = []
    for serie in data:
        # seurl = baseurl +str(serie[2])
        seriesList.append({'title':serie[1], 'url': serie[2],
                           'thumbnail': serie[0]})

    next = bool(re.search('data-moreyn="true"',r))
    if next is True:
        num = int(url.split('/')[-1])+1
        nurl = url[:int(url.rfind('/'))+1] + str(num)
        # plugintools.message('nexturl',str(nurl))
        seriesList.append({'title': u"Next", 'url': nurl,'thumbnail':nextimg})
    return seriesList

def getepisode(url):
    i  =  0
    epurl = baseurl + '/api/html/channel' + url + '/playlists/0/'
    eplist = []
    while True:
        i += 1
        new_url =epurl + str(i)
        # print url
        response = requests.get(new_url,headers=headers).text
        # print response
        episodes = re.findall('a href="(.*?)".*\n.*\n.*data-src="(.*?)"?ty.*alt="(.*?)"',response)
        if episodes == []:
            break

        for ep in episodes:

            # print ep[0]
        #     print [ep[2]
            surl = baseurl + ep[0]
            # print surl
            eplist.append({'title': ep[2] , 'url': surl,
                               'thumbnail': ep[1]})
    return eplist


def download_subtitle(url):
    dest = plugintools.get_temp_path() + 's.srt'
    fi = open(dest, "w")
    fi.write(plugintools.read(url))
    fi.close()


def getstreams(url,title=None):
    response = requests.get(url).text
    vid_key = re.findall("videoId:.'(.*?)',*\s.*\s.*?key:.'(.*?)'",response)
    # print len(vid_key)

    vid = vid_key[0][0]
    key = vid_key[0][1]
    surl = s_baseurl+key+'&videoId=' + vid +'&cc=TH&sm=linetv'
    # print surl
    sponse = requests.get(surl,headers=headers).text
    jdata = json.loads(sponse)
    vdolist = jdata['videos']['list']

    try:
        sub = jdata['captions']['list'][0]['source']
        download_subtitle(sub)
        # print sub
    except:
        del_sub()
        # None

    strmlist = []
    for v  in vdolist:
        stitle= v['encodingOption']['name']
        surl = v['source']
        strmlist .append({'title':stitle, 'url':surl})
    return strmlist
    # print todos == response.j


def del_sub():
    try:
        os.remove(plugintools.get_temp_path() + 's.srt')
    except OSError:
        None

def getsearch(arg):
    url = baseurl+'/search?query='+arg
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html5lib')
    soup.prettify()
    # print r
    div  = soup.find('div',{'id':'section_channelsearch'})
    # print div
    sresult = div.findAll('div',{'class':'ch_item'})
    sourcelist = []
    if sresult !=[]:
        for result in sresult:
            titel = result.find('h4').find('a').text.strip()
            surl = result.find('a').get('href')
            img = result.find('img').get('src')
            sourcelist.append({"title": titel, "url": surl,'thumbnail':img})

    return sourcelist
