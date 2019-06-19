# -*- coding: utf-8 -*-

import plugintools,urllib,xbmc,xbmcgui,add


def get_gerne():
    gerList = add.getgenre()
    for ger in gerList:
        plugintools.add_item(title=ger.get('title'),action='subcate'
                             ,url=ger.get('url'))
    plugintools.add_item(title=u'ค้นหา ', action='showsearch')
    # plugintools.add_item(title=u'Last 10 views  ', action='showlast')
    xbmc.executebuiltin('Container.SetViewMode(502)')
    plugintools.close_item_list()

def get_subcate(url):
    subList = add.getvodlist(url)
    for ger in subList:
        plugintools.add_item(title=ger.get('title'),action=ger.get('action')
                             ,url=ger.get('url'),thumbnail=ger.get('thumbnail'),gtitle=ger.get('title'))
    # plugintools.add_item(title=u'ค้นหา ', action='showsearch')
    # plugintools.add_item(title=u'Last 10 views  ', action='showlast')
    xbmc.executebuiltin('Container.SetViewMode(502)')
    plugintools.close_item_list()


def get_search():
    qry =plugintools.keyboard_input('','ค้นหา')
    showsList = add.getsearch(qry)
    for show in showsList:
        thumb = show.get('thumbnail')
        plugintools.add_item(title=show.get('title'), action=show.get('action'), url=show.get('url'), thumbnail=thumb,gtitle=show.get('title'))
    xbmc.executebuiltin('Container.SetViewMode(502)')
    plugintools.close_item_list()

def get_searchlist(url):

    showsList = add.getsearchlist(url)
    for show in showsList:
        plugintools.add_item(title=show.get('title'),action=show.get('action'),url=show.get('url'),
                             thumbnail=show.get('thumbnail'),gtitle=show.get('title'))
    xbmc.executebuiltin('Container.SetViewMode(502)')
    plugintools.close_item_list()

def get_section(url,title,thumbnail,gtitle):

    showsList = add.get_select(url)
    for show in showsList:
        plugintools.add_item(title=show.get('title'),action=show.get('action'),url=show.get('url'),
                             thumbnail=thumbnail,extra=show.get('extra'),gtitle=gtitle.decode('utf-8'))
    plugintools.close_item_list()


def get_episode(url,title,thumbnail,mmsId,gtitle):
    # xbmcgui.Dialog().ok('strems', gtitle)
    showsList = add.get_ep(url,mmsId)
    for show in showsList:
        title = gtitle.decode('utf-8') +'  ' + show.get('title')
        plugintools.add_item(title=title,action=show.get('action'),url=show.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()


def get_last():
    try:
        showsList = add.loadlast()
        for show in showsList:
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=show.get('thumbnail'))
        plugintools.close_item_list()
    except:
        None

def streamtv(url, title, thumbnail,gtitle):

    # xbmcgui.Dialog().ok('strems', url)
    path = add.getstreams(url)
    # xbmcgui.Dialog().ok('final url', str(path))
    title = gtitle + ' ' + title
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    xbmc.Player().play(path, li)



def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_gerne()
    elif action == 'subcate':
        # xbmcgui.Dialog().ok('action', action)
        get_subcate(params.get('url'))
    elif action == 'section':
        # xbmcgui.Dialog().ok('action', action)
        get_section(params.get('url'), params.get('title'), params.get('thumbnail'),params.get('gtitle'))
    elif action == 'ep':
        get_episode(params.get('url'), params.get('title'), params.get('thumbnail'), params.get('extra'),params.get('gtitle'))
    elif action == 'showsearch':
        get_search()
    elif action == 'searchlist':
        get_searchlist(params.get('url'))

    elif action == 'showlast':
        get_last()
    elif action == 'stream':
        streamtv(params.get('url'), params.get('title'), params.get('thumbnail'),params.get('gtitle'))


run()