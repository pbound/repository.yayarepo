# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup
import xbmcgui
from _utility import y_soup, y_reguests, chksrv, get_title
import HTMLParser
baseurl = 'https://www.037hd.com'
def getgenre():
    matchpag = y_reguests(baseurl,regex='custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<')
    # matchpag = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    movielist = []
    for i in range(0, len(matchpag)):
          movielist.append({'title':matchpag[i][1], 'url':matchpag[i][0]})
    return movielist

def getmov(url):
    soup = y_soup(url)
    ul = soup.findAll('div', {"class": "moviefilm"})
    # print (ul)
    if len(ul) ==0:
        ul = soup.findAll('div', {"class": "item col220"})
    # div = ul.findAll('div', {"class": "moviefilm"})

    movieslist = []
    for item in ul:
        # print item
        murl =  item.find('a').get('href')
        mimg = item.find('img').get('src')
        mtitle = item.find('img').get('alt')
        movieslist.append({'title': mtitle, 'url': murl, 'thumbnail': mimg})

    next = soup.find('a', {'class': 'nextpostslink'})
    # next = soup.find('div', {'class': 'navigation'})
    if next != None:
        # print next
        # print next.get('href')
        movieslist.append({'title': u"Next", 'url': next.get('href')})
    return movieslist

def getstreams(url,title=None):
    orgtitle = get_title(title)
    # xbmcgui.Dialog().ok('test',title,orgtitle)
    if url is not None:
        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text
        player = re.compile('<iframe.*?src="(.*?leoplay.*?)"').findall(r)
        # soup = BeautifulSoup(r.text, 'html5lib')
        # soup.prettify()
        # div = soup.find('h2', {"style": "text-align: center;"})
        # print (player)
        strmlist = []
        for i,surl in enumerate(player,1):
            # if 'container' in surl:
                if i == 1:  # cheak soundtrack with player
                    sound = u'พากย์ไทย'
                else:
                    sound = 'Soundtrack'

                r = requests.get(surl)
                r = HTMLParser.HTMLParser().unescape(r).text
                play = re.compile('<a href="(.*?)"').findall(r)
                for leo in play:
                    r = requests.get(leo)
                    r = HTMLParser.HTMLParser().unescape(r).text
                    strm = re.compile('<iframe.*?src="(.*?)"').findall(r)

                    title = '037HD >'+sound+' >> '+chksrv(strm[0])
                    # print strm[0]
                    # strhost = strm[0]
                    # strhost = strhost[strhost.find('//')+2:strhost.find('.')].capitalize()
                    strmlist.append({"url": strm[0], "title": title})
            # else:
            #     strmlist.append({"url": surl, "title": '037HD >> ' + chksrv(surl) + orgtitle})

    return strmlist
def getsearch(title):
    ssurl = baseurl + '/?s=' + str(title)
    return  getmov(ssurl)

def getsearchall(title):

    ssurl = baseurl + '/?s=' + str(title)
    # xbmcgui.Dialog().ok('title 037',ssurl)
    # print ssurl
    mlist =  getmov(ssurl)
    # print mlist
    # xbmcgui.Dialog().ok('037hd', str(mlist))
    if mlist != []:
        surl = mlist[0].get('url')
        stitle = mlist[0].get('title')
        # print stitle
        return getstreams(surl,stitle)

if __name__ == '__main__':
    # print getstreams(url = 'https://www.037hd.com/foreigner-2017-2-%e0%b9%82%e0%b8%84%e0%b8%95%e0%b8%a3%e0%b8%9e%e0%b8%a2%e0%b8%b1%e0%b8%84%e0%b8%86%e0%b9%8c%e0%b8%9c%e0%b8%b9%e0%b9%89%e0%b8%a2%e0%b8%b4%e0%b9%88%e0%b8%87%e0%b9%83%e0%b8%ab/"')
    print getsearchall(title='safe+Nighborhood')