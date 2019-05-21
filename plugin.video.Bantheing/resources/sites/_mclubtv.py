import HTMLParser
import json
import re
import urllib
import urllib2

import requests
# play = 	var baselink = curServer;
# 	var folder = curFolder;
# 	var bitRate = channelsNumberList[curSelectID].channel.bitrates[curSelectBitRate].value;
# 	var streamid = channelsNumberList[curSelectID].channel.streamer;
# 	var urlString = "http://" + baselink + ":1935/" + folder + "/" + streamid +
# 									"_" + bitRate + "/playlist.m3u8";
# '
from bs4 import BeautifulSoup


#
headers = {
            # 'username': 'PsiCare',
            # 'password': 'dq3JTzXfz9eMYvPW',
            # 'secretkey': '4jeMW5',
            # 'function': 'GetAllChannelList',
            # 'Cookie':'__cfduid=da836966bcf7e727eda8dda308ea5b9071557904829; RCACHE:0=RCACHE%3A0; mvc_session=0e8ed05e7839aedc50ac8c642e4ceaefe4f1e0a6'
            # 'cookie':'username=myyaya; remember_code=rxeaGUmLgIXC5eFAAGDlde'#; mvc_session=d135823543741a542f8f034a9a23622bff658746'
            'cookie': 'RCACHE:0=RCACHE%3A0; username=myyaya; remember_code=rxeaGUmLgIXC5eFAAGDlde'
            # 'Content-Type': 'application/json; charset=UTF-8',
            # 'Content-Length': '2',
            # 'Host': 'apiservice.psisat.com',
            # 'Connection': 'Keep-Alive',
            # 'Accept-Encoding': 'gzip',
            # 'User-Agent': 'okhttp/3.8.0'

            }

def get_chlist():
    r= requests.get('https://www.movieclubhd.tv/th/live',headers=headers)
    # print r.content
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    div = soup.find('div',{'class':"tab-content"})
    data = div.findAll('a')

    # print result
    chlist=[]
    for ch in data:
        url = ch.get('href')
        title = ch.get('title').capitalize()
        thumnail = ch.img.get('src')
        # print source
        # name = source.split('/')[6].split('.')[0]
        # print name.capitalize()

        # print ch.find('img src')
        chlist.append({"url": url, "title": title, 'thumbnail': thumnail})
    return chlist





def getm3u(link):
    url = 'https://www.movieclubhd.tv/th/' + link.replace('.','')
    source = requests.get(url, headers=headers)
    link = re.compile('linkPlay = "([^"]+)";').findall(source.text)
    # print link[0]
    HEADERS = urllib.urlencode({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Referer': 'https://www.movieclubhd.tv/th/live?channel=mcothd_480p',
    })
    return link[0] + '|%s' % HEADERS
    # return link[0]


if __name__ == '__main__':
    # print getchunklist('http://symc-cdn02.bkk04.violin.co.th:1935/liveedge/292277143069_300/playlist.m3u8')
    # souptest()
    # willdel('http://psitv.tv/api/Channels')
    # jsontest('http://psitv.tv/api/Channels')
    # getchalist()
    # get_sesion()
    # getpost()
    # print test_2()
    print getm3u('./live?channel=00_skynetsport6')
    get_chlist()
