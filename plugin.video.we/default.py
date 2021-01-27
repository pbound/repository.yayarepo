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
        plugintools.add_item(title=ger.get('title'),action='showcate',url=ger.get('url'))
    plugintools.add_item(title=u'ค้นหา ', action='showsearch')
    plugintools.add_item(title=u'Last 10 views  ', action='showlast')
    plugintools.close_item_list()


def get_cate(url):
    cateList = nim.getcategory(url)
    for cate in cateList:
        # plugintools.add_item(title=gid,action='showseries',url=year.get('url'),gid=gid)
        plugintools.add_item(title=cate.get('title'), action='showseries', url=cate.get('url'))
    plugintools.close_item_list()
def get_search():
    qry =plugintools.keyboard_input('','ค้นหา')
    showsList = nim.getsearch(qry)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title') != u"Next":
            plugintools.add_item(title=show.get('title'), action='showepisodes', url=show.get('url'), thumbnail=thumb)
        else:
            # plugintools.add_item(title=show.get('title'), action='showepisodes', url=show.get('url'), thumbnail=thumb)
            plugintools.add_item(title=show.get('title'), action='showmovie', url=show.get('url'), thumbnail=thumb)
    plugintools.close_item_list()

def get_shows(url):
    showsList = nim.getseries(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if 'series' in show.get('url'):
        # if show.get('title') != u"Next":
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='stream',url=show.get('url'),thumbnail=thumb)
    plugintools.close_item_list()

def get_last():
    try:
        showsList = nim.loadlast()
        for show in showsList:
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=show.get('thumbnail'))
        plugintools.close_item_list()
    except:
        None

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


def get_episodes(url,title,thumnail):
    nim.savelast(url,title,thumnail)
    epsList = nim.getepisode(url)
    for show in epsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        plugintools.add_item(title=show.get('title') ,action='stream',url=show.get('url'),thumbnail=thumb)

    plugintools.close_item_list()



def get_streams(url, title, thumbnail):
    strmList = nim.getstreams(url)
    # epid = yaddon.getStreams('epid')
    for stream in strmList:
        stitle = title.decode('utf8') + ' ' + stream.get('title')
        plugintools.add_item(title=stitle, action='stream', url=stream.get('url'),
                             thumbnail=thumbnail)
    plugintools.close_item_list()


def stream(url, title, thumbnail):
    path = nim.getstreams(url)
    # path = url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    li.setSubtitles([plugintools.get_temp_path()+'ws.srt'])
    xbmc.Player().play(path, li)


def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_gerne()
    elif action == 'showsearch':
        get_search()
    elif action == 'showcate':
        get_cate(params.get('url'))
    elif action == 'showseries':
        get_shows(params.get('url'))
    elif action == 'showseriesall':
        get_showsall(params.get('url'))
    elif action == 'showlast':
        get_last()
    elif action == 'showepisodes':
        get_episodes(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'stream':
        stream(params.get('url'),params.get('title'),params.get('thumbnail'))

run()