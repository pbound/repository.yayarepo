# -*- coding: utf-8 -*-

import plugintools,urllib,xbmc,xbmcgui,vte


def get_gerne():
    gerList = vte.getgenre()
    for ger in gerList:
        plugintools.add_item(title=ger.get('title'),action='showseries',url=ger.get('url'))
    plugintools.add_item(title=u'ค้นหา ', action='showsearch')
    plugintools.add_item(title=u'Last views ', action='showlast')
    xbmc.executebuiltin('Container.SetViewMode(501)')
    plugintools.close_item_list()


def get_search():
    qry =plugintools.keyboard_input('','ค้นหา')
    showsList = vte.getsearch(qry)
    for show in showsList:
        thumb = show.get('thumbnail')
        plugintools.add_item(title=show.get('title'), action='showepisodes', url=show.get('url'), thumbnail=thumb)
    plugintools.close_item_list()

def get_shows(url):
    showsList = vte.getseries(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next" :
            plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showseries',url=show.get('url'),thumbnail=thumb)
    xbmc.executebuiltin('Container.SetViewMode(500)')
    plugintools.close_item_list()


def get_last():
    showsList = vte.loadlast()
    for show in showsList:
        plugintools.add_item(title=show.get('title'),action='showepisodes',url=show.get('url'),thumbnail=show.get('thumbnail'))
    plugintools.close_item_list()

def get_episodes(url,title,thumnail):
    vte.savelast(url,title,thumnail)
    epsList = vte.getepisode(url)
    for show in epsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)

    plugintools.close_item_list()



def get_streams(url, title, thumbnail):
    strmList = vte.getstreams(url)
    for stream in strmList:
        stitle = title.decode('utf8') + ' ' + stream.get('title')
        plugintools.add_item(title=stitle, action='stream', url=stream.get('url'),
                             thumbnail=urllib.unquote(thumbnail).decode('utf8'))
    plugintools.close_item_list()


def stream(url, title, thumbnail):
    path = url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    li.setSubtitles([plugintools.get_temp_path()+'s.srt'])

    xbmc.Player().play(path, li)


def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        # test()
        get_gerne()
    elif action == 'showsearch':
        get_search()

    elif action == 'showseries':
        get_shows(params.get('url'))
    elif action == 'showlast':
        get_last()
    elif action == 'showepisodes':
        get_episodes(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))

run()