# -*- coding: utf-8 -*-
from _utility import y_soup,y_reguests,get_title,chksrv
baseurl = 'https://nungsub.com'
def getgenres():
    regex = 'item.97[5-6]\d"><a.title="(.*?)".href="(https...nungsub.com.so.*?)"'
    matchpag = y_reguests('https://nungsub.com',regex=regex)
    movielist = []
    for i in range(0, len(matchpag)):
        movielist.append({'title': matchpag[i][0], 'url': matchpag[i][1]})
    return movielist
def getgenre():
    soup = y_soup('https://nungsub.com')
    ul = soup.findAll('li', {"class": "cat-item"})
    # print (ul)?
    genreslist = []
    for items in ul:
        gtitle = items.text.strip()
        if 'VIP' not in gtitle:
            gurl =  items.find('a').get('href')
            genreslist.append({'title': gtitle, 'url': gurl})
    return genreslist

def getmov(url):
    mlist = y_reguests(url, 'div> <a href="([^"]+)".*?title="(.*?)".*?data.*?src="([^"]+)')
    movieslist = []
    for item in mlist:
        movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})

    next = y_reguests(url, "current.*?href='([^']+)'")
    # print snext
    if next != None:
        movieslist.append({'title': u"Next", 'url': next[0]})
    return movieslist

def getstreams(url,title=None):
    # orgtitle = get_title(title)
    strmlist = []
    opt = y_reguests(url,regex='<option.value="(.*?)"')
    if opt != None:
        for frm in opt:
            id = frm
            # print id
            surl = url + '?Player=' + id
            # print surl
            # r = requests.get(surl)
            # r = HTMLParser.HTMLParser().unescape(r).text
            strm = y_reguests(surl,'<iframe.*?src="(http+[^"]+)"')
            if len(strm) > 0:
                strmlist.append({"url": strm[0], "title": 'Nungsub >> ' + chksrv(strm[0])})


        return strmlist
def getsearch(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist = y_reguests(ssurl,'div> <a href="([^"]+)".*?title="(.*?)".*?data.*?src="([^"]+)')
    movieslist = []
    for item in mlist:
        movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})
    return movieslist

def getsearchall(title):
    ssurl = baseurl + '/?s=' + str(title)
    mlist = y_reguests(ssurl,'div> <a href="([^"]+)".*?title="(.*?)".*?data.*?src="([^"]+)')
    if mlist != None:
        surl = mlist[0][0]
        stitle = mlist[0][1]
        return getstreams(surl,title=stitle)

if __name__ == '__main__':

# print getgenre()
#     print getmov('https://nungsub.com/soundtrack-%E0%B8%8B%E0%B8%B1%E0%B8%9A%E0%B9%84%E0%B8%97%E0%B8%A2/full-hd/new-hot-movie/')
#     print getstreams('https://nungsub.com/fifty-shades-freed-2018/')
    print getsearchall('who am i')