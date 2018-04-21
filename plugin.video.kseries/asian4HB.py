# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup


def getMenu():
    r = requests.get('http://www.kseries.co/')
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find(id="menu-item-105338")
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


def getSeries(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('div', {"class": "item_1 items"})
    div = ul.findAll('div', {"class": "item"})

    seriesList = []
    for item in div:
        img = item.find('img')
        seriesList.append({'title': img.get('alt'), 'url': img.parent.get('href'), 'thumbnail': img.get('src')})

    next = soup.find('a', {'class': 'nextpostslink'})
    if next != None:
        seriesList.append({'title': u"Next", 'url': next.get('href')})
    return seriesList


def getEpisodes(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    # ul = soup.findAll('p', {"style":"text-align: center;"})
    ul = soup.select("p  > a")
    print (ul)
    episodesList = []
    for item in ul:
        # print item.text
        # print item.get('href')
        # print url
        episodesList.append({"title": item.text, "url": item.get('href')})
    return episodesList
        
def getStreams(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')
    h3 = soup.find_all('input', {"class": "sublink"})
    sourceList = []
    turl = url.replace('clip/', 'clip/play.php?id=') + '&width=1005&height=550&dh=5-10&dh2=5-9&n='
    # turl = 'http://www.kseries.co/clip/play.php?id=1335106&width=1005&height=550&dh=5-10&dh2=5-9&n='
    for link in h3:
        sourceList.append({"title": link.get('value'), "url":  turl+link.get('id')})
    return sourceList



def k_getEpisodes(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    ul = soup.select("p  > a")
    episodesList = []
    for item in ul:
        episodesList.append({"title": item.text, "url": k_getStreams(item.get('href'))})
    return episodesList


def k_getStreams(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')
    h3 = soup.find_all('input', {"class": "sublink"})
    turl = url.replace('clip/','clip/play.php?id=') + '&width=1005&height=550&dh=5-10&dh2=5-9&n='
    for link in h3:
        kstream = k_stream(turl+link.get('id'))
        if kstream is not None:
            return kstream


def adFly(url):
    r = requests.get('http://skizzerz.net/scripts/adfly.php?url='+url)
    soup = BeautifulSoup(r.text , 'html5lib')
    return soup.find('a').get('href')

def yandex(url):
    try:
        s = requests.Session()
        r = s.get(url)
        r = re.sub(r'[^\x00-\x7F]+',' ', r.text)

        sk = re.findall('"sk"\s*:\s*"([^"]+)', r)[0]

        idstring = re.findall('"id"\s*:\s*"([^"]+)', r)[0]

        idclient = binascii.b2a_hex(os.urandom(16))

        post = {'idClient': idclient, 'version': '3.9.2', 'sk': sk, '_model.0': 'do-get-resource-url', 'id.0': idstring}
        #post = urllib.urlencode(post)

        r = s.post('https://yadi.sk/models/?_m=do-get-resource-url', data=post)
        r = json.loads(r.text)

        url = r['models'][0]['data']['file']

        return url
    except:
        return

def getSpecialEpisodes(url,find='p'):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.find('div', {"class": "post-wrapper"})

    p = ul.findAll(find)

    epsList = []
    last = None
    for eps in p:
        if last == None:
            last=eps
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
                        subject=epstext
                    else:
                        subject = last.text
            
            subject = re.sub('\n.*','',subject)
            if u'פרק' in subject:
                epsList.append({'title':subject,'url':a})
        last = eps
    
    if epsList == [] and find=='p':
        return getSpecialEpisodes(url,'address')
        
    return epsList

def getSpecialStreams(url,episode):
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

def k_stream(url):
    r = requests.get(url)
    s = re.compile('file.."(.*?)"').findall(r.text)
    url = s[0]
    return url

#print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
#print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
# print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
# print getStreams()