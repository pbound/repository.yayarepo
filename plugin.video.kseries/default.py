# -*- coding: utf-8 -*-
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,asian4HB
from bs4 import BeautifulSoup

# import web_pdb; web_pdb.set_trace()
#down.upf.co.il/downloadnew


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


def get_streams(url,title,thumbnail):
    strmList = asian4HB.exactkSeries(url)

    for stream in strmList:
        plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()

def stream(url,title,thumbnail):
    if 'google' in url:
        path = urlresolver.HostedMediaFile(url).resolve()
    elif 'ok.ru' in url:
        path = urlresolver.HostedMediaFile(url).resolve()
    else:
        path = url
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
