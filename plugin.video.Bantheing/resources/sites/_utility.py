# -*- coding: utf-8 -*-
import HTMLParser
import json
import os

import sys

import re
import requests
import xbmcaddon
import xbmcgui
from bs4 import BeautifulSoup

addon = xbmcaddon.Addon()
addoname = addon.getAddonInfo('name')
addonid = addon.getAddonInfo('id')
addonpath= addon.getAddonInfo('path')
tmpjson= addonpath+r'\lib\btjson'
numword = (('zero','0'),('two','2'),('nine','9'))
webseries = ('utaseries','kseries', 'series-onlines','fanseries','seriesgamo','doonee')
def name2site(word):
    for nw in numword:
        s = nw[0]
        if s in word:
            sname = word.replace(nw[0],nw[1]).replace('_','-')
            break

        else:
            sname = word.replace('_','-')
    return sname.split('.')[0]

def site2name(num):
    for n in numword:
        if  n[1] ==num[0]:
            rsite = num.replace(n[1],n[0]).replace('-','_')
            break
        else:
            rsite = num.replace('-','_')
    return rsite.lower()


def y_soup(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    return soup

def y_reguests(url, regex = None, referer = None):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': referer}
    r = requests.get(url, headers=headers).text
    r = HTMLParser.HTMLParser().unescape(r)
    # print '*'*50
    # print r
    match = re.compile(regex).findall(r)
    if len(match) > 0:
        return match

def y_sites():
    os.chdir("..")
    pt = os.path.abspath(os.curdir) + '/sites'
    print pt

    # pt = sys.path[0] + '/hosts'
    # pt = addonpath  + '/hosts'
    items = os.listdir(pt)
    # print items
    # items = os.listdir()
    newlist = []
    for names in items:
        if names.endswith(".py") and not names.startswith('_'):
            names = names.split('.')[0]
            newlist.append(names)
    return newlist


def getnext(url):

    nextreg1 ='href="([^"]+page\/.*?\/)">'
    nextreg2 = 'href="([^"]+)">Next'
    nextreg3 = 'next..href="([^"]+)">'
    nextreg4 = 'next.*?href="([^"]+)">'

    nextreg = (nextreg1,nextreg2,nextreg3,nextreg4)
    for txt in nextreg:
        matchnext = y_reguests(url,regex=txt)
        # print matchnext
        # print len(matchnext)
        if matchnext != None:
            if  len(matchnext)== 1:
                return matchnext
                break
            else:
                matchnext = []
                return matchnext






def importsite(url,youget,title=None):
    # xbmcgui.Dialog().ok('url', url)
    sitename = getsitename(url)
    # xbmcgui.Dialog().ok('url', sitename)
    exec 'from resources.sites.' + sitename + ' import ' + youget
    # while True:
    if youget =='getmov':
        return getmov(url)
    elif youget == 'getgenre':
        return getgenre()
    elif youget == 'getstreams':
        return getstreams(url,title)
    elif youget == 'getsearch':
        return getsearch(title)
    elif youget == 'getsearchall':
        return getsearchall(title)

    elif youget == 'getseries':
        return getseries(url)
    elif youget == 'getepisode':
        return getepisode(url)



def is_series(name):
    if name in webseries:
        g = 'series'
    else:
        g = 'movie'
    return g
def getsitename(url):
    # url = 'https://nungsub.com/soundtrack'
    if 'www' in url:
        sitename = url.split('.')[1]
    else:  # print
        sitename = (url[url.find('/') + 2:url.find('.')])
        # print sitename
    return site2name(sitename)

def getsiteslist():
    # pt = sys.path[0] + '/resources/sites'
    # pt = sys.path[0]
    pt = addonpath + '/resources/sites'
    items = os.listdir(pt)
    slist = []
    for names in items:
        if names.endswith(".py") and not names.startswith('_'):
            hname = name2site(names)
            hurl = 'https://www.' + hname.lower() + '.com'
            hgenre = is_series(hname)
            slist.append({"url": hurl, "title": hname.capitalize(), 'thumbnail':pt +'/img/'+hname.lower() + '.png',"genre":hgenre})
    return slist

def getsiteserieslist_b():
    # pt = sys.path[0] + '/resources/sites'
    # pt = sys.path[0]
    pt = addonpath + '/resources/sites/ser'
    items = os.listdir(pt)
    slist = []
    for names in items:
        if names.endswith(".py") and not names.startswith('_'):
            hname = name2site(names).capitalize()
            hurl = 'https://www.' + hname.lower() + '.com'
            slist.append({"url": hurl, "title": hname})
    return slist

def chksrv(s):  # check server streaming
    if 'www' in s:
        return s.split('.')[1].capitalize()
    else:  # print
        return (s[s.find('/') + 2:s.find('.')]).capitalize()

def site2list():
    s = getsiteslist()
    ulist = []
    tlist = []
    for i in s:
        # print i.get('url')
        # print i.get('title')

        # print i.values()
        ulist.append(i.get('url'))
        tlist.append(i.get('title'))
    return ulist, tlist

def get_title(title):
    if title != None:

        orgtitle = re.sub('[^a-zA-Z0-9 ]', '', title)
        orgtitle = ' ( '+ orgtitle +')'
    else:
        orgtitle = ''
    return orgtitle

def savelast(url,title,thumbnail,action):
    # path =plugintools.get_runtime_path()
    information = {'url': url, 'title': title, 'thumbnail': thumbnail,'action':action}
    lasttitle = information['url']
    try:
        with open(tmpjson, "r") as info_read:
            dict_info = json.load(info_read)
            # plugintools.message('title',str(lasttitle))
            for n in dict_info['list']:
                print n
                if lasttitle == n['url']:
                    n_status = True
                    break
                else:
                    n_status = False
            # plugintools.message('n_status',str(n_status))
            if n_status is False:
                dict_info['list'].append(information)
            if len(dict_info['list']) > 10:
                dict_info['list'].pop(1)
    except:
        dict_info = {"list": [{'url': url, 'title': title, 'thumbnail': thumbnail,'action':action}]}
    with open(tmpjson, "w") as data:
        data.write(json.dumps(dict_info))
        data.close()
def loadlast():
    seriesList = []
    with open(tmpjson, "r") as info_read:
        dict_info = json.load(info_read)
        info_read.close()

    for lv in dict_info['list'][::-1]:
        # print p
        seriesList.append({'title': lv['title'], 'url': lv['url'],'thumbnail':lv['thumbnail'],'action':lv['action']})
    return seriesList
