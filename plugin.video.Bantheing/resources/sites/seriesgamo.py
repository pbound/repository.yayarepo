# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup
from _utility import y_soup, y_reguests, chksrv, get_title

def getgenre():
    soup = y_soup('http://www.series24hr.com/')
    ul = soup.find(id="menu-home2")
    # print ul
    # ul = ul.find_next_siblings('li')
    li = ul.findAll('li',{'class':'menu-item'})
    # print li
    seriesList = []
    for link in li:
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


    # find last page number
    pages = soup.findAll('a', {'rel': "nofollow"})
    if pages:
        # pages=pages[-1]
        pages = pages[-1].get('href')
        lastnum = int(re.search('page.([0-9]+)', pages).groups()[0])

        # find current page number from url
        current = re.search('page.([0-9]+)', url)
        current = int(current.groups()[0]) if current else 1

        # print lastnum, current
        if lastnum > current:
            if current == 1 :url=url+'page/1'
            current += 1
            nurl = re.sub("page.([0-9]+)", 'page/'+str(current), url)
            seriesList.append({'title': u"Next", 'url': nurl})
    return seriesList


def getepisode(url):
    soup = y_soup(url)
    div = soup.find(style="text-align: center;")
    # print div
    ul = div.select("p  > a")
    # print (ul)
    episodesList = []
    for item in ul:
        # print item.text
        # print item.get('href')
        # print url
        episodesList.append({"title": item.text, "url": item.get('href')})
    return episodesList
        


def getepid(url):
    epid = y_reguests(url,'\/embed\/([\d]+)"')
    return epid[0]




def getstreams(url,title=None):

    wurl = 'https://www2.popuplayer.com/'
    player = ('player1.php?id=', 'v2/gdrive.php?id=')
    epid = getepid(url)

    strmlist = []
    for p in player:
        purl = wurl + p + str(epid)
        surl = y_reguests(purl, '(https.\/\/.*\W)" width')
        if (surl):
            strm = surl[0].replace('\\', '')
            title = ' > ' + chksrv(strm)
            strmlist.append({"url": strm, "title": title})
    return strmlist


def testnext():
    url = 'https://www.series24hr.com/category/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B8%9D%E0%B8%A3%E0%B8%B1%E0%B9%88%E0%B8%87-usa-series/page/2'
    # url = 'https://www.series24hr.com/category/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B8%8D%E0%B8%B5%E0%B9%88%E0%B8%9B%E0%B8%B8%E0%B9%88%E0%B8%99-japan-series/'
    current = re.search('page.([0-9]+)',url)
    # print current.groups()[0]
    current = int(current.groups()[0])if current else 1
        # current = int(current[-1].groups()[0])
    # else:
    #     current = 1


    soup = y_soup(url)

    # find last page num
    pages = soup.findAll('a', {'rel': "nofollow"})
    if pages:
        # pages = pages[-1]
        pages = pages[-1].get('href')
        lastnum= int(re.search('page.([0-9]+)',pages).groups()[0])
        print lastnum,current
        if lastnum > current:
            current +=1
            print current

if __name__ == '__main__':
    testnext()

    # getgenre()
    # print getseries(url = 'https://www.series24hr.com/category/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B8%9D%E0%B8%A3%E0%B8%B1%E0%B9%88%E0%B8%87-usa-series/page/2')

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
#     getepid('https://www.seriesgamo.com/video/tomorrow-with-you-ep-1/')
#     print getpstream('8605')
#     print getstreams('https://www.seriesgamo.com/video/tomorrow-with-you-ep-1/')

