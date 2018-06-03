# -*- coding: utf-8 -*-
import xbmcgui


from _utility import y_soup, y_reguests, chksrv, get_title

baseurl = 'https://www.series-onlines.com/'
def getgenre():
    matchpag = y_reguests(baseurl,regex='<a href="(.*?category.*?)".*?>(.*?)<')
    # matchpag = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    movielist = []
    for i in range(0, len(matchpag)):
          movielist.append({'title':matchpag[i][1], 'url':matchpag[i][0]})
    return movielist

def getseries(url):
    mlist = y_reguests(url, 'moviefilm".*\s.*?href="([^"]+)".*\s.*?src="([^"]+)".alt="(.*?)"')
    # print (mlist)
    movieslist = []
    if mlist != []:
        for item in mlist:
            movieslist.append({'title': item[2], 'url': item[0], 'thumbnail': item[1]})

    next = y_reguests(url, 'nextpost.*?href="([^"]+)"')
    # print snext
    if next != None:
        movieslist.append({'title': u"Next", 'url': next[0]})
    return movieslist

def gettab(url):
    tablist = []
    list = y_reguests(url,'li.*?href="(.*?)".*?tab.*?internal.>(.*?)<')
    for tab in list:
        # print tab
        tablist.append({'url':url + tab[0], 'title': tab[1]})
    return tablist

def getepisode(url,thumbnail=None):
    eplist =[]
    list = y_reguests(url,'<a href="([^"]+)".*?>(.*?)<')
    for ep in list:
        print ep[0]
        eplist.append({'url':ep[0],'title':ep[1]})
    return eplist






def getstreams(url,title=None):
    orgtitle = get_title(title)
    # xbmcgui.Dialog().ok('test',title,orgtitle)
    if url is not None:
        url = url + '#tab' #call tab

        player = y_reguests(url,'iframe src="([^"]+)"')
        strmlist = []

        for strm in player:
            # print strm
            title = 'Uta > '+chksrv(strm) + orgtitle
            strmlist.append({"url": strm, "title": title})
    return strmlist

def getsearch(title):
    ssurl = baseurl + '/?s=' + str(title)
    return  getseries(ssurl)
def getsearchall(title):
    pass
def getsearchalls(title):

    ssurl = baseurl + '/?s=' + str(title)
    xbmcgui.Dialog().ok('title 037',ssurl)
    # print ssurl
    mlist =  getseries(ssurl)
    # print mlist
    xbmcgui.Dialog().ok('037hd', str(mlist))
    if mlist != []:
        surl = mlist[0].get('url')
        stitle = mlist[0].get('title')
        # print stitle
        return getstreams(surl,stitle)
def test_soup(url):
    soup = y_soup(url)
    div = soup.find('div',{'class':'filmicerik'})
    p = div.find('p')


    print p
    # for item in strm:
    #     print item




if __name__ == '__main__':
    # getmov('https://utaseries.co/category/series-online/ซี่รี่ย์เกาหลี/ซีรี่ย์เกาหลี-ซับไทย/')
    print getepisode('https://www.series-onlines.com/series-korea/wok-of-love-%E0%B8%8B%E0%B8%B1%E0%B8%9A%E0%B9%84%E0%B8%97%E0%B8%A2')
    # print gettab('https://utaseries.co/miracle-that-we-met-ep1/')
    # print  getstreams('https://utaseries.co/miracle-that-we-met-ep1/')
    # test_soup('https://www.series-onlines.com/series-korea/wok-of-love-%E0%B8%8B%E0%B8%B1%E0%B8%9A%E0%B9%84%E0%B8%97%E0%B8%A2')
