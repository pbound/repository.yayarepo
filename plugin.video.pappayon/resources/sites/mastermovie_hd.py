# -*- coding: utf-8 -*-
import requests
import xbmcgui
from bs4 import BeautifulSoup
from _utility import y_soup,y_reguests,getnext,chksrv

baseurl = 'https://www.mastermovie-hd.com/'


def getgenre():
    soup = y_soup(baseurl)
    ul = soup.findAll('li', {"class": "cat-item"})
    # print (ul)?
    genreslist = []
    for items in ul:
        gtitle = items.text.strip()
        if 'VIP' not in gtitle:
            gurl =  items.find('a').get('href')
            genreslist.append({'title': gtitle, 'url': gurl})
    return genreslist

def getmov(url):
    soup = y_soup(url)
    ul = soup.findAll('div', {"class": "item col220"})
    if len(ul) == 0:
        ul = soup.findAll('div', {"class": "item col300"})

    movieslist = []
    for item in ul:
        # print item
        murl =  item.find('h2').find('a').get('href')
        mimg = item.find('img').get('src')
        # mimg = mimg.encode('utf8')
        mtitle = item.find('img').get('alt')
        # print murl
        movieslist.append({'title': mtitle, 'url': murl, 'thumbnail': mimg})

    # snext = y_reguests(url,regex='href="([^"]+)">Next')
    snext = y_reguests(url,"current.*?href='([^']+)'")
    print snext
    if snext != None:
        # print 'd'
        movieslist.append({'title': u"Next", 'url': snext[0]})
    return movieslist

def getsound(url):
    soundlist = y_reguests(url,regex='a class.*?vod_m3u8.*?>(.*?)<')
    return soundlist


def getstreams(url):
    # xbmcgui.Dialog().ok('url', url)
    if url is not None:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        # print soup
        div = soup.findAll('div', {"class": "video-player-section"})
        # print div
        strmlist = []
        for frm in div:
            surl = frm.find('source').get('src')
            sid = frm.find('video').get('id')
            # print sid
            if 'videojs-hls-player-vod_m3u8_sub' in sid:
                stitle = 'Soundtrack'
            else:
                stitle = 'Thai sound (T)'

            strmlist.append({"url":surl,"title":'Mastermovie-HD >> ' + stitle})
    return strmlist

def getsearch(title):
    ssurl = 'https://www.mastermovie-hd.com/?s=' + str(title)
    mlist = y_reguests(ssurl,'href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"')
    movieslist = []
    for item in mlist:
        movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})
    return movieslist

def getsearchall(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist = y_reguests(ssurl,'href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"')
    surl = mlist[0][0]
    return getstreams(surl)


if __name__ == '__main__':
    print getsearchall('battleship')
# print getgenre()
#     getmov('https://www.mastermovie-hd.com/category/%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B9%84%E0%B8%95%E0%B8%A3%E0%B8%A0%E0%B8%B2%E0%B8%84/')
# getsound('https://www.mastermovie-hd.com/the-magnificent-seven-2016-7-สิงห์แดนเสือ')
# print getstreams('https://www.mastermovie-hd.com/the-magnificent-seven-2016-7-สิงห์แดนเสือ')