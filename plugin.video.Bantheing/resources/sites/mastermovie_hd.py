# -*- coding: utf-8 -*-
import requests
import xbmcgui
from bs4 import BeautifulSoup
from _utility import y_soup,y_reguests,get_title,chksrv

baseurl = 'https://www.mastermovie-hd.com'


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
    mlist = y_reguests(url, 'div>.*\n<a href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"')
    movieslist = []
    for item in mlist:
        movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})

    next = y_reguests(url, "current.*?href='([^']+)'")
    # print snext
    if next != None:
        movieslist.append({'title': u"Next", 'url': next[0]})
    return movieslist


def getsound(url):
    soundlist = y_reguests(url,regex='a class.*?vod_m3u8.*?>(.*?)<')
    return soundlist


def getstreams(url, title =None):
    # orgtitle = get_title(title)
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
            # print frm
            surl = frm.find('source').get('src')
            sid = frm.find('video').get('id')
            # print sid
            if 'videojs-hls-player-vod_m3u8_sub' in sid:
                stitle = 'Soundtrack'
            else:
                stitle = 'Thai sound (T)'

            strmlist.append({"url":surl,"title":'Mastermovie-HD >> ' + stitle  })


        div2 = soup.findAll('div', {'class':'videoWrapper'})
        # print (div2)
        for player in div2:
            purl = player.find('iframe').get('src')
            strmlist.append({"url": purl, "title": 'Mastermovie-HD >> ' +chksrv(purl) })
    return strmlist


def getsearch(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist = y_reguests(ssurl,'href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"')
    movieslist = []
    for item in mlist:
        movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})
    return movieslist

def getsearchall(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist = y_reguests(ssurl,'href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"')
    if mlist != None:
        surl = mlist[0][0]
        stitle = mlist[0][1]
        return getstreams(surl,title=stitle)

if __name__ == '__main__':
    # print getsearchall('who+am+i+ซิ่งสู้ฟัด')
# print getgenre()
#     getmov('https://www.mastermovie-hd.com/category/%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B9%84%E0%B8%95%E0%B8%A3%E0%B8%A0%E0%B8%B2%E0%B8%84/')
# getsound('https://www.mastermovie-hd.com/the-magnificent-seven-2016-7-สิงห์แดนเสือ')
    print getstreams('https://www.mastermovie-hd.com/the-magnificent-seven-2016-7-สิงห์แดนเสือ')