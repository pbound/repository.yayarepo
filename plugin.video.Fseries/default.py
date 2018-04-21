# -*- coding: utf-8 -*-
import sys
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,Fseries

# import web_pdb; web_pdb.set_trace()
#down.upf.co.il/downloadnew
path = sys.path[0]+'/'
def get_categories():
    catgList = Fseries.getMenu()
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showseries',url=ctg.get('url'),thumbnail=path+'icon.png')
    plugintools.close_item_list()
    
def get_shows(url):
    showsList = Fseries.getSeries(url)
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
        epsList = Fseries.getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = Fseries.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'),action='stream',url=episode.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()


def get_episodes_new(url, thumbnail):
    try:
        epsList = Fseries.k_getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = Fseries.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'), action='streams', url=episode.get('url'),
                             thumbnail=thumbnail)
    plugintools.close_item_list()


def get_streams(url,title,thumbnail):
    strmList = Fseries.getStreams(url)

    for stream in strmList:
        plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()
    
def stream(url,title,thumbnail):
    # if 'upf' in url:
    #     resolved_url = upf(url.replace("upfile",'upf'))
    # elif "yadi" in url:
    #     resolved_url = Fseries.yandex(url)
    # elif "mp4" in url:
    #     resolved_url = Fseries.k_stream(url)
    # else:
    #     final=urlresolver.HostedMediaFile(url)
    #     new_url=final.get_url()
    #     resolved_url=urlresolver.resolve(new_url)
    # path=resolved_url
    strm_url = Fseries.F_stream(url)
    # strm_url = 'https://drive.google.com/file/d/0Bz2BdKVoSbSwbVBGQUQ2VVMxcDQ/preview'
    path = urlresolver.HostedMediaFile(strm_url).resolve()

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