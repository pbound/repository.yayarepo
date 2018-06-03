# -*- coding: utf-8 -*-
import HTMLParser

import re
import requests
from bs4 import BeautifulSoup


class webmov:
    def __init__(self, url=None, regenre=None, rexmov='th'):
        self.url = url
        self.regenre = regenre
        self.country = rexmov

    def getgenre(self, url ):
        genreg1 = 'class="nav-main-link.*?href="(.*?category.*?)".*?>(.*?)<' #movie2free
        genreg2 = 'custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<' #037HD
        genreg3 = 'item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"' #nungsub
        genreg4 = 'href="(.*?category.*?)".*>.*\n(.*?)\n' #movie-hd
        genreg5 = 'href="(.*?category.*?)".*?strong>(.*?)<' #nanamovie
        genreg6 = 'href="(.*?category.*?)">(.*?)<' #2youhd
        genreg7 = '<li class.*?<a href="(.*?see.*?)">(.*?)<' # 9nung
        genreg8 = 'category menu-item.*?a href="(.*?kod.hd.com.category\/.*?)">(.*?)<' #kod-hd


        genreg = (genreg1, genreg8, genreg2, genreg3, genreg5, genreg7, genreg6, genreg4)



        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text
        for regenre in genreg:
            genmatch = re.compile(regenre).findall(r)
            print len(genmatch)
        # print match
            if len(genmatch) !=0:
                gerelist = []
                for i in range(0, len(genmatch)):
                    # print match[i]
                    if 'http' in genmatch[i][0]:
                        self.gurl = genmatch[i][0]
                        title = genmatch[i][1]
                        print title
                    else:
                        self.gurl = genmatch[i][1]
                        title = genmatch[i][0]
                        print title

                    gerelist.append({'title':title, 'url':self.gurl})
                print gerelist
                break
            else:
                gerelist = []
        return gerelist

    def getmov(self,url):

        movreg1 = 'movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"'
        movreg2 = 'class="moviefilm">.*\n.*<a href="(.*?)".*\n.*img.src="(.*?)".alt="(.*?)"'
        movreg3 = 'div> <a href="([^"]+)".*?title="(.*?)".*?lazy.src="([^"]+)'
        movreg4 = '<a.href="([^"]+)".*\n.*\n.*\n.*?h3>(.*?)<.*\n.*?src="([^"]+)'
        movreg5 = 'class="moviefilm.*?href="([^"]+)".*?src="([^"]+).*?alt="(.*?")'
        movreg6 = 'class="thumb.*\n.*?href="([^"]+)".title="(.*?)".*\n.*?src="([^"]+)'
        movreg7 = 'div.*\n.*?href="([^"]+).*?title="(.*?)".*?src="([^"]+)'

        movreg = (movreg1, movreg2, movreg3, movreg4, movreg5, movreg6, movreg7)

        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text

        for movtxt in movreg:
            movmatch = re.compile(movtxt).findall(r)
            print len(movmatch)
            if len(movmatch) != 0:

                for i in range(0, len(movmatch)):
                    if '.jpg'in movmatch[i][1] and 'http' in movmatch[i][0]:
                        print 'url>> '+movmatch[i][0]
                        print 'Title>>'+movmatch[i][2]
                        print 'Thumbnail..'+movmatch[i][1]
                    elif 'http' in movmatch[i][1] and '.jpg' in movmatch[i][2]:
                        print 'url>> ' + movmatch[i][1]
                        print 'Title>>' + movmatch[i][0]
                        print 'Thumbnail..' + movmatch[i][2]
                    elif 'http' in movmatch[i][0] and '.jpg' in movmatch[i][2]:
                        print 'url>> ' + movmatch[i][0]
                        print 'Title>>' + movmatch[i][1]
                        print 'Thumbnail..' + movmatch[i][2]
                break
        self.getnext(url)

    def getnext(self,url):

        nextreg1 ='href="([^"]+page\/.*?\/)">'
        nextreg2 = 'href="([^"]+)">Next'
        nextreg3 = 'next..href="([^"]+)">'
        nextreg4 = 'next.*?href="([^"]+)">'

        nextreg = (nextreg1,nextreg2,nextreg3,nextreg4)

        r = requests.get(url)
        r = HTMLParser.HTMLParser().unescape(r).text
        for txt in nextreg:
            matchnext = re.compile(txt).findall(r)
            # print matchnext
            # print len(matchnext)
            if  len(matchnext)== 1:
                return matchnext[0]
                break
            # else:
            #     matchnext = []




        # if matchnext != None:
        #     print matchnext[0]

    def getmovSoup(self,url):
        r = requests.get(url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, 'html5lib')
        soup.prettify()
        ul = soup.findAll('div', {"class": "moviefilm"})
        print (ul)
        if len(ul) ==0:
            ul = soup.findAll('div', {"class": "item col220"})
        # div = ul.findAll('div', {"class": "moviefilm"})

        seriesList = []
        for item in ul:
            # print item
            print item.find('a').get('href')
            print item.find('img').get('src')
            print item.find('img').get('alt')
            # seriesList.append({'title': img.get('alt'), 'url': img.parent.get('href'), 'thumbnail': img.get('src')})

        next = soup.find('a', {'class': 'nextpostslink'})
        # next = soup.find('div', {'class': 'navigation'})
        if next != None:
            # print next
            print next.get('href')
            seriesList.append({'title': u"Next", 'url': next.get('href')})
        return seriesList


if __name__ == '__main__':
    m2f = webmov()
    # m2f.getgenre(url="https://www.movie2free.com", regenre='class="nav-main-link.*?href="(.*?)".*?>(.*?)<')
    # m2f.getmov(url='https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%ad%e0%b8%ad%e0%b8%81%e0%b9%83%e0%b8%ab%e0%b8%a1%e0%b9%88/',rexmov='movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"')
    # webmov.getgenre(m2f,url='https://www.037hd.com', regenre= 'custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<')
    # m2f.getgenre(url='https://nungsub.com',regenre='item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"')
    # m2f.getmov(url='https://www.037hd.com',rexmov='class="moviefilm">.*\n.*<a href="(.*?)".*\n.*img.src="(.*?)".alt="(.*?)"')
    # m2f.getmov(url='https://nungsub.com',rexmov='div> <a href="([^"]+)".*?title="(.*?)".*?lazy.src="([^"]+)')
    # m2f.getmov(url='https://www.nanamovies.com/category/%E0%B9%81%E0%B8%99%E0%B8%A7%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%A2%E0%B8%99%E0%B8%95%E0%B8%A3%E0%B9%8C/adventure-%E0%B8%9C%E0%B8%88%E0%B8%8D%E0%B8%A0%E0%B8%B1%E0%B8%A2/',rexmov='<a.href="([^"]+)".*\n.*\n.*\n.*?h3>(.*?)<.*\n.*?src="([^"]+)')
    # m2f.getmov(url='https://www.2youhd.com/',rexmov='class="moviefilm.*\n.*?href="([^"]+)".*\n.*?src="([^"]+).*?alt="(.*?)"')
    # m2f.getmov(url='https://www.9nung.com',rexmov='class="thumb.*\n.*?href="([^"]+)".title="(.*?)".*\n.*?src="([^"]+)')
    # m2f.getmov(url='https://www.mastermovie-hd.com',rexmov='div.*\n.*?href="([^"]+).*?title="(.*?)".*?src="([^"]+)')
    # m2f.getmov(url='https://kod-hd.com/category/27/',rexmov='class="moviefilm.*?href="([^"]+)".*?src="([^"]+).*?alt="(.*?")')
    # m2f.getmovSoup(url='https://kod-hd.com/category/27/')
    # m2f.getmovSoup(url='https://www.2youhd.com/')
    # m2f.getmovSoup(url='https://www.037hd.com')
    # m2f.getmovSoup(url='https://www.mastermovie-hd.com/category/new/')

    print m2f.getnext(url="https://www.movie2free.com/top-imdb/")
    # m2f.getnext(url='https://www.mastermovie-hd.com/category/new/page/29/',rexnext='href="([^"]+)">Next')
    # m2f.getnext(url='https://www.037hd.com/page/29/', rexnext='next..href="([^"]+)">')
    # m2f.getnext(url='https://www.2youhd.com/page/29/', rexnext='next..href="([^"]+)">')
    # m2f.getnext(url='https://kod-hd.com/category/27/page/29/', rexnext='next..href="([^"]+)">')
    # m2f.getnext(url='https://www.9nung.com/page/29/', rexnext='next..href="([^"]+)">')
    # m2f.getnext(url='https://www.nanamovies.com/category/%e0%b9%81%e0%b8%99%e0%b8%a7%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%a2%e0%b8%99%e0%b8%95%e0%b8%a3%e0%b9%8c/horror-%e0%b8%aa%e0%b8%a2%e0%b8%ad%e0%b8%87%e0%b8%82%e0%b8%a7%e0%b8%b1%e0%b8%8d/page/17/', rexnext='next.*?href="([^"]+)">')
    # m2f.getnext(url='https://nungsub.com/page/29/', rexnext='href="([^"]+)">Next')
    # m2f.getnext('https://nungsub.com/soundtrack-%e0%b8%8b%e0%b8%b1%e0%b8%9a%e0%b9%84%e0%b8%97%e0%b8%a2/page/29/')
    # m2f .getmov('https://www.mastermovie-hd.com')
    # m2f.getgenre('https://kod-hd.com')
    # m2f.getmov('https://www.nanamovies.com/category/%e0%b9%81%e0%b8%99%e0%b8%a7%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%a2%e0%b8%99%e0%b8%95%e0%b8%a3%e0%b9%8c/%e0%b8%9a%e0%b8%b9%e0%b9%89-action/')
    # m2f.getmov('https://www.movie2free.com/')