# -*- coding: utf-8 -*-
import os
import sys
import urllib
import re
import xbmc
import xbmcaddon
import xbmcgui
import plugintools
import urlresolver
from resources import my_resolved
from resources.sites._utility import importsite, y_sites,getsiteslist, site2list,loadlast,savelast,checktv

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonpath= addon.getAddonInfo('path')
nextimg = addonpath + r'\lib\img\next.jpg'
# print addon.


def get_main():
    plugintools.add_item(title=u'TV', action='showTV', url='http://psitv.tv/api/Channels',thumbnail='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKEnivgmG2z2cUlO0Rcw4GBz-UqfXJ11pTV7ssBh51lqSSYGHmNw')
    plugintools.add_item(title=u'Series&Movies', action='showhosts',thumbnail='http://mynotl.com/sites/welland/files/field/image/film-series-logo.jpg')
    plugintools.add_item(title=u'ค้นหา หนัง', action='showsearch',thumbnail='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjo0TdD4Mgh3hBgKces3bv6e1WqbeH6msGWXj_9vGKwICjBy6Yfw')
    xbmc.executebuiltin('Container.SetViewMode(502)')
    plugintools.close_item_list()


def get_sites():

    slist = getsiteslist()
    for site in slist:
        genre = site.get('genre')
        if genre == 'series':
            plugintools.add_item(title=site.get('title'), action='showseriesgenre', url=site.get('url'),
                                 thumbnail=site.get('thumbnail'))
        else:
            plugintools.add_item(title=site.get('title'), action='showgenre', url=site.get('url'),
                                 thumbnail=site.get('thumbnail'))
    plugintools.add_item(title=u'Last 10 views ', action='showlast')
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
    # xbmc.executebuiltin('Container.SetViewMode(500)')
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

def get_episode(url,title,thumnail):
    savelast(url, title, thumnail, action='showepisode')
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
    savelast(url=url, title=title, thumbnail=thumbnail,action = 'streamslist')
    # xbmcgui.Dialog().ok('get_stream', title)
    # arg(title)
    strmList = importsite(url,'getstreams',title=title)

    for stream in strmList:
        stitle = title.decode('utf8') + ' ' + stream.get('title')
        if 'sources' in stream.get('url'):
            plugintools.add_item(title=stitle, action='qualitylist', url=stream.get('url'),
                                 thumbnail=urllib.unquote(thumbnail).decode('utf8'))
        else:
            plugintools.add_item(title=stitle, action='stream',url=stream.get('url'),thumbnail=urllib.unquote(thumbnail).decode('utf8'))
    plugintools.close_item_list()


def get_tv():
    plugintools.add_item(title=u'TV1', action='showchannel',thumbnail='https://i3.wp.com/psisat.com/site/wp-content/uploads/2018/09/logo-psi2018.png')
    plugintools.add_item(title=u'TV2', action='showchannel', thumbnail='https://www.mvtv.co.th/wp-content/uploads/2019/01/mvtv-official-logo.png')
    plugintools.add_item(title=u'TV3', action='showchannel', thumbnail='https://image.makewebeasy.net/makeweb/0/HSqZMq6g7/DefaultData/Untitled_1_1.png')
    plugintools.add_item(title=u'TV4', action='showchannel',
                         thumbnail='https://lh3.googleusercontent.com/TtiB9niJIaQwqn4n7RWXdoprigigN-K_Mm8rnE_F57BdknYufywwKDzeMcoaZKSbRaw=s180-rw')
    plugintools.add_item(title=u'TV5', action='showchannel',
                         thumbnail='https://lh3.googleusercontent.com/ZitE6e8xo2ptVNJRX8M0MEyDr5btN4yARlPy3VDntZGk48PIVLvdqafKMZ0p98huuA=s180')
    plugintools.add_item(title=u'TV6', action='showchannel',
                         thumbnail='https://scontent.fbkk5-4.fna.fbcdn.net/v/t1.0-9/29104254_1854937651196677_3353442213391499264_n.jpg?_nc_cat=110&_nc_ht=scontent.fbkk5-4.fna&oh=92f437fe2c8d9f5fd1b6bff77bd9507b&oe=5D5452AF')
    plugintools.add_item(title=u'TV7', action='showchannel',
                         thumbnail='https://i0.wp.com/www.we-play.tv/wp-content/uploads/2018/11/logo.png')
    plugintools.add_item(title=u'TV8', action='showchannel',
                         thumbnail='https://scontent.fbkk22-2.fna.fbcdn.net/v/t1.0-1/15780666_1039555132820647_7174041289293035783_n.png?_nc_cat=105&_nc_ht=scontent.fbkk22-2.fna&oh=c0f70260f8927451d4d86c7490ec0540&oe=5D931C5F')
    xbmc.executebuiltin('Container.SetViewMode(500)')
    plugintools.close_item_list()

def get_channel(title):
    try:
        # xbmcgui.Dialog().ok('get_stream', 'title')
        # arg(title)
        if title == 'TV1':
            from resources.sites import _fixit
            strmList = _fixit.getstreams()
        elif title == 'TV2':
            from resources.sites import _mvtv
            strmList =  _mvtv.get_chlist()
        elif title == 'TV3':
            from resources.sites import _loox
            strmList = _loox.get_chlist()
        elif title == 'TV4':
            checktv('_2idtv')
            from resources.sites import _2idtv
            strmList = _2idtv.get_chlist()
        elif title == 'TV5':
            checktv('_12tv')
            from resources.sites import _12tv
            strmList = _12tv.get_chlist()
        elif title == 'TV6':
            from resources.sites import _mclubtv
            strmList = _mclubtv.get_chlist()
        elif title == 'TV7':
            from resources.sites import _weplaytv
            strmList = _weplaytv.get_chlist()
        elif title == 'TV8':
            from resources.sites import _dstv
            strmList = _dstv.get_chlist()

        for stream in strmList:
            url = stream.get('url')
            thumb = stream.get('thumbnail')
            if thumb == None:
                thumb = ""
            if url  == None :
                url = ''
            stitle = stream.get('title')

            # stitle = stitle.decode('utf8')
            # plugintools.add_item(title=u'stitle', action='stream',url=stream.get('url'),thumbnail=stream.get('thumbnail'))
            plugintools.add_item(title=stitle, action='streamtv',url=url,thumbnail=thumb)
        xbmc.executebuiltin('Container.SetViewMode(500)')
        plugintools.close_item_list()
    except OSError:
        None

def get_quality(url,thumbnail,title):
    # savelast(url=url, title=title, thumbnail=thumbnail,action = 'streamslist')
    from resources.sites.movie2free import getquality
    strmList = getquality(url,title=title)

    for stream in strmList:
        stitle = title.decode('utf8') + ' ' + stream.get('title')
        # plugintools.message('title', stitle)
        plugintools.add_item(title=stitle, action='stream',url=stream.get('url'),thumbnail=urllib.unquote(thumbnail).decode('utf8'))
    plugintools.close_item_list()

def stream(url,title,thumbnail):
    resolved_url = my_resolved.run(url)
    if resolved_url is None:
        final=urlresolver.HostedMediaFile(url)

        new_url=final.get_url()
        resolved_url=urlresolver.resolve(new_url)
    if resolved_url == False:
        resolved_url = url
    path=resolved_url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail,path=path)
    li.setInfo(type='Video', infoLabels={ "Title": str(title) })
    xbmc.Player().play(path,li)

def streamtv(url,title,thumbnail):
    # xbmcgui.Dialog().ok('strems', url)
    if 'tv.true' in url:
        from resources.sites._2vison import getsubstream
        furl = getsubstream(url)
    # elif 'co.th' in url:
    #     furl = url
    elif './live?' in url:
        from resources.sites._mclubtv import getm3u
        furl = getm3u(url)
    elif 'we-play' in url:
        from resources.sites._weplaytv import getm3u
        furl = getm3u(url)
    elif '17:1935' in url:
        from resources.sites._dstv import getm3u
        furl = getm3u(url)
    elif 'dmpapi2' in url:
        from resources.sites._2idtv import getsubstream

        if getsubstream(url)[1]:  ##### Check mpd file streaming
            smurl = getsubstream(url)[0]
            lc_url = getsubstream(url)[1]
            plaympd(smurl, lc_url, title, thumbnail)
            exit()
        else:
            furl = getsubstream(url)[0]
            
    elif  url.isdigit():
        from resources.sites._fixit import getchadetail
        furl =getchadetail(url)
    elif not url.startswith('http'):
        from resources.sites._12tv import getm3u
        furl = getm3u(url)
    else:

        # furl = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;url=' + url
        furl = url
    path = furl
    # xbmcgui.Dialog().ok('final url', str(path))
    # path = urlresolver.HostedMediaFile(url).resolve()
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    li.setInfo(type='Video', infoLabels={"Title": str(title)})
    xbmc.Player().play(path, li)


def plaympd(path, lc_url, title, thumbnail):
    play_item = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=path)
    play_item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
    play_item.setProperty('inputstream.adaptive.license_key', lc_url + '||R{SSM}|')
    play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
    play_item.setMimeType('application/dash+xml')
    play_item.setContentLookup(False)
    xbmc.Player().play(path, play_item)
    #


def arg(title):
    line1 = sys.argv[0]
    line2 = "title="+title
    line3 = "arg[2]="+sys.argv[2]

    xbmcgui.Dialog().ok('test', line1, line2, line3)


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

def get_last():
    try:
        showsList = loadlast()
        for show in showsList:
            plugintools.add_item(title=show.get('title'),action=show.get('action'),url=show.get('url'),thumbnail=show.get('thumbnail'))
        plugintools.close_item_list()
    except:
        None


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
        get_episode(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'showsearch':
        get_search()
    elif action == 'showlast':
        get_last()
    elif action == 'streamslist':
        get_streams(params.get('url'),params.get('thumbnail'),params.get('title'))
    elif action == 'searchstreamslist':
        get_searchstreams(params.get('title'),params.get('thumbnail'))
    elif action == 'qualitylist':
        get_quality(params.get('url'),params.get('thumbnail'),params.get('title'))
    elif action == 'showTV':
        get_tv()
    elif action == 'showchannel':
        get_channel(params.get('title'))
    elif action == 'stream':
        stream(params.get('url'), params.get('title'), params.get('thumbnail'))
    elif action == 'streamtv':
        streamtv(params.get('url'), params.get('title'), params.get('thumbnail'))

run()
