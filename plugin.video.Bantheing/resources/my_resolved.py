# coding=utf-8
import json
import os
import urllib2

import requests,re
import HTMLParser

import sys

import xbmc
import xbmcaddon
import xbmcgui


def get_streamitems(url,lblmatch,stmmatch,referer=None):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Referer': referer}
    r = requests.get(url,headers=headers).text
    r = HTMLParser.HTMLParser().unescape(r)
    labelitem = re.compile(lblmatch).findall(r)
    streamitems = re.compile(stmmatch).findall(r)

    return labelitem,streamitems

def check_host(url):
    if 'leoplayer3' in url:

        if 'movie'in url:
            re_url = get_streamitems(url, '"label"."(.*?)"', '"file.."([^"]+)"')
        elif 'embed' in url:
            re_url = get_streamitems(url, 'label."(.*?)"','file.."([^"]+)"')
        return re_url

    elif 'ddtube.net'in url:
        re_url = get_streamitems(url, 'label.."(.*?)"', '(http.*?m3u8)',referer='https://www.mastermovie-hd.com')
        return re_url
    elif 'iptvz.net'in url:
        re_url = get_streamitems(url, 'label.."(.*?)"', 'file.."([^"]+)"')
        return re_url
    elif 'filebebo.com' in url:
        re_url = get_streamitems(url,'video id="(.*?)"','source.src="([^"]+)"')
        return re_url
    elif 'vidlox.me' in url:
        re_url = get_streamitems(url, '', '(http.*?m3u8)')
        return re_url
    elif  'openload' in url:
        re_url = import_ol(url)
        return re_url
    elif  'okplayer' in url:
        return okru(url)




def run(url):
    re_url = check_host(url)
    # xbmcgui.Dialog().ok('len url1', str(len(re_url[1])))
    if re_url is not None:
        if len(re_url[1]) > 1:
            menuItems = re_url[0]
            select = xbmcgui.Dialog().select('ความละเอียด', menuItems)

            if select == -1:
                return None
                # break
            else:
                return re_url[1][select]
        else:
            return re_url[1][0]



def okru(url):
    url ='https:'+url

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    #### find Frame url ######
    r = requests.get(url, headers=HEADERS).text
    furl = re.compile('<iframe src="([^"]+)"').findall(r)
    furl = 'https:'+furl[0]
    #### Find script json ######

    req = urllib2.Request(furl, headers=HEADERS)
    response = urllib2.urlopen(req)
    shtml = response.read()
    response.close()
    shtml = shtml[shtml.find('data-options=') + 14:shtml.find('" data-player-container')]
    # print shtml
    shtml = shtml.replace('&quot;', '"')
    page = json.loads(shtml)
    page = json.loads(page['flashvars']['metadata'])
    if page:
        url = []
        lbl = []
        for x in page['videos']:
            purl = x['url']
            purl = '%s|User-Agent=%s&Accept=%s' % (purl, HEADERS['User-Agent'], HEADERS['Accept'])
            purl = purl + '&Referer=' + furl + '&Origin=http://ok.ru'
            url.append(purl)
            lbl.append(x['name'].capitalize())

    return lbl,url

