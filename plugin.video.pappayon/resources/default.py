# -*- coding: utf-8 -*-
import sys,os
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,Mya,my_resolved
from hosts import movie2free, nungsub
from bs4 import BeautifulSoup

def get_main():
    url ='https://www.movie2free.com'
    mainList = Mya.getgenre(url)
    for ctg in mainList:
        plugintools.add_item(title=ctg.get('title'),action='showmovie',url=ctg.get('url'))
    plugintools.add_item(title=u'Slect Hosts', action='showhosts')
    plugintools.close_item_list()


def get_hosts():
    hostlist = Mya.gethosts()
    for host in hostlist:
        plugintools.add_item(title=host.get('title'),action='showgenre',url=host.get('url'))

    plugintools.close_item_list()


def get_genre(url):

    catgList = Mya.getgenre(url)
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showmovie',url=ctg.get('url'))
    plugintools.close_item_list()
    # xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    # xbmc.executebuiltin('Container.SetViewMode(503)')
def get_shows(url):
    showsList = Mya.getmov(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next":
            plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showmovie',url=show.get('url'),thumbnail=thumb)
    plugintools.close_item_list()
    

    

def get_streams(title,thumbnail):
    # arg(title)
    strmList = Mya.get_searchall(title)

    for stream in strmList:
        plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()
    
def stream(url,title,thumbnail):
    resolved_url = select(url)
    if resolved_url is None:
    # if 'upf' in url:
        # resolved_url = upf(url.replace("upfile",'upf'))
    # elif "leoplay" in url:
    #     resolved_url = select(url)
        # resolved_url = Mya.leo(url)
    # else:
        final=urlresolver.HostedMediaFile(url)
        new_url=final.get_url()
        resolved_url=urlresolver.resolve(new_url)

    path=resolved_url
    # path = urlresolver.HostedMediaFile(url).resolve()
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail,path=path)
    li.setInfo(type='Video', infoLabels={ "Title": str(title) })
    xbmc.Player().play(path,li)



def arg(title):
    # strm_url = 'https://drive.google.com/file/d/0Bz2BdKVoSbSwbVBGQUQ2VVMxcDQ/preview'
    # path = str(urlresolver.HostedMediaFile(strm_url).resolve())
    line1 = sys.argv[0]
    line2 = "title="+title
    line3 = "arg[2]="+sys.argv[2]

    xbmcgui.Dialog().ok('test', line1, line2, line3)

def select(url):
    # title = 'test'

    re_url=my_resolved.run(url)
    if re_url is not None:
        menuItems = re_url[0]
        select = xbmcgui.Dialog().select('ความละเอียด',menuItems)

        if select == -1:
            return None
            # break
        else:
            return re_url[1][select]


def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_main()
    elif action == 'showhosts':
        get_hosts()
    elif action == 'showgenre':
        get_genre(params.get('url'))
    elif action == 'showmovie':
        get_shows(params.get('url'))
    # elif action == 'showepisodes':
    #     get_episodes(params.get('url'),params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('title'),params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))
    
run()