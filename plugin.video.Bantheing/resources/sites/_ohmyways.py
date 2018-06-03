# -*- coding: utf-8 -*-
import xbmcgui


from _utility import y_soup, y_reguests, chksrv, get_title

baseurl = 'https://ohmyways.blogspot.com'
def getgenre():
    soup = y_soup(baseurl)
    print soup

    # matchpag = y_reguests(baseurl,regex='<li id="menu-item.*?menu-item-\d+"><a\shref="(.*?category.*?)".*?>(.*?)<')
    # matchpag = re.compile('custom menu-item-\d+"><a\shref="(.*?category.*?)">(.*?)<').findall(r)
    # movielist = []
    # for i in range(0, len(matchpag)):
    #       movielist.append({'title':matchpag[i][1], 'url':matchpag[i][0]})
    # return movielist

def getseries(url):
    soup = y_soup(url)
    slist = soup.findAll('div',{'class':'post'})

    # mlist = y_reguests(url, 'div class="featured clearfix.*\s.*?title="(.*?)".data-src="([^"]+)".class=.*?href="([^"]+)"')
    # print (mlist)
    serieslist = []
    if slist != []:
        for item in slist:
            surl = item.a.get('href')
            img = item.a.get('style')[15:-47]
            title = item.h2.text.strip()
            serieslist.append({'title': item[0], 'url': item[2], 'thumbnail': item[1]})

    next = y_reguests(url, '"next page-numbers..href="([^"]+)"')
    # print snext
    if next != None:
        serieslist.append({'title': u"Next", 'url': next[0]})
    return serieslist

def gettab(url):
    tablist = []
    list = y_reguests(url,'li.*?href="(.*?)".*?tab.*?internal.>(.*?)<')
    for tab in list:
        # print tab
        tablist.append({'url':url + tab[0], 'title': tab[1]})
    return tablist

def getepisode(url,thumbnail=None):
    eplist =[]
    list = y_reguests(url,'<p .*?<a href="([^"]+)".*?>(.*?)<')
    for ep in list:
        # print ep
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



if __name__ == '__main__':
    # getmov('https://utaseries.co/category/series-online/ซี่รี่ย์เกาหลี/ซีรี่ย์เกาหลี-ซับไทย/')
    # print getepisode('https://utaseries.co/series-online/miracle-that-we-met/')
    # print gettab('https://utaseries.co/miracle-that-we-met-ep1/')
    # print  getstreams('https://utaseries.co/miracle-that-we-met-ep1/')
    getgenre()
    # getseries('https://ohmyways.blogspot.com')
