# -*- coding: utf-8 -*-
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,asian4HB
from bs4 import BeautifulSoup

# import web_pdb; web_pdb.set_trace()
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
    catgList = asian4HB.getMenu()
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showseries',url=ctg.get('url'))
    plugintools.close_item_list()
    
def get_shows(url):
    showsList = asian4HB.getSeries(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next":
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showseries',url=show.get('url'),thumbnail=thumb)
    plugintools.close_item_list()
    
def get_episodes(url,thumbnail):
    try:
        epsList = asian4HB.getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = asian4HB.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'),action='streamslist',url=episode.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()


def get_episodes_new(url, thumbnail):
    try:
        epsList = asian4HB.k_getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = asian4HB.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'), action='streamslist', url=episode.get('url'),
                             thumbnail=thumbnail)
    plugintools.close_item_list()


def get_streams(url,title,thumbnail):
    strmList = asian4HB.getStreams(url)

    for stream in strmList:
        plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()
    
def stream(url,title,thumbnail):
    # if 'upf' in url:
    #     resolved_url = upf(url.replace("upfile",'upf'))
    # elif "yadi" in url:
    #     resolved_url = asian4HB.yandex(url)
    # elif "mp4" in url:
    #     resolved_url = asian4HB.k_stream(url)
    # else:
    #     final=urlresolver.HostedMediaFile(url)
    #     new_url=final.get_url()
    #     resolved_url=urlresolver.resolve(new_url)
    # path=resolved_url
    path = asian4HB.k_stream(url)
    # path = url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail,path=path)
    li.setInfo(type='Video', infoLabels={ "Title": str(title) })
    xbmc.Player().play(path,li)
    
def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_categories()
    elif action == 'showseries':
        get_shows(params.get('url'))
    elif action == 'showepisodes':
        get_episodes(params.get('url'),params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('url'),params.get('title'),params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))
    
run()
# print get_categories()