# -*- coding: utf-8 -*-
import HTMLParser
import json
import re
import requests
import xbmcgui

from _utility import y_soup,y_reguests,get_title


baseurl = 'https://www.movie2free.com'
logourl = 'https://www.movie2free.com/wp-content/themes/next/logo/logo.png'
# mainlist.append({'title': u'Movie2Free', 'url': 'https://www.movie2free.com',
#                  'thumbnail': 'https://www.movie2free.com/wp-content/themes/next/logo/logo.png'})


def getgenre():
    gen = y_reguests(baseurl,'class="nav-main-link.*?href="(.*?category.*?)".*?>(.*?)<')
    # print ul
    gensList = []
    for items in gen:
        gensList.append({'title': items[1], 'url': items[0]})
    return gensList

def getmov(url):

    soup = y_soup(url)
    ul = soup.find('div', {"class": "box"})
    div = ul.findAll('div', {"class": "movie-box"})
    seriesList = []
    for item in div:
        img = item.find('img')

        seriesList.append(
            {'title': item.find('a').text.strip(), 'url': item.find('a').get('href'), 'thumbnail': img.get('src')})

    next = y_reguests(url,'href="([^"]+page\/.*?\/)">')
    # print next
    if next != None :
        seriesList.append({'title': u"Next", 'url': next[0]})
    #     seriesList.append({'title': u"Next", 'url': next.get('href')})
    return seriesList


def getstreams(url,title=None):

    # orgtitle =get_title(title)

############# Fraeme embed ###############
    itemslist = getitemsframe(url)
    # xbmcgui.Dialog().ok('url', str(len(itemslist)), orgtitle)
    strmlist = []
    for stm in itemslist:
        print stm
        iurl = stm.get('url')
        ititle = stm.get('title')
        # print ititle,iurl

############## Find url in Embed ##################
        streamf = y_reguests(iurl, regex='url":"([^"]+)".*?Name.."(.*?)"', referer='https://www.movie2free.com/')
        # print (streamf)
        if streamf != None:
            # xbmcgui.Dialog().ok('url',str(len(streamf)), iurl)
            # strmlist = []
            for i in range(0,len(streamf)):
                # print i

                if streamf[i][1] == '\u0e2b\u0e25\u0e31\u0e01' or streamf[i][1] == 'Thai':
                    surl = iurl
                    # server  หลัก  and Thai
                    # print '??????????????????????'
                else:
                    surl= streamf[i][0].replace('\/','/')

                stitle = ititle + ' > '+ streamf[i][1].decode('unicode_escape')

                # print surl
                # print stitle
                strmlist.append({"url": surl, "title": stitle})
    return strmlist

def getframe(url):
    frameurl = y_reguests(url, 'style.*\s.*?<iframe.src="([^"]+)"')
    # print frameurl
    return frameurl[0]

def getitemsframe(url):
    frameurl = getframe(url)
    streamf = y_reguests(frameurl, regex='label"."(.*?)".*?url":"([^"]+)"', referer='https://www.movie2free.com/')
    # print (streamf)
    itemslist = []
    for i in range(0, len(streamf)):
        iurl = streamf[i][1].replace('\/', '/')
        ititle = streamf[i][0].decode('unicode_escape')
        # print iurl
        # print ititle
        # strm = src.get('data-lazy-src')
        itemslist.append({"url": iurl, "title": 'movie2free  >>' + ititle})
    return itemslist

def getsearch(title):
    ssurl = baseurl+ '/?s=' + str(title)
    return  getmov(ssurl)

def getsearchall(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist =  getmov(ssurl)
    # xbmcgui.Dialog().ok('m2f',str(mlist))
    if mlist != None:
        surl = mlist[0].get('url')
        stitle = mlist[0].get('title')
        # print surl
        return getstreams(surl,stitle)

def getquality(url,title):
    ntitle = title.split('>')[-1].strip().decode('utf8')
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': 'https://www.movie2free.com/'}
    r = requests.get(url, headers=headers).text
    r = HTMLParser.HTMLParser().unescape(r)
    r = r.decode('unicode_escape').encode('utf-8')
    todos = json.loads(r)
    jlist = todos['data']
    strmlist = []
    for i in range( len(jlist)):
        svname = jlist[i]['providerName']
        if svname == ntitle :
            qualist = jlist[i]['streams']
            for j in range(len(qualist)):
                stitle = qualist[j]['quality']
                surl = qualist[j]['url']

                strmlist.append({"url": surl, "title": stitle})
            break
    return strmlist




def extractLinks(a):
    linkList = []
    for link in a:
        linkList.append(link.get('href'))
    return linkList
