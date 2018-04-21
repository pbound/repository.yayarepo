# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup

path = sys.path[0]+'/'

_session = requests.session()
web_login =  'https://www.friend-series.com/wp-login.php'
__headers1__ = {'Cookie': 'wordpress_test_cookie=WP Cookie check'}
__datas__ = {
    'log': 'pbound', 'pwd': 'jhuuYiCD007', 'wp-submit': 'Log In',
    'redirect_to': '', 'testcookie': '1'
}
_session.post(web_login, headers=__headers1__, data=__datas__)
# r = session.get('https://www.friend-series.com/')

def getMenu():
    r = _session.get('https://www.friend-series.com/')
    # r = requests.get('https://www.friend-series.com/')
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('ul', {"id": 'menu-sub-menu'})
    # print ul
    li= ul.findAll('li', {"class": "menu-item"})
    # print li
    seriesList = []
    for link in li:
        news = link.find('a').get('href')
        if news != 'https://www.friend-series.com/movies/':
            seriesList.append({'title': link.text.replace('\n', ''), 'url': link.find('a').get('href')})
    return seriesList


def getSeries(url):
    r = _session.get(url)
    # r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('div', {"class": "item_1 items"})
    div = ul.findAll('div', {"class": "item"})
    # print div
    seriesList = []
    for item in div:
        # print item.find('a').get('href')
        # print item.find('img').get('src')
        # print item.find('img').get('alt')

        img = item.find('img')
        seriesList.append({'title': img.get('alt'), 'url': item.find('a').get('href'), 'thumbnail': img.get('src')})
    # find next page
    next = soup.find('div', {'class': 'nav-previous alignleft'})
    # print next.find('a').get('href')
    if next != None:
        seriesList.append({'title': u"Next", 'url': next.find('a').get('href'), 'thumbnail': path+'nextpage.png'})
    return seriesList


def getEpisodes(url):
    r = _session.get(url)
    # r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    div = soup.find('div', {"class": "contenidotv"})

    # ul = div.findAll('div', {"class":"videos-l-li"})
    ul = div.findAll('a', {"class": "ajax-video"})
    # ul = soup.select("p  > a")
    # print (ul)
    episodesList = []
    for item in ul:
        # print item.get('title')
        # print item.get('href')
        # print url
        episodesList.append({"title": item.get('title'), "url": item.get('href')})
    return episodesList
        
def getStreams(url):
    r = _session.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')
    h3 = soup.find_all('input', {"class": "sublink"})
    sourceList = []
    turl = url.replace('clip/', 'clip/play.php?id=') + '&width=1005&height=550&dh=5-10&dh2=5-9&n='
    # turl = 'http://www.kseries.co/clip/play.php?id=1335106&width=1005&height=550&dh=5-10&dh2=5-9&n='
    for link in h3:
        sourceList.append({"title": link.get('value'), "url":  turl+link.get('id')})
    return sourceList





def F_stream(url):
    r = _session.get(url)
    # s = re.compile('file.."(.*?)"').findall(r.text)
    s = re.compile('<iframe src="([^"]+)"').findall(r.text)
    url = s[0]
    return url

#print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
#print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
# print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
# print getStreams()
# url = 'https://www.friend-series.com/watch/d-day-%e0%b8%8b%e0%b8%b1%e0%b8%9a%e0%b9%84%e0%b8%97%e0%b8%a2-hd-%e0%b8%95%e0%b8%ad%e0%b8%99%e0%b8%97%e0%b8%b5%e0%b9%88-01/'
# print F_stream(url)
# url = 'https://www.friend-series.com/tvseries-genre/%e0%b8%8b%e0%b8%b5%e0%b8%a3%e0%b8%b5%e0%b8%aa%e0%b9%8c%e0%b9%80%e0%b8%81%e0%b8%b2%e0%b8%ab%e0%b8%a5%e0%b8%b5/'
# print getSeries(url)
# print getEpisodes(url)
# print getMenu()