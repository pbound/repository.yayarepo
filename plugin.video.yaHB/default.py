# -*- coding: utf-8 -*-
import sys,os
import urlresolver,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,re,requests,Mya,my_resolved
from hosts import movie2free, nungsub
from bs4 import BeautifulSoup
#down.upf.co.il/downloadnew
def upf(url):
    s = requests.Session()
    s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=s.get(url)
    soup = BeautifulSoup(r.text,"html5lib")
    hidden = soup.find("input",{"type":"hidden"}).get("value")
    print url.replace("www.upf.co.il","down.upf.co.il/downloadnew").replace(".html","/")+hidden
    return url.replace("www.upf.co.il","down.upf.co.il/downloadnew").replace(".html","/")+hidden

def get_main():
    hostlist = Mya.getmain()
    for host in hostlist:
        plugintools.add_item(title=host.get('title'),action='showcate',url=host.get('url'))
    plugintools.close_item_list()
def get_main2():
    # hostlist = []
    pt = sys.path[0] + '/hosts'
    allfile = os.listdir(pt)
    if 'nungsub.py' in allfile:
        # hostlist.append(u'Nungsub')
        plugintools.add_item(title=u'Nungsub', action='showcate', url='')
    if '037hd.py' in allfile:
        # hostlist.append(u'037HD')
        plugintools.add_item(title=u'037HD', action='showcate', url='')
    if 'movie2free.py' in allfile:
        # hostlist.append(u'Movie2Free')
        plugintools.add_item(title=u'Movie2Free', action='showcate', url='')
    # for host in hostlist:
    #     plugintools.add_item(title=host,action='showcate',url='')
    plugintools.close_item_list()

def get_categories(url):
    # catgList=[]
    # if 'Movie2Free' in title :
    #     catgList = movie2free.getMenu()
    # if '037HD' in title :
    #     catgList = 037hd.getMenu()
    catgList = Mya.getMenu(url)
    for ctg in catgList:
        plugintools.add_item(title=ctg.get('title'),action='showmovie',url=ctg.get('url'))
    plugintools.close_item_list()
    # xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    # xbmc.executebuiltin('Container.SetViewMode(503)')
def get_shows(url):
    showsList = Mya.getMovies(url)
    for show in showsList:
        thumb = show.get('thumbnail')
        if thumb == None:
            thumb = ""
        if show.get('title')!= u"הבא":
            plugintools.add_item(title=show.get('title'),action='streamslist',url=show.get('url'),thumbnail=thumb)
        else:
            plugintools.add_item(title=show.get('title'),action='showmovie',url=show.get('url'),thumbnail=thumb)
    plugintools.close_item_list()
    
def get_episodes(url,thumbnail):
    try:
        epsList = asian4HB.getEpisodes(url)
    except:
        epsList = []
    if epsList == []:
        epsList = asian4HB.getSpecialEpisodes(url)
    for episode in epsList:
        plugintools.add_item(title=episode.get('title'),action='streamslist',url=url,thumbnail=thumbnail)
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
    elif action == 'showcate':
        get_categories(params.get('url'))
    elif action == 'showmovie':
        get_shows(params.get('url'))
    elif action == 'showepisodes':
        get_episodes(params.get('url'),params.get('thumbnail'))
    elif action == 'streamslist':
        get_streams(params.get('title'),params.get('thumbnail'))
    elif action == 'stream':
        stream(urllib.unquote_plus(params.get('url')),params.get('title'),params.get('thumbnail'))
    
run()