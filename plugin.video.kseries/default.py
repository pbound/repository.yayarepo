# -*- coding: utf-8 -*-
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,kaddon
from bs4 import BeautifulSoup

# import web_pdb; web_pdb.set_trace()
#down.upf.co.il/downloadnew


def get_categories():
    catgList = kaddon.getMenu()
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showseries',url=ctg.get('url'))
    plugintools.add_item(title=u'ค้นหา ซีรีส์เกาหลี', action='showsearch', url='http://www.kseries.co/?s=')
    plugintools.close_item_list()

def get_search(url):
    qry = get_keyboard('ค้นหา',default='')
    surl = url + qry
    # xbmcgui.Dialog().ok('test',surl)
    showsList = kaddon.getSeries(surl)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next":
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showseries',url=show.get('url'),thumbnail=thumb)
    plugintools.close_item_list()

def get_shows(url):
    showsList = kaddon.getSeries(url)
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
        epsList = kaddon.getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = kaddon.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'),action='streamslist',url=episode.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()


def get_streams(url,title,thumbnail):
    strmList = kaddon.exactkSeries(url)
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

def get_keyboard(heading, default=''):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(heading)
    if default: keyboard.setDefault(default)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()

    else:
        return None

def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_categories()
    elif action == 'showseries':
        get_shows(params.get('url'))
    elif action == 'showsearch':
        get_search(params.get('url'))
    elif action == 'showepisodes':
        get_episodes(params.get('url'),params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('url'),params.get('title'),params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))
    
run()
# print get_categories()