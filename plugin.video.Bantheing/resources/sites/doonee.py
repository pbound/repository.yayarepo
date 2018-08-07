# -*- coding: utf-8 -*-
# from __future__ import print_function
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup
from _utility import y_soup, y_reguests, chksrv, get_title

baseurl = 'https://www.doonee.com/'

def getgenre():
    # soup = y_reguests('http://www.doonee.com/',)
    # ul = soup.find(id="menu-home2")
    soup = y_soup('http://www.doonee.com')
    ul = soup.find('ul',{'class':'topnav'})
    # print div
    li = ul.findAll('li', {'class': 'nav-cate'})
    # print li
    seriesList = []
    for link in li:
        # print link
        chekmenu = link.find('a').get('href')
        # print chekmenu

        # if 'movie' in chekmenu:
            # mtitle =  link.find('a').text
            # murl = ''
        if 'cate/'  in chekmenu:
            # print link.find('a').get('href')
            mtitle = link.find('a').text
            murl = link.find('a').get('href').split('/')[-1]
            murl = 'https://doonee.com/movie/dynamic_search?page=1&limit=30&cate_id='+str(murl)


            seriesList.append({'title': mtitle, 'url': murl })

        div = link.select("p  > a")
        for slink in div:
            if 'cate' in slink.get('href'):
                if 'all' not in slink.get('href'):
                # print slink.get('href')
                    stitle = slink.text
                    cate_id = slink.get('href').split('/')[-1]
                    surl = 'https://doonee.com/movie/dynamic_search?page=1&limit=30&cate_id='+str(cate_id)

                    seriesList.append({'title': stitle, 'url': surl})
    return seriesList


def getseries(url):

    matches = re.search("page.([0-9]+).*?cate.id.([0-9]+)", url)
    pagenum = matches.groups()[0]
    cate_id = matches.groups()[1]
    # print page
    payload = {'cate_id': cate_id,
               'limit': '30',
               'page': pagenum,
               'search_mode': 'CATE'
               }

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': 'https://doonee.com/movie?type=movies',

               }

    source = requests.post(url, data=payload, headers=headers).json()
    maxpage = source['pageing']['maxPage']
    # print maxpage
    source = source['items']
    seriesList = []
    for mov in source:
        # print mov.keys()
        year = mov['year']
        title =  mov['title'] + ' ('+year+')'
        img = mov['img_src']
        surl = mov['href']
        seriesList.append({'title': title, 'url': surl , 'thumbnail': img})

    # next = soup.find('a', {'class': 'nextpostslink'})
    if int(pagenum) < int(maxpage):
        pagenum =int(pagenum)+1
        nurl = re.sub("page.([0-9]+)",'page='+str(pagenum),url)
        seriesList.append({'title': u"Next", 'url': nurl})
    return seriesList


def getepisode(url):

    source = y_reguests(url,'default.playlist.:(.*?)..\/\/need object')
    # print (source)
    jdata = json.loads(source[0])
    episodesList = []
    audio = getaudio(url)
    # print (audio)
    for sw in audio:
        snd = str(sw)
        for item in jdata:
            title = item['title'] + '  ' + item['episode_name'] + ' (Audio ' + snd +')'
            iurl = baseurl+(item['path'])+ snd.lower()
            img = baseurl + 'assets'+item['thumbnail']+'.jpg'
            episodesList.append({"title": title, "url": iurl, 'thumbnail':img})
    return episodesList
        


def getaudio(url):
    auid = y_reguests(url,'sw_audio..value="(.*?)"')
    return auid[0].split(',')





def getstreams(url,title=None):

    url=url.replace('https://www.doonee.com/','https://edge.api.brightcove.com/playback/v1/accounts/5308289312001/videos/ref:')
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': 'https://www.doonee.com/movie/396_MessyGoestoOkido%E0%B8%9B%E0%B8%B51',
               'Accept': 'application/json;pk=BCpkADawqM3KmViKn8EXGduvPEgvUZYe8FJx0qVp_XMUmATfl2Il92I82zyKRHqAHwp7w93PjivG6N68hHmRwO2d0v3Inmz6JH7xBzW6InSkWdA1zfr0FImSCQ5hKwCA1GNS27P1IVhyiXdhS001Zh9gNGjgncBoIMMxqTCmY_o0biUh-kCN_W7wSIT8AXAVE4qwCgVx9YH-PsZk',
               'Origin': 'https://www.doonee.com',

               }
    respons = requests.get(url, headers=headers).json()
    source = respons['sources']
    source = source[-3:-1]
    strmlist = []
    # print source
    for i , s  in enumerate(source,1):

        # purl = wurl + p + str(epid)
        # surl = y_reguests(purl, '(https.\/\/.*\W)" width')
        # if (surl):
        #     strm = surl[0].replace('\\', '')
        #     title = ' > ' + chksrv(strm)
        strmlist.append({"url": s['src'], "title": 'Player '+ str(i)})
    return strmlist

def dysearch():
    url ='https://doonee.com/movie/dynamic_search?page=1&limit=30&cate_id=14&q=&alphabet=&search_mode=CATE&moviemode='
    print url[url.find('?')+1:].split('&')[0]
    matches = re.search("page.([0-9]+).*?cate.id.([0-9]+)", url)
    page = matches.groups()[0]
    cate_id = matches.groups()[1]
    # print url.find('?')
    print page
    print cate_id

    sub = re.sub("page.([0-9]+)",'page=2',url)
    print sub

    payload = {'cate_id': '14',
                   'limit': '30',
                   'page': '1',
                   'search_mode': 'CATE'
                }
    print type(payload)

if __name__ == '__main__':

    # dysearch()

    print getgenre()
    # getseries('https://doonee.com/movie/dynamic_search?page=1&limit=30&cate_id=50')
    # print getepisode('https://doonee.com/movie/2624_')
    # print (getepisode('https://doonee.com/movie/2404'))
    # getaudio('https://doonee.com/movie/2404')
#     getepid('https://www.seriesgamo.com/video/tomorrow-with-you-ep-1/')

    # print getstreams('https://www.doonee.com/1283c7f7f6th')

