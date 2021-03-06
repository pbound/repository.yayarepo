# -*- coding: utf-8 -*-
import HTMLParser

import re
import requests
import xbmcgui

from _utility import y_soup,y_reguests,getnext


baseurl = 'https://www.movie2free.com/'
logourl = 'https://www.movie2free.com/wp-content/themes/next/logo/logo.png'
# mainlist.append({'title': u'Movie2Free', 'url': 'https://www.movie2free.com',
#                  'thumbnail': 'https://www.movie2free.com/wp-content/themes/next/logo/logo.png'})


def getgenre():
    soup = y_soup(baseurl)
    ul = soup.findAll('ul', {"class": "nav"})
    seriesList = []
    # print ul
    for li in ul:
        li = soup.findAll('a', {"class": "nav-main-link"})
        for link in li:
            seriesList.append({'title': link.text.replace('\n', ''), 'url': link.get('href')})
    return seriesList

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


def getstreams(url):
    itemslist = getitemsframe(url)
    # xbmcgui.Dialog().ok('url', str(len(itemslist)), url)
    strmlist = []
    for stm in itemslist:
        iurl = stm.get('url')
        ititle = stm.get('title')
        # print ititle,iurl
        streamf = y_reguests(iurl, regex='url":"([^"]+)".*?Name.."(.*?)"', referer='https://www.movie2free.com/')
        if streamf != None:
            # xbmcgui.Dialog().ok('url',str(len(streamf)), iurl)
            # strmlist = []
            for i in range(0,len(streamf)):
                surl= streamf[i][0].replace('\/','/')
                stitle = ititle+' > '+ streamf[i][1].decode('unicode_escape')
                # print surl
                # print stitle
                strmlist.append({"url": surl, "title": stitle})
    return strmlist

def getframe(url):
    frameurl = y_reguests(url, 'style.*\s.*?<iframe.src="([^"]+)"')
    return frameurl[0]

def getitemsframe(url):
    frameurl = getframe(url)
    streamf = y_reguests(frameurl, regex='label"."(.*?)".*?url":"([^"]+)"', referer='https://www.movie2free.com/')
    # print len(streamf)
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
    ssurl = 'https://www.movie2free.com/?s=' + str(title)
    return  getmov(ssurl)

def getsearchall(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist =  getmov(ssurl)
    surl = mlist[0].get('url')
    # print surl
    return getstreams(surl)







def extractLinks(a):
    linkList = []
    for link in a:
        linkList.append(link.get('href'))
    return linkList

if __name__ == '__main__':
    # print getsearchall('battleship')
# print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
# print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
# print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
# getMenu()
# print getmov('https://www.movie2free.com/top-imdb/')
# getgenre()
# print getstreams('https://www.movie2free.com/black-panther-%E0%B9%81%E0%B8%9A%E0%B8%A5%E0%B9%87%E0%B8%84-%E0%B9%81%E0%B8%9E%E0%B8%99%E0%B9%80%E0%B8%98%E0%B8%AD%E0%B8%A3%E0%B9%8C-2018/')
    print getstreams('https://www.movie2free.com/battleship-%E0%B8%A2%E0%B8%B8%E0%B8%97%E0%B8%98%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%A3%E0%B8%B7%E0%B8%AD%E0%B8%A3%E0%B8%9A%E0%B8%9E%E0%B8%B4%E0%B8%86%E0%B8%B2%E0%B8%95%E0%B9%80%E0%B8%AD%E0%B9%80/')