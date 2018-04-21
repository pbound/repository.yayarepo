# -*- coding: utf-8 -*-
import requests, re, urllib, os, json, binascii, sys
from bs4 import BeautifulSoup


def getMenu():
    r = requests.get('https://www.movie2free.com/')
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.findAll('ul', {"class": "nav"})
    seriesList = []
    # print ul
    for li in ul:
        li = soup.findAll('a', {"class": "nav-main-link"})
        for link in li:
            # print link.text.replace('\n', '')
            # print link.get('href')
            seriesList.append({'title': link.text.replace('\n', ''), 'url': link.get('href')})
    return seriesList


def getSeries(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('div', {"class": "box"})
    div = ul.findAll('div', {"class": "movie-box"})
    # print div
    seriesList = []
    for item in div:
        img = item.find('img')
        # print img
        # print item.find('a').get('href')
        # print item.find('a').text.strip()

        seriesList.append(
            {'title': item.find('a').text.strip(), 'url': item.find('a').get('href'), 'thumbnail': img.get('src')})

    next = soup.find('a', {'class': 'nextpostslink'})
    if next != None:
        seriesList.append({'title': u"הבא", 'url': next.get('href')})
    return seriesList


def getEpisodes(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.findAll('div', {"class": "symple-toggle state-closed "})

    episodesList = []
    for item in ul:
        episodesList.append({"title": item.find('h3').text, "url": url})
    return episodesList


def getStreams(url, episode):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')

    h3 = soup.find('h3', text=lambda x: x and x == episode.decode('utf-8'))

    sourceList = []
    h3parent = []
    try:
        h3parent = h3.parent.findAll('a')
    except:
        h3parent = []
    if h3parent == []:
        h3parent = getSpecialStreams(url, episode)
    for link in h3parent:
        linkurl = link.get('href')
        if "adf.ly" in linkurl.lower():
            if '/http' in linkurl.lower():
                linkurl = re.sub(r'.*http', 'http', linkurl.replace('http://adf.ly/', ''))
            else:
                linkurl = adFly(linkurl)
        sourceList.append({"title": linkurl, "url": linkurl})
    return sourceList


def adFly(url):
    r = requests.get('http://skizzerz.net/scripts/adfly.php?url=' + url)
    soup = BeautifulSoup(r.text, 'html5lib')
    return soup.find('a').get('href')


def yandex(url):
    try:
        s = requests.Session()
        r = s.get(url)
        r = re.sub(r'[^\x00-\x7F]+', ' ', r.text)

        sk = re.findall('"sk"\s*:\s*"([^"]+)', r)[0]

        idstring = re.findall('"id"\s*:\s*"([^"]+)', r)[0]

        idclient = binascii.b2a_hex(os.urandom(16))

        post = {'idClient': idclient, 'version': '3.9.2', 'sk': sk, '_model.0': 'do-get-resource-url', 'id.0': idstring}
        # post = urllib.urlencode(post)

        r = s.post('https://yadi.sk/models/?_m=do-get-resource-url', data=post)
        r = json.loads(r.text)

        url = r['models'][0]['data']['file']

        return url
    except:
        return


def getSpecialEpisodes(url, find='p'):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.find('div', {"class": "post-wrapper"})

    p = ul.findAll(find)

    epsList = []
    last = None
    for eps in p:
        if last == None:
            last = eps
        a = eps.findAll('a')
        if a != []:
            strong = eps.find('strong')
            subject = ''
            if strong != None:
                subject = strong.text
            else:
                laststrong = last.find('strong')
                if laststrong != None:
                    subject = laststrong.text
                else:
                    epstext = eps.text
                    if u'פרק' in epstext:
                        subject = epstext
                    else:
                        subject = last.text

            subject = re.sub('\n.*', '', subject)
            if u'פרק' in subject:
                epsList.append({'title': subject, 'url': a})
        last = eps

    if epsList == [] and find == 'p':
        return getSpecialEpisodes(url, 'address')

    return epsList


def getSpecialStreams(url, episode):
    epsList = getSpecialEpisodes(url)
    strmList = []
    for item in epsList:
        if item.get('title') == episode.decode('utf-8'):
            return item.get('url')
    return strmList


def extractLinks(a):
    linkList = []
    for link in a:
        linkList.append(link.get('href'))
    return linkList


# print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
# print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
# print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
getMenu()
# getSeries('https://www.movie2free.com/top-imdb/')