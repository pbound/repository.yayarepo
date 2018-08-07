# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup
from _utility import y_soup, y_reguests, chksrv, get_title

def getgenre():
    soup = y_soup('http://www.fanseries.co/')
    ul = soup.find(id="menu-item-184632")
    # print ul
    ul = ul.find_next_siblings('li')
    seriesList = []
    for link in ul:
        news = link.find('a').get('href')
        if news != 'http://news.kseries.co/':
            # print link.text
            # print link.find('a').get('href')
            # print link.select('a[href="http://www.kseries.co/category/korea-series/"]')
            seriesList.append({'title': link.text.replace('\n', ''), 'url': link.find('a').get('href')})
    return seriesList


def getseries(url):
    soup = y_soup(url)
    ul = soup.find('div', {"class": "item_1 items"})
    div = ul.findAll('div', {"class": "item"})

    seriesList = []
    for item in div:
        surl = item.find('a').get('href')
        img = item.find('img')
        seriesList.append({'title': img.get('alt'), 'url': surl , 'thumbnail': img.get('src')})

    next = soup.find('a', {'class': 'nextpostslink'})
    if next != None:
        seriesList.append({'title': u"Next", 'url': next.get('href')})
    return seriesList


def getepisode(url):
    soup = y_soup(url)
    ul = soup.select("p  > a")
    print (ul)
    episodesList = []
    for item in ul:
        # print item.text
        # print item.get('href')
        # print url
        episodesList.append({"title": item.text, "url": item.get('href')})
    return episodesList
        






def getstreams(url,title=None):
    soup = y_soup(url)
    inp = soup.findAll('input', {"type": "button"})
    # print inp
    seriesList = []
    for bt in inp:

            id = bt.get('id')
            # print url
            kstrm = kstream(url,id)
            # print kstrm
            for src in kstrm:
                label=src.get('label')
                # print src.get('curl')
                if label is None:
                    label = ''
                title = bt.get('value')+'  '+label
                seriesList.append({'title': title, 'url': src.get('curl')})
    return seriesList

def kstream(url,id):
    # url = 'http://www.subthai.co/p/playi.php?id=33859975&width=1280&height=720&dh=1-15&dh2=1-14&os=&n=0'
    # url = 'http://www.kseries.co/clip/play.php?id=1582765&width=1005&height=540&dh=30-5&dh2=30-4&n=1'
    url = url.replace('p/','p/playi.php?id=')
    url = url +'&width=1005&height=540&dh=30-4&dh2=30-3&n='+id
    # print url
    r = requests.get(url)
    r.encoding = "utf-8"
    gsrc = re.compile('mobile.*\n.*src="([^"]+)"').findall(r.text)
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    strmList=[]
    src = soup.findAll('source')
    for strm in src:
        csrc = strm.get('src')
        if 'cliperror' not in csrc:
            if '\'' not in csrc:
                if 'LoadingCircleYouTube'in csrc:
                 csrc= gsrc[0]
                strmList.append({'label': strm.get('label'), 'curl': csrc})
    return strmList






def k_stream(url):
    r = requests.get(url)
    # s = re.compile('file.."(.*?)"').findall(r.text)
    s = re.compile('<source src="([^"]+)"').findall(r.text)
    url = s[0]
    return url
if __name__ == '__main__':
    getgenre()

#print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
# print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
# print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
# print getStreams()
# url = 'http://www.kseries.co/clip/play.php?id=1407338&width=1005&height=540&dh=24-10&dh2=24-9&n=0'
# print k_stream(url)
# print exteact_stream('http://www.kseries.co/clip/play.php?id=1390602&width=1005&height=540&dh=29-10&dh2=29-9&n=0')
# print  k_stream('http://www.kseries.co/clip/58836/')
# print getstreams('http://www.kseries.co/clip/58836/')
# print exactkSeries('http://www.kseries.co/clip/58836/')
#     print getseries('http://www.subthai.co/category/korea-series/')
#     print getstreams('http://www.serieshot.co/p/8817566/')