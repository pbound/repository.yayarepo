# -*- coding: utf-8 -*-
import HTMLParser
import requests,re,urllib,os,json,binascii,sys
import master,xbmcgui

from bs4 import BeautifulSoup

def gethosts():
    # mainlist.append({'title': u'', 'url': '', 'thumbnail': ''})
    mainlist =[]
    mainlist.append({'title': u'Movie2Free', 'url': 'https://www.movie2free.com','thumbnail':'https://www.movie2free.com/wp-content/themes/next/logo/logo.png'})
    mainlist.append({'title': u'037HD', 'url': 'https://www.037hd.com','thumbnail':'https://www.037hd.com/wp-content/uploads/2015/12/037HD_LOGO.png'})
    mainlist.append({'title': u'Nungsub', 'url': 'https://nungsub.com','thumbnail':'https://nungsub.com/wp-content/uploads/2017/05/head-_E0_B8_99_E0_B8_B0-min.jpg'})
    mainlist.append({'title': u'Kod-Hd', 'url': 'https://www.kod-hd.com', 'thumbnail': 'https://kod-hd.com/wp-content/uploads/2016/04/KOD-HD-1.png'})
    mainlist.append({'title': u'Mastermovie hd', 'url': 'https://www.mastermovie-hd.com', 'thumbnail': ''})
    mainlist.append({'title': u'2youHD', 'url': 'https://www.2youhd.com', 'thumbnail': 'https://www.2youhd.com/wp-content/uploads/2017/01/cooltext225441445291923.png'})
    mainlist.append({'title': u'9nung', 'url': 'https://www.9nung.com', 'thumbnail': 'http://9nung.com/wp-content/uploads/2016/01/logo.png'})
    mainlist.append({'title': u'NaNa movie', 'url': 'https://www.nanamovies.com', 'thumbnail': 'https://ssl.อัพรูป.com/firewall/getimg/database/embedupload/bc6e5f.jpg'})
    return mainlist

def getgenre(url ):
    genreg1 = 'class="nav-main-link.*?href="(.*?com\/.*?)".*?>(.*?)<' #movie2free
    genreg2 = 'custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<' #037HD
    genreg3 = 'item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"' #nungsub
    genreg4 = 'href="(.*?category\/.*?\/).*?title="(.*?)"' #movie-hd
    genreg5 = 'href="(.*?category.*?)".*?strong>(.*?)<' #nanamovie
    genreg6 = 'href="(.*?category.*?)">(.*?)<' #2youhd
    genreg7 = '<li class.*?<a href="(.*?see.*?)">(.*?)<' # 9nung
    genreg8 = 'category menu-item.*?a href="(.*?kod.hd.com.category\/.*?)">(.*?)<' #kod-hd


    genreg = (genreg1, genreg8, genreg2, genreg3, genreg5, genreg7, genreg6, genreg4)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
               }
    r = requests.get(url, headers=headers).text
    # r = HTMLParser.HTMLParser().unescape(r).text
    # print r
    for regenre in genreg:
        print regenre
        genmatch = re.compile(regenre).findall(r)
        print len(genmatch)
    # print match
        if len(genmatch) !=0:
            gerelist = []
            for i in range(0, len(genmatch)):
                # print genmatch[i][0]
                if 'http' in genmatch[i][0]:
                    gurl = genmatch[i][0]
                    title = genmatch[i][1]
                    # print gurl
                    # print title
                else:
                    gurl = genmatch[i][1]
                    title = genmatch[i][0]
                    # print title

                gerelist.append({'title':title, 'url':gurl})
            # print gerelist
            break
        else:
            gerelist = []
    return gerelist

def getmov(url):

    movreg1 = 'movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"'
    movreg2 = 'class="moviefilm">.*\n.*<a href="(.*?)".*\n.*img.src="(.*?)".alt="(.*?)"'
    movreg3 = 'div> <a href="([^"]+)".*?title="(.*?)".*?lazy.src="([^"]+)'
    movreg4 = '<a.href="([^"]+)".*\n.*\n.*\n.*?h3>(.*?)<.*\n.*?src="([^"]+)' #nana movie
    movreg5 = 'class="moviefilm.*?href="([^"]+)".*?src="([^"]+).*?alt="(.*?")'
    movreg6 = 'class="thumb.*\n.*?href="([^"]+)".title="(.*?)".*\n.*?src="([^"]+)'
    movreg7 = 'href="([^"]+)".*?title="(.*?)<.*?src="([^"]+)'

    movreg = (movreg1, movreg2, movreg3, movreg4, movreg5, movreg6, movreg7)

    r = requests.get(url)
    r = HTMLParser.HTMLParser().unescape(r).text
    movielist = []
    for movtxt in movreg:
        movmatch = re.compile(movtxt).findall(r)
        print len(movmatch)
        if len(movmatch) != 0:
        #
            for i in range(0, len(movmatch)):
                # print movmatch
                if '.jpg'in movmatch[i][1] or '.jpeg' in movmatch[i][1] and 'http' in movmatch[i][0]:
                    murl = movmatch[i][0]
                    Title = movmatch[i][2]
                    thumbnail = movmatch[i][1]
                elif 'http' in movmatch[i][1] and '.jpg' in movmatch[i][2]:
                    murl =  movmatch[i][1]
                    # print 'URL ='+murl

                    Title =   movmatch[i][0]
                    # print Title
                    thumbnail =   movmatch[i][2]

                elif 'http' in movmatch[i][0] and '.jpg' in movmatch[i][2] or '.jpeg' in movmatch[i][2]:
                    murl =  movmatch[i][0]
                    # print url
                    Title =   movmatch[i][1]
                    # print Title
                    thumbnail =   movmatch[i][2]
                movielist.append( {'title': Title, 'url': murl, 'thumbnail': thumbnail})
            break
        else:
            movielist = []

    return movielist
    #

def getnext(url):

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
        print len(matchnext)
        if  len(matchnext)== 1:
            break
        # else:
        #     matchnext = []



    print matchnext[0]
    # if matchnext != None:
    #     print matchnext[0]

def getMovies(url):
    movielist = []
    if 'movie2free' in url:
        regtext = 'movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            movielist.append({'title': mlt[i][0], 'url': mlt[i][1], 'thumbnail': mlt[i][2]})

            # thmb = mlt[i][2]
            # try:

                # thmb = thmb.decode('unicode_escape').encode('utf-8')
                # return thmb
                # print thmb
            # except:

                # return
                # print thmb

            movielist.append({'title': mlt[i][1].replace('Permalink to ',''), 'url': mlt[i][0], 'thumbnail': mlt[i][2]})

    return movielist

def getMovies_backup(url):
    movielist = []
    if 'movie2free' in url:
        regtext = 'movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            movielist.append({'title': mlt[i][0], 'url': mlt[i][1], 'thumbnail': mlt[i][2]})
    elif '037hd' in url:
        regtext = 'class="moviefilm">.*\n.*<a href="(.*?)".*\n.*img.src="(.*?)".alt="(.*?)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            movielist.append({'title': mlt[i][2], 'url': mlt[i][0], 'thumbnail': mlt[i][1]})
    else:
        regtext = 'class="entry-title"><a href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            # thmb = mlt[i][2]
            # try:

                # thmb = thmb.decode('unicode_escape').encode('utf-8')
                # return thmb
                # print thmb
            # except:

                # return
                # print thmb

            movielist.append({'title': mlt[i][1].replace('Permalink to ',''), 'url': mlt[i][0], 'thumbnail': mlt[i][2]})

    return movielist

    # next = soup.find('a', {'class': 'nextpostslink'})
    # if next != None:
    #     seriesList.append({'title': u"Next", 'url': next.get('href')})
    # return seriesList



def get_allstream(title):
    # title ='โคตรพยัคฆ์ผู้ยิ่งใหญ่'
    # title = title.decode('utf-8').replace(' ','+')
    # title = 'Blade%20Runner%202049%20(2017)%20%E0%B9%80%E0%B8%9A%E0%B8%A5%E0%B8%94%20%E0%B8%A3%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%99%E0%B8%AD%E0%B8%A3%E0%B9%8C%202049'
    # 'http://www.google.com/search?q=pizza&num=75'
    # url1 = 'https://www.2youhd.com/?s=Nai-Kai-Jeow+(2017)'
    # url = 'https://www.mastermovie-hd.com/?s=Thor+Ragnarok+(2017)'

    url = 'https://www.google.co.th/search?hl=th&q=' + title + '&num=30'
    # print url
    # default.arg(url)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': 'https://www.google.co.th'}
    page_data = requests.get(url, headers=headers).text
    page_data = HTMLParser.HTMLParser().unescape(page_data)
    page_data = page_data.encode('utf-8')
    # soup = BeautifulSoup(r.text, 'html5lib')
    matchpag = re.compile('<h3.class="r".*?href="([^"]+)"').findall(page_data)
    serv=('www.kod-hd.com','www.mastermovie-hd.com','www.nanamovie.com','www.nungsub.com','www.037hd.com','www.2youhd.com','www.9nung.com','www.vojkud.com')
    streamlist=[]
    # for it in serv:
        # print it
    # ul = soup.find('h2', {"class": "hd"})
    for item in matchpag:
            # print item
            streamlist=(master.fidmov(url=item))
    # print streamlist
    return streamlist

            # if it in item:
            # if serv in item:
            #     print '>> '+item
                # print master.fidmov(url=item)
def get_searchall(title):
    # title = 'Nai-Kai-Jeow (2017) นายไข่เจียว เสี่ยวตอร์ปิโด'
    title = title[0:title.find(')') + 1].replace(' ', '+')
    # print title
    # url1 = 'https://www.2youhd.com/?s=Nai-Kai-Jeow+(2017)'
    # url = 'https://www.mastermovie-hd.com/?s=Thor+Ragnarok+(2017)'
    serv = ('www.kod-hd.com', 'www.mastermovie-hd.com', 'www.nanamovies.com', 'www.nungsub.com', 'www.037hd.com',
            'www.2youhd.com', 'www.9nung.com', 'www.vojkud.com', 'www.movie2free.com')
    # start dialogbox progress here
    dialog = xbmcgui.DialogProgress()
    dialog.create('ค้นหา', ("Loading items"))
    num_urls = len(serv)
    # streamlist = []
    for index,it in enumerate(serv,1):
        if dialog.iscanceled():
            break
        percent = ((index + 1) * 100) / num_urls
        dialog.update(percent, ("processing lists"), ("%s") % (
            it))

        url = 'http://' + it + '/?s=' + str(title)
        # print url
        streamlist = master.fidmov(url)
    # print streamlist
    return streamlist


def getEpisodes(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.findAll('div', {"class": "symple-toggle state-closed "})
    
    episodesList = []
    for item in ul:
        episodesList.append({"title":item.find('h3').text,"url":url})
    return episodesList 
        
def getStreams(url,episode):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')
    strmlist = []
    if 'movie2free' in url:
        regtext = 'movie-title.*\n.*\n.*span>(.*?)<.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*href="(.*?)".*\n.*src="(.*?)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            strmlist.append({'title': mlt[i][0], 'url': mlt[i][1], 'thumbnail': mlt[i][2]})
    elif '037hd' in url:
        regtext = 'class="moviefilm">.*\n.*<a href="(.*?)".*\n.*img.src="(.*?)".alt="(.*?)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            strmlist.append({'title': mlt[i][2], 'url': mlt[i][0], 'thumbnail': mlt[i][1]})
    else:
        regtext = 'class="entry-title"><a href="([^"]+)".*?title="(.*?)".*?src="([^"]+)"'
        mlt = getitems(url, regtext)
        for i in range(0, len(mlt)):
            # thmb = mlt[i][2]
            # try:

                # thmb = thmb.decode('unicode_escape').encode('utf-8')
                # return thmb
                # print thmb
            # except:

                # return
                # print thmb

            strmlist.append({'title': mlt[i][1].replace('Permalink to ',''), 'url': mlt[i][0], 'thumbnail': mlt[i][2]})

    return strmlist
#
#     # h3 = soup.find('h3', text=lambda x: x and x==episode.decode('utf-8'))
#
#     sourceList = []
#     h3parent = []
#     try:
#         h3parent = h3.parent.findAll('a')
#     except:
#         h3parent =[]
#     if h3parent == []:
#         h3parent = getSpecialStreams(url, episode)
#     for link in h3parent:
#         linkurl = link.get('href')
#         if "adf.ly" in linkurl.lower():
#             if '/http' in linkurl.lower():
#                 linkurl = re.sub(r'.*http', 'http', linkurl.replace('http://adf.ly/',''))
#             else:
#                 linkurl = adFly(linkurl)
#         sourceList.append({"title":linkurl,"url":linkurl})
#     return sourceList
#
# def adFly(url):
#     r = requests.get('http://skizzerz.net/scripts/adfly.php?url='+url)
#     soup = BeautifulSoup(r.text , 'html5lib')
#     return soup.find('a').get('href')
def leo(url):
    r = requests.get(url).text
    r = HTMLParser.HTMLParser().unescape(r)
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
    #            'Referer': 'https://stream.movie2free.com/api/sources/1371'}
    # page_data = requests.get(url, headers=headers).text
    # page_data = HTMLParser.HTMLParser().unescape(page_data)
    # r = r.decode('unicode_escape').encode('utf-8')

    # r.encoding = "utf-8"
    # if 'movie2free' in url:
    streamitems = re.compile('file.."([^"]+)"').findall(r)
    labelitem = re.compile('label."(.*?)"').findall(r)
    # print matchpag
    # for label in matchpag:
    #     print label
    # menuItems = [u'360p', u'720p', u'1080p']
    select = xbmcgui.Dialog().select('title', labelitem)

    if select == -1:
        return None
    else:
        return streamitems[select]

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

def getitems(url,regtext):
    r = requests.get(url).text
    r = HTMLParser.HTMLParser().unescape(r)
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
    #            'Referer': 'https://stream.movie2free.com/api/sources/1371'}
    # page_data = requests.get(url, headers=headers).text
    # page_data = HTMLParser.HTMLParser().unescape(page_data)
    # r = r.decode('unicode_escape').encode('utf-8')

    # r.encoding = "utf-8"
    # if 'movie2free' in url:
    matchpag = re.compile(regtext).findall(r)
    # elif '037hd' in url:
    #     matchpag = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    # else:
    #     matchpag =re.compile('item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"').findall(r)
    # print len(matchpag)
    return matchpag
    #     matchpag
    # gerelist = []
    # for i in range(0, len(matchpag)):
    #     if 'nungsub'in url:
    #         gerelist.append({'title': matchpag[i][0], 'url': matchpag[i][1]})
    #     else:
    #       print matchpag[i][0]
    #       print matchpag[i][1]
    #       gerelist.append({'title':matchpag[i][1], 'url':matchpag[i][0]})
    # return gerelist
# if __name__ == '__main__':

    #print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
    #print getEpisodes("http://www.asia4hb.com/view/my-dear-cat")
    #print getSpecialStreams('http://www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
    # url = 'https://www.movie2free.com'
    # regtext = 'class="nav-main-link.*?href="(.*?)".*?>(.*?)<'
    # url = 'https://nungsub.com/'
    # print getMenu(url)
    # print getMovies(url)
    # print getitems(url,regtext)
    # print getMovieslist()
    # getStreams(url,title)
    # title ='Nai-Kai-Jeow (2017) นายไข่เจียว เสี่ยวตอร์ปิโด'
    # get_allstream(title)
    # get_searchall()
    # print leo('https://www.leoplayer5.com/watch5?v=908485')
    # getgenre('http://www.nungsub.com')
    # getgenre(url = 'https://www.mastermovie-hd.com/')
    # getmov('https://www.nanamovies.com/category/%e0%b9%81%e0%b8%99%e0%b8%a7%e0%b8%a0%e0%b8%b2%e0%b8%9e%e0%b8%a2%e0%b8%99%e0%b8%95%e0%b8%a3%e0%b9%8c/%e0%b8%9a%e0%b8%b9%e0%b9%89-action/')
    # getmov('https://www.mastermovie-hd.com/category/%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88-2015/')