# -*- coding: utf-8 -*-
from _utility import y_soup,y_reguests,getnext

def getgenres():
    regex = 'item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"'
    matchpag = y_reguests('https://nungsub.com',regex=regex)
    movielist = []
    for i in range(0, len(matchpag)):
        movielist.append({'title': matchpag[i][0], 'url': matchpag[i][1]})
    return movielist
def getgenre():
    soup = y_soup('https://nungsub.com')
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
    ul = soup.findAll('div', {"class": "item col300"})
    movieslist = []
    for item in ul:
        # print item
        murl =  item.find('a').get('href')
        mimg = item.find('img').get('data-lazy-src')
        mtitle = item.find('img').get('alt')
        # print murl
        movieslist.append({'title': mtitle, 'url': murl, 'thumbnail': mimg})

    next = getnext(url)
    if len(next) != 0:
        movieslist.append({'title': u"Next", 'url': next[0]})
    return movieslist


# print getgenre()
# print getmov('https://nungsub.com/soundtrack-%E0%B8%8B%E0%B8%B1%E0%B8%9A%E0%B9%84%E0%B8%97%E0%B8%A2/full-hd/new-hot-movie/')
