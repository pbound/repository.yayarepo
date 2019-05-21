# -*- coding: utf-8 -*-
import json, requests, urllib
import re
from base64 import b64decode

from bs4 import BeautifulSoup


def get_chlist():
    r= requests.get('https://www.we-play.tv/videos/live/')
    # print r.content
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    data = soup.findAll('a',{'class':"video-slide"})
    # print div
    # data = div.findAll('a')

    # print result
    chlist=[]
    for ch in data:
        # print ch
        # print ch.img.get('alt')
        # print 'http:'+ch.img.get('src')
        url = ch.get('href')
        print url
        title = ch.img.get('alt')
        thumnail = 'http:' + ch.img.get('src')
        # print source
        # name = source.split('/')[6].split('.')[0]
        # print name.capitalize()

        # print ch.find('img src')
        chlist.append({"url": url, "title": title, 'thumbnail': thumnail})
    return chlist

# getifreame()

def getm3u(url):
    #find frame src from url
    source = requests.get(url)
    flink = re.compile('iframe src="([^"]+)"').findall(source.text)
    # print flink[0]


    #find m3u from frame url
    frameurl =flink[0]
    source = requests.get(frameurl)
    link = re.compile('file: "([^"]+)",').findall(source.text)
# def getstreams():
    HEADERS = urllib.urlencode({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Referer': 'https://www.we-play.tv',
                })
    return link[0] + '|%s' % HEADERS

if __name__ == '__main__':
    # getstreams()
    print get_chlist()
    # print getm3u('https://www.we-play.tv/videos/%E0%B8%AA%E0%B8%B2%E0%B8%A3%E0%B8%84%E0%B8%94%E0%B8%B5/national-geographic/')