import HTMLParser
import requests,re,urllib,os,json,binascii,sys
from bs4 import BeautifulSoup

strmlist =[]
def mastermov(url):
    # url ='https://kod-hd.com/2018/01/29/mother-2017-%e0%b8%a1%e0%b8%b2%e0%b8%a3%e0%b8%94%e0%b8%b2-hd/'
    # url = 'https://www.mastermovie-hd.com/blade-runner-2049-%E0%B9%80%E0%B8%9A%E0%B8%A5%E0%B8%94-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-2049/'
    url =getitems(url,' class="item-content.*\n.*\n.*?href="([^"]+)')
    if url is not None:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        div = soup.findAll('div', {"id": "video_main"})
        for frm in div:
            # print
            strm = frm.find('iframe').get('src')
            strmlist.append({"url":strm,"title":'Mastermovie-HD >> '+chksrv(strm)})
    return strmlist


def nungsub(url):
    # url = 'https://nungsub.com/blade-runner-2049-2017-%E0%B9%80%E0%B8%9A%E0%B8%A5%E0%B8%94-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-2049/'
    url = getitems(url,'class="item-conten.*?href="([^"]+)"')
    print url
    if url is not None:
        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text
        opt  = re.compile('<option.value="(.*?)"').findall(r)
        # print opt

        for frm in opt:
            id = frm
            # print id
            surl=url+'?Player='+id
            # print surl
            r = requests.get(surl)
            r = HTMLParser.HTMLParser().unescape(r).text
            strm = re.compile('<div class="text_player.*?iframe.*?src="(.*?)"').findall(r)
            # print strm[0]
            strmlist.append({"url": strm[0], "title": 'Nungsub >> '+chksrv(strm[0])})
    return strmlist

def Kodhd(url):
    url = getitems(url,'class="moviefilm.*?href="([^"]+)"')
    # print url1
    if url is not None:
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        # div = soup.find('h2', {"style": "text-align: center;"})
        ifm = soup.findAll('iframe',{'height':"400"})
        # print ifm
        for src in ifm:
            # print src
            strm= src.get('src')
            # if strm != 'https://donungvip.com/vip/':
                # print strm +' (kod-hd)'
            strmlist.append({"url":strm, "title": 'KOD-HD >> '+chksrv(strm)})
    return strmlist
    # print div


def nana(url):
    # url = 'https://www.nanamovies.com/%E0%B8%94%E0%B8%B9%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87-maze-runner-death-cure-2018-%E0%B9%80%E0%B8%A1%E0%B8%8B-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-%E0%B9%84/'
    url = getitems(url,'class="film-list-playbtn.*?href="([^"]+)"')
    if url is not None:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        ul = soup.find('ul', {"class": "film-part-tabs"})
        li = ul.findAll('li')
        for l in li:
            surl = l.find('a').get('href')
            r = requests.get(surl)
            r = HTMLParser.HTMLParser().unescape(r).text
            strm = re.compile('<iframe.*?src="(.*?)"').findall(r)
            # print strm[0] +' (Nana)'
            strmlist.append({"url": strm[0], "title": 'Nanamovie >> '+chksrv(strm[0])})
    return strmlist

    # source = requests.get(url, headers=headers)
    # r = HTMLParser.HTMLParser().unescape(r).text
    # opt = re.compile('<li><a href="(.*?)"').findall(r)
    # for item in opt:
    #     print item
            #     print  frm.find('iframe').get('src')

def hd037(url):
    # url = 'https://www.037hd.com/maze-runner-death-cure-2018-%E0%B9%80%E0%B8%A1%E0%B8%8B-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-%E0%B9%84%E0%B8%82%E0%B9%89%E0%B8%A1%E0%B8%A3%E0%B8%93%E0%B8%B0/'
    # url = 'https://www.037hd.com/foreigner-2017-2-%e0%b9%82%e0%b8%84%e0%b8%95%e0%b8%a3%e0%b8%9e%e0%b8%a2%e0%b8%b1%e0%b8%84%e0%b8%86%e0%b9%8c%e0%b8%9c%e0%b8%b9%e0%b9%89%e0%b8%a2%e0%b8%b4%e0%b9%88%e0%b8%87%e0%b9%83%e0%b8%ab/"'
    url = getitems(url, 'class="moviefilm.*\n.*?href="([^"]+)"')
    if url is not None:
        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text
        player = re.compile('<iframe.*?src="(.*?leoplay.*?)"').findall(r)
        # soup = BeautifulSoup(r.text, 'html5lib')
        # soup.prettify()
        # div = soup.find('h2', {"style": "text-align: center;"})
        # print len(player)
        for surl in player:
            if len(player)>2:
                # print surl + ' (037HD)'
                strmlist.append({"url": surl , "title": '037HD >> '+chksrv(surl)})
            # return strmlist
            else:
            # print item
                r = requests.get(surl)
                r = HTMLParser.HTMLParser().unescape(r).text
                play = re.compile('<li><a href="(.*?)"').findall(r)
                for leo in play:
                    r = requests.get(leo)
                    r = HTMLParser.HTMLParser().unescape(r).text
                    strm = re.compile('<iframe.*?src="(.*?)"').findall(r)
                    # print strm[0]
                    # strhost = strm[0]
                    # strhost = strhost[strhost.find('//')+2:strhost.find('.')].capitalize()
                    strmlist.append({"url": strm[0], "title": '037HD >> '+chksrv(strm[0])})
    return strmlist

def youhd(url):
    # url = 'https://www.2youhd.com/2018/01/30/mother-2017-%e0%b8%a1%e0%b8%b2%e0%b8%a3%e0%b8%94%e0%b8%b2/'
    # url = 'https://www.2youhd.com/2018/01/25/open-house-2018-%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B8%AB%E0%B8%A5%E0%B8%AD%E0%B8%99-%E0%B8%AA%E0%B8%B1%E0%B8%A1%E0%B8%9C%E0%B8%B1%E0%B8%AA%E0%B8%AA/'
    'https://www.2youhd.com/?s=Nai-Kai-Jeow+(2017)'
    url = getitems(url, 'class="moviefilm.*\n.*?href="([^"]+)"')
    if url is not None:
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        div = soup.find('div', {"class": 'filmicerik'})
        ifm = div.findAll('iframe', {'scrolling': "no"})
        # print  div
        for src in ifm:
            strm = src.get('src')
            strmlist.append({"url": strm, "title": '2youHD  >> '+chksrv(strm)})
    return strmlist


def nung9(url):
    # url = 'https://www.9nung.com/26306/'

    url = getitems(url,'class="thumb.*\n.*?href="([^"]+)"')
    if url is not None:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        div = soup.find('div', {"class": 'textbox clearfix'})
        ifm = div.findAll('iframe', {'height': "360"})
        # print  div
        for src in ifm:
            # print
            strm = src.get('src')
            strmlist.append({"url":strm ,"title":'9nung >> '+chksrv(strm)})
    return strmlist

def vojkud(url):
    # url = 'https://www.vojkud.com/the-foreigner-2017-2-%E0%B9%82%E0%B8%84%E0%B8%95%E0%B8%A3%E0%B8%9E%E0%B8%A2%E0%B8%B1%E0%B8%84%E0%B8%86%E0%B9%8C%E0%B8%9C%E0%B8%B9%E0%B9%89%E0%B8%A2%E0%B8%B4%E0%B9%88%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/'
    url = getitems(url,'class="boxinfo.*\n.*?href="([^"]+)"')
    # print url
    if url is not None:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        div = soup.find('div', {"id": 'player2'})
        ifm = div.findAll('iframe', {'scrolling': "no"})
        # print  div
        # print ifm
        for src in ifm:
            strm = src.get('data-lazy-src')
            strmlist.append({"url": strm, "title": 'vojkud  >> '+chksrv(strm)})
    return strmlist

def chksrv(s): # check server streaming
    if 'www' in s:
        return s.split('.')[1].capitalize()
    else:        # print
        return (s[s.find('/') + 2 :s.find('.')]).capitalize()

def getitems(url,regtext):
    r = requests.get(url).text
    r = HTMLParser.HTMLParser().unescape(r)
    matchpag = re.compile(regtext).findall(r)
    # print matchpag
    if len(matchpag) > 0:
        return matchpag[0]



def fidmov(url):
    # params = plugintools.get_params()
    # action = params.get('action')
    if 'kod-hd' in url:
        Kodhd(url)
        return strmlist
    elif '037hd' in url:
        hd037(url)
        return strmlist
    elif 'www.mastermovie-hd.com' in url:
        mastermov(url)
        return strmlist
    elif 'nanamovies' in url:
        nana(url)
        return strmlist
    elif 'nungsub.com' in url:
        nungsub(url)
        return strmlist
    elif '2youhd.com' in url:
        youhd(url)
        return strmlist
    elif '9nung.com' in url:
        nung9(url)
        return strmlist
    elif 'vojkud.com' in url:
        vojkud(url)
        return strmlist
    return strmlist



# print vojkud('http://www.vojkud.com/?s=Nai-Kai-Jeow+(2017)')
# print hd037()
# nung9()
# getMaster()
# print nungsub('http://www.nungsub.com/?s=blade-runner-2049-2017')
# nana()

# url = 'https://www.nanamovies.com/%E0%B8%94%E0%B8%B9%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87-maze-runner-death-cure-2018-%E0%B9%80%E0%B8%A1%E0%B8%8B-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-%E0%B9%84/'
# url = 'https://www.vojkud.com/the-foreigner-2017-2-%E0%B9%82%E0%B8%84%E0%B8%95%E0%B8%A3%E0%B8%9E%E0%B8%A2%E0%B8%B1%E0%B8%84%E0%B8%86%E0%B9%8C%E0%B8%9C%E0%B8%B9%E0%B9%89%E0%B8%A2%E0%B8%B4%E0%B9%88%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88/'
# url = 'https://www.mastermovie-hd.com/blade-runner-2049-%E0%B9%80%E0%B8%9A%E0%B8%A5%E0%B8%94-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-2049/'
# url = 'https://www.nanamovies.com/%E0%B8%94%E0%B8%B9%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87-breathe-2017-%E0%B9%83%E0%B8%88%E0%B8%9A%E0%B8%B1%E0%B8%99%E0%B8%94%E0%B8%B2%E0%B8%A5%E0%B9%83%E0%B8%88-hd/'
# print nana(url)
# url = 'https://www.nanamovies.com/?s=breath'
# print fidmov(url)
# url = 'https://kod-hd.com/2018/01/29/mother-2017-%e0%b8%a1%e0%b8%b2%e0%b8%a3%e0%b8%94%e0%b8%b2-hd/'
# url = 'https://kod-hd.com/?s=Nai-Kai-Jeow+(2017)'
# url = 'https://www.037hd.com/maze-runner-death-cure-2018-%E0%B9%80%E0%B8%A1%E0%B8%8B-%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C-%E0%B9%84%E0%B8%82%E0%B9%89%E0%B8%A1%E0%B8%A3%E0%B8%93%E0%B8%B0/'
# url = 'https://www.037hd.com/foreigner-2017-2-%e0%b9%82%e0%b8%84%e0%b8%95%e0%b8%a3%e0%b8%9e%e0%b8%a2%e0%b8%b1%e0%b8%84%e0%b8%86%e0%b9%8c%e0%b8%9c%e0%b8%b9%e0%b9%89%e0%b8%a2%e0%b8%b4%e0%b9%88%e0%b8%87%e0%b9%83%e0%b8%ab/"'
# url = 'https://www.037hd.com/nai-kai-jeow-2017-%E0%B8%99%E0%B8%B2%E0%B8%A2%E0%B9%84%E0%B8%82%E0%B9%88%E0%B9%80%E0%B8%88%E0%B8%B5%E0%B8%A2%E0%B8%A7-%E0%B9%80%E0%B8%AA%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B8%A7%E0%B8%95%E0%B8%AD/'
# print hd037(url)
# print Kodhd(url)
# url = 'https://www.2youhd.com/?s=Nai-Kai-Jeow+(2017)'
# print youhd(url)