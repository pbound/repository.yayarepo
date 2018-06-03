# -*- coding: utf-8 -*-
import os
import sys
import urllib

import re
import xbmc
import xbmcaddon
import xbmcgui

import my_resolved
import plugintools
import urlresolver
from resources.sites._utility import importsite, y_sites,getsiteslist, site2list

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonpath= addon.getAddonInfo('path')
nextimg = addonpath + r'\lib\img\next.jpg'
# print addon.


def get_main():
    from resources.sites import movie2free
    mainlist = movie2free.getgenre()

    for ctg in mainlist:
        plugintools.add_item(title=ctg.get('title'),action='showsearchmovie',url=ctg.get('url'))
    plugintools.add_item(title=u'ซีรีส์เกาหลี', action='showseries', url='http://www.kseries.co/category/korea-series/')
    plugintools.add_item(title=u'ดูเว็บ ซีรีส์', action='showwebseries')
    plugintools.add_item(title=u'Slect Hosts', action='showhosts')
    plugintools.add_item(title=u'ค้นหา หนัง', action='showsearch')
    plugintools.close_item_list()


def get_sites():

    slist = getsiteslist()
    for site in slist:
        genre = site.get('genre')
        if genre == 'series':
            plugintools.add_item(title=site.get('title'), action='showseriesgenre', url=site.get('url'))
        else:
            plugintools.add_item(title=site.get('title'),action='showgenre',url=site.get('url'))

    plugintools.close_item_list()

def get_siteseries():

    slist = getsiteslist()
    for site in slist:
        genre = site.get('genre')
        if genre == 'series':
            plugintools.add_item(title=site.get('title'), action='showseriesgenre', url=site.get('url'))

    plugintools.close_item_list()

def get_genre(url):


    catgList = importsite(url,'getgenre')
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showmovie',url=ctg.get('url'))
    plugintools.close_item_list()
    # xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    # xbmc.executebuiltin('Container.SetViewMode(503)')
def get_seriesgenre(url):


    catgList = importsite(url,'getgenre')
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showseries',url=ctg.get('url'))
    plugintools.close_item_list()
def get_movsearch(url):
    movsList = importsite(url,'getmov')
    for show in movsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next":
            plugintools.add_item(title=show.get('title'),action='searchstreamslist',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showsearchmovie',url=show.get('url'),thumbnail=nextimg)
    plugintools.close_item_list()

def get_mov(url):
    # xbmcgui.Dialog().ok('url',url)
    movsList = importsite(url,'getmov')
    for show in movsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"Next":
            plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showmovie',url=show.get('url'),thumbnail=nextimg)
    plugintools.close_item_list()


def get_series(url):
    # xbmcgui.Dialog().ok('url',url)
    movsList = importsite(url, youget='getseries')
    for show in movsList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title') != u"Next":
            plugintools.add_item(title=show.get('title'), action='showepisode', url=show.get('url'), thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'), action='showseries', url=show.get('url'), thumbnail=nextimg)
    plugintools.close_item_list()

def get_episode(url):
    # xbmcgui.Dialog().ok('url',url)
    epList = importsite(url,youget='getepisode')
    for show in epList:
        # print show
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)

    plugintools.close_item_list()



def get_searchstreams(title,thumbnail):
    dialog = xbmcgui.DialogProgress()
    dialog.create('ค้นหา', ("Loading items"))

    ntitle = title[0:title.find('(')-1].replace(' ', '+')
    ntitle = re.sub('[^a-zA-Z0-9 +]','',ntitle)#.encode('utf8','ignore')
    # xbmcgui.Dialog().ok('test', str(type(ntitle)),ntitle)
    # arg(title)
    # strmList = Mya.get_searchall(title)
    # ntitle = title[0:title.find(')') + 1].replace(' ', '+')
    # ntitle = title[0:title.find('(')].replace(' ', '+')
    # ntitle = title
    siteslist = getsiteslist()
    num_urls = len(siteslist)

    for index,site in enumerate (siteslist,1):
        if dialog.iscanceled():
            break
        percent = ((index + 1) * 100) / num_urls
        dialog.update(percent, ("processing lists"), ("%s") % (
            site.get('title')))

        url = site.get('url')

        webgenre = site.get('genre') # check series web
        if webgenre !='series':
            strmList = importsite(url, 'getsearchall', title=ntitle)
        else:
            strmList = None

        # xbmcgui.Dialog().ok('searchall',str(strmList))
        if strmList != None:
            for stream in strmList:
                plugintools.add_item(title=stream.get('title'),action='stream',url=stream.get('url'),thumbnail=thumbnail)
    plugintools.close_item_list()



def get_streams(url,thumbnail,title):
    # xbmcgui.Dialog().ok('get_stream', title)
    # arg(title)
    strmList = importsite(url,'getstreams',title=title)

    for stream in strmList:
        stitle = title.decode('utf8')+' '+stream.get('title')
        plugintools.add_item(title=stitle, action='stream',url=stream.get('url'),thumbnail=urllib.unquote(thumbnail).decode('utf8'))
    plugintools.close_item_list()
    
def stream(url,title,thumbnail):
    # xbmcgui.Dialog().ok('strems', url)
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
    # xbmcgui.Dialog().ok('final url',str(resolved_url))
    if resolved_url == False:
        resolved_url = url
    path=resolved_url
    # xbmcgui.Dialog().ok('final url', str(path))
    # path = urlresolver.HostedMediaFile(url).resolve()
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail,path=path)
    li.setInfo(type='Video', infoLabels={ "Title": str(title) })
    xbmc.Player().play(path,li)

    # listitem = xbmcgui.ListItem("My Jam TV")
    # listitem.setInfo('video', {'Title': 'My Jam TV', 'Genre': 'Music Video'})
    # xbmc.Player().play(path, listitem)



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

def get_keyboard(heading, default=''):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(heading)
    if default: keyboard.setDefault(default)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()

    else:
        return None


def get_search():
    slist = site2list()
    menuItems = slist[1]
    selecturl = xbmcgui.Dialog().select('Select Sites', menuItems)

    qry = get_keyboard('ค้นหา',default='')
    # xbmcgui.Dialog().ok('test', str(slist[0][selecturl]))
    # siteslist =  getsiteslist()


    # if select == -1:
    #     return None
    #     break
    # else:
    #     return menuItems[select]
    # strmList = importsite(url, 'getstreams')

    surl = slist[0][selecturl]
    showsList = importsite(surl,'getsearch',title=qry)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title') != u"Next":
            plugintools.add_item(title=show.get('title'), action='streamslist', url=show.get('url'), thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'), action='showmovie', url=show.get('url'), thumbnail=thumb)
    plugintools.close_item_list()


def get_test():
    slist = site2list()
    menuItems = slist[1]
    # typ = slist
    # xbmcgui.Dialog().ok('test',str(typ))
    select = xbmcgui.Dialog().select('ความละเอียด', menuItems)

    # if select == -1:
    #     return None
        # break
    # else:
    #     return slist[1][select]
    # for s in slist:
    hurl = ''
    hnames = slist[0][select]
    plugintools.add_item(title=hnames, action='streamslist', url=hurl)

    plugintools.close_item_list()
def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_main()
        # get_test()
    elif action == 'showhosts':
        get_sites()
    elif action == 'showwebseries':
        get_siteseries()
    elif action == 'showgenre':
        get_genre(params.get('url'))
    elif action == 'showseriesgenre':
        get_seriesgenre(params.get('url'))
    elif action == 'showsearchmovie':
        get_movsearch(params.get('url'))
    elif action == 'showmovie':
        get_mov(params.get('url'))
    elif action == 'showseries':
        get_series(params.get('url'))
    elif action == 'showepisode':
        get_episode(params.get('url'))
    elif action == 'showsearch':
        get_search()
    elif action == 'streamslist':
        get_streams(params.get('url'),params.get('thumbnail'),params.get('title'))
    elif action == 'searchstreamslist':
        get_searchstreams(params.get('title'),params.get('thumbnail'))
    elif action == 'stream':
        # stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))
        stream(params.get('url'), params.get('title'), params.get('thumbnail'))
    
run()
# if __name__ == '__main__':
# print get_sites()
    # get_main()
    # get_shows('https://www.movie2free.com/top-imdb/')
    # get_searchstreams('who am i','ddd')
