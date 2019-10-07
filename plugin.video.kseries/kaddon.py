# -*- coding: utf-8 -*-
import requests, re
from bs4 import BeautifulSoup
from base64 import b64decode

base_url = b64decode('aHR0cHM6Ly93d3cua3N1YnRoYWkuY28=')

def getMenu():
    print base_url
    r = requests.get(base_url)

    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find(id="menu-item-151384")
    ul = ul.find_next_siblings('li')
    seriesList = []
    for link in ul:
        print link.find('a').get('href')
        seriesList.append({'title': link.text.replace('\n', ''), 'url': link.find('a').get('href')})
    return seriesList


def getSeries(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    # print soup
    # li = soup.findAll('a', {"class": "post-thumb"})
    li = soup.findAll('div', {'class': 'image'})
    # print li

    seriesList = []
    for item in li:
        img = item.find('img')
        seriesList.append({'title': img.get('alt'), 'url': img.parent.get('href'), 'thumbnail': img.get('src')})

    next = soup.find('span', {'class': 'pages'})

    if next != None:
        cp = int(next.text.split(' ')[1])
        lp = int(next.text.split(' ')[-1])
        if lp > cp:
            np = int(cp) + 1
            if 'page' in url:
                # print np
                nurl = url.replace(str(cp), str(np))
            else:
                nurl = url + 'page/' + str(np)
            seriesList.append({'title': u"Next", 'url': nurl})
    return seriesList


def getEpisodes(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.findAll('p', {"style": "text-align: center;"})
    episodesList = []
    for items in ul:
        item = items.find('a')
        if item:
            episodesList.append({"title": item.text, "url": item.get('href')})
    return episodesList


def getStreams(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')
    h3 = soup.find_all('input', {"class": "sublink"})
    sourceList = []
    turl = url.replace('clip/', 'clip/play.php?id=') + '&width=1005&height=550&dh=5-10&dh2=5-9&n='
    for link in h3:
        sourceList.append({"title": link.get('value'), "url": turl + link.get('id')})
    return sourceList


def exactkSeries(url):
    # print url
    r = requests.get(url)
    r.encoding = "utf-8"
    # print r.content.title()
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    inp = soup.findAll('input', {"type": "button"})
    # print inp
    stitle = soup.find("meta", property="og:title").get('content')
    # print stitle
    seriesList = []
    for bt in inp:

        id = bt.get('id')
        kstrm = kstream(url, id)
        for src in kstrm:
            label = src.get('label')
            if label is None:
                label = ''
            title =  bt.get('value') + '  ' + label + '  ' + stitle
            # print title
            seriesList.append({'title': title, 'url': src.get('curl')})
    return seriesList


def kstream(url, id):
    # print url
    # url = url.replace('clip/', 'clip/play.php?id=')
    url = url.replace('p/', 'p/playi.php?id=')
    url = url + '&width=1005&height=540&dh=30-4&dh2=30-3&n=' + id
    # print url
    r = requests.get(url)
    r.encoding = "utf-8"
    # print r
    gsrc = re.compile('mobile.*\n.*src="([^"]+)"').findall(r.text)
    ksrc = re.compile("player.src.*?'([^']+)'").findall(r.text)
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    strmList = []
    src = soup.findAll('source')
    for strm in src:
        # print strm
        csrc = strm.get('src')
        if 'cliperror' not in csrc:
            if '\'' not in csrc:
                if 'LoadingCircleYouTube' in csrc:
                    csrc = gsrc[0]
                if 'loading.mp4' in csrc:
                    csrc = ksrc[0]
                    csrc = csrc + '|Referer=%s' % url
                strmList.append({'label': strm.get('label'), 'curl': csrc})
    return strmList


def k_stream(url):
    r = requests.get(url)
    s = re.compile('<source src="([^"]+)"').findall(r.text)
    url = s[0]
    return url

if __name__ == '__main__':
    pass
    # getMenu()
    # print getSeries('https://www.ksubthai.co/category/korea-series/')
    # print getEpisodes('https://www.ksubthai.co/melting-me-softly/')
    # print getStreams('https://www.ksubthai.co/p/163688/')
    # print exactkSeries('https://www.ksubthai.co/p/166061/')