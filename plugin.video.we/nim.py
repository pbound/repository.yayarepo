# -*- coding: utf-8 -*-
import json,plugintools
import os
import re
import urllib
import urllib2

import requests
import sys
import xbmcgui
from bs4 import BeautifulSoup
from base64 import b64decode
tmplastpath = plugintools.get_temp_path()+"\info_.json"
baseurl = 'http://www.we-play.tv/'
srbaseurl = b64decode('aHR0cHM6Ly93d3cudml1LmNvbS9vdHQvdGgvaW5kZXgucGhwP3I9dm9kL2FqYXgtZGV0YWlsJnBsYXRmb3JtX2ZsYWdfbGFiZWw9d2ViJmFyZWFfaWQ9NCZsYW5ndWFnZV9mbGFnX2lkPTQmcHJvZHVjdF9pZD0=')
fbaseurl = b64decode('aHR0cHM6Ly9kZnA2cmdsZ2pxc3prLmNsb3VkZnJvbnQubmV0L2luZGV4LnBocD9yPXYxL3NlYXJjaC92aWRlbyZsYW5ndWFnZV9mbGFnX2lkPTQ=')
stmbaseurl = b64decode('aHR0cHM6Ly9kMWsydXM2NzFxY29hdS5jbG91ZGZyb250Lm5ldC9kaXN0cmlidXRlX3dlYl90aC5waHA/Y2NzX3Byb2R1Y3RfaWQ9')
caturl = baseurl + '?r=category/series-category&platform_flag_label=web&area_id=4&language_flag_id=4&'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
           'referer': 'http://www.we-play.tv/'}
def getgenre():
    r = requests.get(url=baseurl,headers=headers)
    # print r.content
    #
    # r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    li = soup.findAll('li', {'class': "nav-item"})[1:-2]
    # li = ul.findAll('a', {'class': ''})
    seriesList = []
    print (li)
    for link in li:
        surl = link.find('a').get('href')
        # print link.text.replace('\n', '')
        # print link.find('a').get('href')
        seriesList.append({'title': link.text.replace('\n', ''), 'url': surl})

    return seriesList
    # movieslist = []
    # if mlist != []:
    #     for item in mlist:
    #         movieslist.append({'title': item[1], 'url': item[0], 'thumbnail': item[2]})

def getcategory(url):
    # url = 'https://we-play.tv/movies'
    r = requests.get(url,headers=headers)
    # print r.content
    #
    # r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    li = soup.findAll('div', {'class': "col-sm-6 text-left mb-1 mt-4"})
    # li = ul.findAll('a', {'class': ''})
    seriesList = []
    # print (li)
    for link in li:
        # print link
        surl = link.find('a').get('href')
        # print link.text.replace('\n', '')
        # print link.find('a').get('href')
        seriesList.append({'title': link.text.replace('\n', ''), 'url': surl})

    return seriesList

def getseries(url):
    r = requests.get(url=url, headers=headers)
    # result = re.compile('iframe src="([^"]+)"').findall(r.text)
    # print r.content
    #
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    li = soup.findAll('a', {'class': "slide-one slide-two"})
    sourcelist = []
    # print (li)
    for link in li:
        # print link
        surl = link.get('href')
        thumnail = link.find('img').get('data-src')
        title = link.find('div', {'class': "slide-content"}).h2.text.replace('\n', '')
        # print title,thumnail,surl
        sourcelist.append(
            {"title": title, "url": surl, 'thumbnail': thumnail})

    return sourcelist


def getepisode(url):
    # url = 'https://www.we-play.tv/watching/series/run-on-2020/season1/ep12'
    # if 'http' in url: url = url.replace(baseurl,'')
    # url = baseurl + url
    # epurl = url[:url.find('product_id=')+11]
    # print epurl
    r = requests.get(url)
    # print r.content
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    li = soup.findAll('div', {'class':"col-3"})[:-2]
    # print li

    # episodes = jseries ['product']
    # print type(episodes)
    eplist = []
    for ep in li:

        surl = ep.find('a').get('href')
        title = ep.find('a').text
        # url = epurl+ep['product_id']
        eplist.append({'title':title , 'url': surl,
                           'thumbnail': ""})
    return eplist
def download_subtitle(url):
    dest = 's.srt'
    # dest = plugintools.get_temp_path() + 's.srt'
    fi = open(dest, "w")
    fi.write(plugintools.read(url))
    fi.close()

def getquality(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': srbaseurl,
               'Origin': baseurl
               }
    response = requests.get(url, headers=headers)
    jdata = json.loads(response.text)
    qualist = jdata['data']['stream']['url']
    # print type(qualist)
    sourcelist = []
    for key in qualist:
        # print key
        # print qualist[key]
        sourcelist.append({"title": key[1:], "url": qualist[key].replace('_var_','_')})

    return sourcelist






def getstreams(url,title=None):
    response = requests.get(url)
    streamurl  = re.compile('playlist:.*\s.*\s.*?file:."([^"]+)').findall(response.text)
    HEADERS = urllib.urlencode({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Referer': 'https://www.we-play.tv',
    })
    get_subtitle(streamurl[0])
    return streamurl[0] + '|%s' % HEADERS
    # return 'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4'

def getnext(url,total):
    offset = url.split('&')
    length = 12
    # offset = 26
    # offset = offset+length
    if 'offset' in  offset[-1]:
        offsetnum = offset[-1].split('=')[-1]
        offsetnum = int(offsetnum)+12

    else:
        offsetnum = 14
    print offsetnum

    if offsetnum <= int(total):
        return offsetnum

def del_sub():
    try:
        os.remove(plugintools.get_temp_path() + 'ws.srt')
    except OSError:
        None

def getsearch(arg):
    url = 'https://www.we-play.tv/search?q='+ arg

    r = requests.get(url=url,headers=headers)
    # result = re.compile('iframe src="([^"]+)"').findall(r.text)
    # print r.content
    #
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    li = soup.findAll('a', {'class': "slide-one slide-two"})
    sourcelist = []
    # print (li)
    for link in li:
        # print link
        surl = link.get('href')
        thumnail = link.find('div').get('style')[22:-2]
        title =  link.find('div', {'class': "slide-content"}).h2.text.replace('\n','')
        # print title,thumnail,surl
        sourcelist.append(
            {"title": title, "url": surl, 'thumbnail': thumnail})

    return sourcelist



def savelast(url,title,thumbnail):
    # path =plugintools.get_runtime_path()
    information = {'url': url, 'title': title, 'thumbnail': thumbnail}
    lasttitle = information['url']
    try:
        with open(tmplastpath, "r") as info_read:
            dict_info = json.load(info_read)
            # plugintools.message('title',str(lasttitle))
            for n in dict_info['list']:
                # print n
                if lasttitle == n['url']:
                    n_status=True
                    break
                else:
                    n_status = False
            # plugintools.message('n_status',str(n_status))
            if n_status is False:
                dict_info['list'].append(information)
            if len(dict_info['list']) > 10:
                dict_info['list'].pop(1)
    except:
        dict_info = {"list": [{'url': url, 'title': title, 'thumbnail': thumbnail}]}
            # plugintools.message('len',str(len(dict_info)))
    with open(tmplastpath, "w") as data:
        data.write(json.dumps(dict_info))
        data.close()

def loadlast():
    seriesList = []
    with open(tmplastpath, "r") as info_read:
        dict_info = json.load(info_read)
        info_read.close()

    for lv in dict_info['list'][::-1]:
        # print p
        seriesList.append({'title': lv['title'], 'url': lv['url'],'thumbnail':lv['thumbnail']})
    return seriesList


def get_subtitle(url):
    dest = plugintools.get_temp_path() + 'ws.srt'
    # dest = 'ss.srt'
    starurl = url[:url.find('playlist')]
    res = requests.get(url)
    # print  res.content
    ############### find sub im m3u8
    sub = re.compile('(subtitle.*?),').findall(res.text)

    if sub :
        sub_url = starurl+sub[0]
        # print sub_url
        res = requests.get(sub_url)
        # print  res.content

        ############## Find all sub url in suburl #########
        allsub = re.compile('(n.*?webvtt.*?)\n').findall(res.text)
        # print allsub

        for i, j in enumerate(allsub):
            s_sul = starurl + j
            # print i
            if i == 0:############ start open write mode
                fi = open(dest, "w+")
                # print sub_url
            else: ##### another open append mode
                fi = open(dest, "a")
            fi.write(read(s_sul))
            fi.close()
    else:
        # print 'No sub'
        fi = open(dest, "w")
        fi.write('')
        fi.close()

def read(url):

    f = urllib2.urlopen(url)
    res = requests.get(url)
    data = f.read()
    f.close()
    # print data
    return data
def read2(url):

    f = requests.get(url)
    data = f.text
    data=data.replace('position:50.00%,middle align:middle size:80.00% line:10.00%','').replace('&lrm;','').replace('<c.thai><c.bg_transparent>','').replace('</c.bg_transparent></c.thai>','')
    f.close()
    print data
    return data.encode('utf8')
def get_subvtt(url):
    dest = 'ss.srt'
    fi = open(dest, "w")
    fi.write(read2(url))
    fi.close()
if __name__ == '__main__':
    pass
    # getseries('https://we-play.tv/movies/family')
    # getgenre()
    # print getcategory('https://we-play.tv/movies')
    # get_subtitle('https://r3-sn-w5nuxa-o536.googlevideocdn.com/series/korea/Find.Me.in.Your.Memory/1.mp4/playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9MS8yNi8yMDIxIDE6NDg6MTIgUE0maGFzaF92YWx1ZT0vM3Iwc3MxQmxUeDR5WXdhOWJtNnZnPT0mdmFsaWRtaW51dGVzPTIw')
    # print getstreams('https://www.we-play.tv/watching/series/reply-1988-2015/season1/ep1')
    # print getsearch("run")
    # getepisode('https://www.we-play.tv/watching/series/run-on-2020/season1/ep12')
    # download_subtitle('https://app.we-play.tv/uploads/subtitles/507_1681_cnqv961574fl.vtt')
    # read2('https://app.we-play.tv/uploads/subtitles/507_1681_cnqv961574fl.vtt')
    # get_subvtt('https://app.we-play.tv/uploads/subtitles/473_1589_e8z3u6at5el7.vtt')
