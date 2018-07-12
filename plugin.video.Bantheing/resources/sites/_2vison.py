# -*- coding: utf-8 -*-
import requests
from _utility import y_soup, y_reguests


def get_chlist():
    url = 'http://tv.trueid.net/live/listall'
    soup =y_soup(url)
    soup.prettify()
    div = soup.findAll('div', {'class': "block_pd col-md-3 col-sm-3 col-xs-3 col-list5"})
    chalist = []
    for items in div:

        title = items.find('a').get('title')
        img = items.find('img').get('data-src')
        churl = items.find('a').get('href')
        # print churl
        chalist.append({"url": churl, "title": title ,'thumbnail':img})

    return chalist

def getsubstream(url):
    r = y_reguests(url,'content.id = "(.*?)"')
    if (r):
        return getfinal(r[0])


def getfinal(ch_code):
    url = 'http://tv.trueid.net/live/geturl'
    payload = {"chc":ch_code}
    source = requests.post(url, data=payload).content
    return source


