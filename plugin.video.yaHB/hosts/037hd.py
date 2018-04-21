# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup
import HTMLParser
def getMenu():
    r = requests.get('https://www.037hd.com')
    # soup = BeautifulSoup(r.text, 'html5lib')
    # soup.prettify()
    # ul = soup.findAll('ul', {"class": "nav"})
    # source = requests.get(url, headers=headers)
    r = HTMLParser.HTMLParser().unescape(r).text
    # r = source.decode('unicode_escape').encode('utf-8').replace('\/', '/')
    # print  source

    # matchpag1 = re.compile('class="nav-main-link.*?href="(.*?)".*?>(.*?)<').findall(r)
    # matchpag2 = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    # if 'movie2free' in url:
    #     matchpag = re.compile('class="nav-main-link.*?href="(.*?)".*?>(.*?)<').findall(r)
    # elif '037hd' in url:
    matchpag = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    # else:
    #     matchpag =re.compile('item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"').findall(r)
    # print len(matchpag)
    # print matchpag
    #     matchpag
    movielist = []
    for i in range(0, len(matchpag)):
        # if 'nungsub'in url:
        #     movielist.append({'title': matchpag[i][0], 'url': matchpag[i][1]})
        # else:
          # print matchpag[i][0]
          # print matchpag[i][1]
          movielist.append({'title':matchpag[i][1], 'url':matchpag[i][0]})
    return movielist