# -*- coding: utf-8 -*-
import os
import sys
import urllib2

import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,nim
from bs4 import BeautifulSoup
#down.upf.co.il/downloadnew



def get_gerne():
    gerList = nim.getgenre()
    for ger in gerList:
        plugintools.add_item(title=ger.get('title'),action='showseries',url=ger.get('url'))
    # plugintools.add_item(title=u'ค้นหา ', action='showsearch')
    plugintools.close_item_list()


def get_year(url):
    yearList = yaddon.getyear(url)
    for year in yearList:
        # plugintools.add_item(title=gid,action='showseries',url=year.get('url'),gid=gid)
        plugintools.add_item(title=year.get('title'), action='showseries', url=year.get('url'), yid=year.get('yid'))
    plugintools.close_item_list()
def get_search():
    # slist = site2list()
    # menuItems = slist[1]
    # selecturl = xbmcgui.Dialog().select('Select Sites', menuItems)
    qry =plugintools.keyboard_input('','ค้นหา')

    # qry = get_keyboard('ค้นหา',default='')
    # xbmcgui.Dialog().ok('test', str(slist[0][selecturl]))
    # siteslist =  getsiteslist()


    # if select == -1:
    #     return None
    #     break
    # else:
    #     return menuItems[select]
    # strmList = importsite(url, 'getstreams')

    # surl = slist[0][selecturl]
    showsList = nim.getsearch(qry)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title') != u"Next":
            plugintools.add_item(title=show.get('title'), action='showepisodes', url=show.get('url'), thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'), action='showmovie', url=show.get('url'), thumbnail=thumb)
    plugintools.close_item_list()

def get_shows(url):
    showsList = nim.getseries(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next" :
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showseries',url=urllib.unquote(url).decode('utf8'),thumbnail=thumb)
    plugintools.close_item_list()


def get_showsall(url):
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
    epsList = nim.getepisode(url)
    for show in epsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)

    plugintools.close_item_list()



def get_streams(url, title, thumbnail):
    strmList = nim.getstreams(url)
    # epid = yaddon.getStreams('epid')
    for stream in strmList:
        stitle = title.decode('utf8') + ' ' + stream.get('title')
        plugintools.add_item(title=stitle, action='stream', url=stream.get('url'),
                             thumbnail=urllib.unquote(thumbnail).decode('utf8'))
    plugintools.close_item_list()


def stream(url, title, thumbnail):
    path = url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    li.setSubtitles([sys.path[0] + '/resources/temp/s.srt'])
    xbmc.Player().play(path, li)


def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_gerne()
    elif action == 'showsearch':
        get_search()
    elif action == 'showyear':
        get_year(params.get('url'))
    elif action == 'showseries':
        get_shows(params.get('url'))
    elif action == 'showseriesall':
        get_showsall(params.get('url'))
    elif action == 'showepisodes':
        get_episodes(params.get('url'))
    elif action == 'streamslist':
        get_streams(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))

run()