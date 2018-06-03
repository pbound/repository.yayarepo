# -*- coding: utf-8 -*-
import HTMLParser

import re
import requests
import xbmcgui


# from resources.sites._utility import y_soup, y_reguests, chksrv, get_title
from _utility import y_soup, y_reguests, chksrv, get_title

baseurl = 'https://www.movieclub.tv/series/'
def getgenre():
    matchpag = y_reguests(baseurl,regex="onclick.*?Series.'(.*?)'.*?>.(.*?.).<")
    movielist = []
    # movielist.append({'title': u'ภาพยนต์ ทั้งหมด', 'url': 'https://www.movieclub.tv/movies/list-movies/filter/all'})
    # movielist.append({'title': u'ภาพยนต์ ไทย', 'url': 'https://www.movieclub.tv/movies/list-movies/filter/thai'})
    # movielist.append({'title': u'ภาพยนต์ ฝรั่ง', 'url': 'https://www.movieclub.tv/movies/list-movies/filter/inter'})
    # movielist.append({'title': u'ภาพยนต์ เอเซีย', 'url': 'https://www.movieclub.tv/movies/list-movies/filter/asia'})
    for i in range(0, len(matchpag)):
        url = baseurl + 'list-series/filter/' + matchpag[i][0]

        # print url
        movielist.append({'title':matchpag[i][1], 'url':url})
    return movielist

def getmov(url):
    mlist = y_reguests(url, '<a href="([^"]+)".title="(.*?)".*?nal="([^"]+)"')
    # print (mlist)
    movieslist = []
    if mlist != []:
        for item in mlist:
            movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})

    next = y_reguests(url, '<li class="">.*?href="(.*?)"')
    # print snext
    if next != None:
        movieslist.append({'title': u"Next", 'url': url + next[0]})
    return movieslist


def getepisode(url,thumbnail=None):
    eplist =[]
    list = y_reguests(url,'title.."(.*?)"."file"."([^"]+)"')
    for ep in list:
        # print ep
        eplist.append({'url':url,'title':ep[0]})
    return eplist






def getstreams(url,title=None):
    # orgtitle = get_title(title)
    # xbmcgui.Dialog().ok('test',title,orgtitle)
    if url is not None:

        player = y_reguests(url,'title.."(.*?)"."file"."([^"]+)"')
        strmlist = []

        for strm in player:
            surl= strm[1].replace('\/','/')

            # title =  title.encode('utf-8') +' Movieclup > '
            strmlist.append({"url": surl, "title": strm[0]})
    return strmlist

def getsearch(title):
    ssurl = baseurl + '/?s=' + str(title)
    return  getmov(ssurl)
def getsearchall(title):
    pass
def getsearchalls(title):

    ssurl = baseurl + '/?s=' + str(title)
    xbmcgui.Dialog().ok('title 037',ssurl)
    # print ssurl
    mlist =  getmov(ssurl)
    # print mlist
    xbmcgui.Dialog().ok('037hd', str(mlist))
    if mlist != []:
        surl = mlist[0].get('url')
        stitle = mlist[0].get('title')
        # print stitle
        return getstreams(surl,stitle)

def willdel(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'referer':'https://www.movieclub.tv'}
    r = requests.get(url, headers=headers).text
    r = HTMLParser.HTMLParser().unescape(r)
    # print '*'*50
    print r
    match = re.compile('').findall(r)

if __name__ == '__main__':
    # getmov('https://utaseries.co/category/series-online/ซี่รี่ย์เกาหลี/ซีรี่ย์เกาหลี-ซับไทย/')
    # print getepisode('https://www.movieclub.tv/series/detail/8388')
    # print gettab('https://utaseries.co/miracle-that-we-met-ep1/')
    # print  getstreams('https://utaseries.co/miracle-that-we-met-ep1/')
    # print getgenre()
    # print getmov('https://www.movieclub.tv/movies/list-movies/filter/all')
    print getstreams('https://www.movieclub.tv/series/detail/8388')
    # willdel('https://www.movieclub.tv/movies/list-movies/filter/all')