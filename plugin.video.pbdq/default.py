# -*- coding: utf-8 -*-
import os
import sys
import urllib2

import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,yaddon
from bs4 import BeautifulSoup
#down.upf.co.il/downloadnew
def upf(url):
    s = requests.Session()
    s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=s.get(url)
    soup = BeautifulSoup(r.text,"html5lib")
    hidden = soup.find("input",{"type":"hidden"}).get("value")
    print url.replace("www.upf.co.il","down.upf.co.il/downloadnew").replace(".html","/")+hidden
    return url.replace("www.upf.co.il","down.upf.co.il/downloadnew").replace(".html","/")+hidden


def get_categories():
    catgList = yaddon.getMenu()
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showyear',url=ctg.get('url'))
    plugintools.close_item_list()

def get_gerne(url):
    gerList = yaddon.getgerne(url)
    for ger in gerList:
        plugintools.add_item(title=ger.get('title'),action='showyear',url=ger.get('url'),gid=ger.get('gid'))
    plugintools.close_item_list()


def get_year(url):
    yearList = yaddon.getyear(url)
    for year in yearList:
        # plugintools.add_item(title=gid,action='showseries',url=year.get('url'),gid=gid)
        plugintools.add_item(title=year.get('title'), action='showseries', url=year.get('url'), yid=year.get('yid'))
    plugintools.close_item_list()

    
def get_shows(url,yid):
    showsList = yaddon.getSeries(url,yid)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"โหลดทังหมด" :
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showseriesall',url=urllib.unquote(url).decode('utf8'),thumbnail=thumb,yid=yid)
    plugintools.close_item_list()


def get_showsall(url, yid):
    showsList = yaddon.getSeriesAll(url, yid)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        # if show.get('title') != u"โหลดทังหมด":
        plugintools.add_item(title=show.get('title'), action='showepisodes', url=show.get('url'), thumbnail=thumb)
        # else:
        #     plugintools.add_item(title=show.get('title'), action='showall', url=show.get('url'), thumbnail=thumb)
    plugintools.close_item_list()


def get_episodes(url):
    epsList = yaddon.getEpisodes(url)
    # epid = yaddon.getEpisodes('epid')
    for episode in epsList:
        epid = episode.get('epid')
        thumb = episode.get('thumbnail')
        plugintools.add_item(title=episode.get('title'),action='streamslist',url=episode.get('url'),thumbnail=thumb,epid=epid)
    plugintools.close_item_list()

    

def get_streams(url,epid):
    strmList = yaddon.getStreams(url,epid)
    # epid = yaddon.getStreams('epid')

    for stream in strmList:
        sub = stream.get('epid')
        plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),epid=sub)
        # plugintools.add_item(title=sub, action='stream', url=stream.get('url'), epid=sub)
    plugintools.close_item_list()
    # Download_subtitle(sys.path[0] + '/resources/temp', 'nameteat', sub)

def Download_subtitle(subs, videoTitle, url):
    if not os.path.exists(subs):
        os.makedirs(subs)
    filename = str(videoTitle) + '.srt'
    filepath = xbmc.translatePath(os.path.join(subs, filename))

    def download(url, dest):
        pip = '127.0.0.1:3128'
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        sock = urllib2.urlopen(req)

        fi = open(dest, "w")
        fi.write(sock.read())
        fi.close()
        # proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:3128'})
        # construct a new opener using your proxy settings
        # opener = urllib.request.build_opener(proxy)
        # install the openen on the module-level
        # urllib.request.install_opener(opener)
        ##                    dialog = xbmcgui.DialogProgress()
        ##                    dialog.create('Downloading Movie','From Source', filename)
        # urllib.urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, ''))

    def _pbhook(numblocks, blocksize, filesize, url=None, dialog=None):
        try:

            percent = min((numblocks * blocksize * 100) / filesize, 100)
        ##                        dialog.update(percent)
        except:
            percent = 100
            ##                        dialog.update(percent)
            ##                    if dialog.iscanceled():
            ##                                    dialog.close()

    download(url, filepath)
    iscanceled = True
    xbmc.executebuiltin('Notification("Subtitle","Downloaded")')
    return filepath


def stream(url, title, thumbnail,epid):
    # if 'upf' in url:
    #     resolved_url = upf(url.replace("upfile",'upf'))
    # elif "yadi" in url:
    #     resolved_url = asian4HB.yandex(url)
    # else:
    #     final=urlresolver.HostedMediaFile(url)
    #     new_url=final.get_url()
    #     resolved_url=urlresolver.resolve(new_url)
    # path=resolved_url
    path = url
    # subtitle_url =  str(epid).replace("u'",'')
    # subtitle_url = 'https://www.grabvdo.com/subtitle?viu=eyJpdiI6IlBSWUV4M2tIODdjelwvK09GNWFlcWNBPT0iLCJ2YWx1ZSI6Ino3bENuVXVkQ0M1OUNwdDJHZnBQUm9ZZEd1b3BrVXNaVk1SMldacFlhM3lEZDcyMyszM0VVMmViTlwvTVQySUFXemlUdWV1eEJwRjVaa3daR1JiVDRLWjVRWjRib0V0SVE0a0xmVTZiMUdKRm1JejBkbTU1QzJVREJkMVNDdXlMTTB6S05RTTFOa2trUk02Z3hveStWbGc9PSIsIm1hYyI6ImFlNzJlMTIzMGQxNDc5YmQzMjUxYWY3OGFmYmQwMzc5YmFiNzgxY2U4YmJlZjNhZjlmZTg3MzhiYWU0YjljZTEifQ=='
    # subtitle = Download_subtitle(sys.path[0] + '/resources/temp', 'nameteat', subtitle_url )
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    li.setSubtitles([sys.path[0] + '/resources/temp/s.srt'])
    xbmc.Player().play(path, li)


def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_categories()
    elif action == 'showgerne':
        get_gerne(params.get('url'))
    elif action == 'showyear':
        get_year(params.get('url'))
    elif action == 'showseries':
        get_shows(params.get('url'),params.get('yid'))
    elif action == 'showseriesall':
        get_showsall(params.get('url'),params.get('yid'))
    elif action == 'showepisodes':
        get_episodes(params.get('url'))
    elif action == 'streamslist':
        get_streams(params.get('url'),params.get('epid'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'),params.get('epid'))
    
run()