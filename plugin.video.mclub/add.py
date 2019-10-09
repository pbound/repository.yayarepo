# -*- coding: utf-8 -*-
import json,plugintools
import re
import urllib
import requests

from base64 import b64decode

from bs4 import BeautifulSoup

tmplastpath = plugintools.get_temp_path()+"\info_.json"
baseurl = b64decode('aHR0cHM6Ly93d3cubW92aWVjbHViaGQudHYvdGgv')#mcu
shbaseurl = b64decode('aHR0cHM6Ly9hcHAubW92aWVjbHViLnR2L2FwaS9zZWFyY2gvaW5kZXg/dGVybT0=')

fbaseurl = b64decode('aHR0cHM6Ly9kZnA2cmdsZ2pxc3prLmNsb3VkZnJvbnQubmV0L2luZGV4LnBocD9yPXYxL3NlYXJjaC92aWRlbyZsYW5ndWFnZV9mbGFnX2lkPTQ=')
stmbaseurl = b64decode('aHR0cHM6Ly9kMWsydXM2NzFxY29hdS5jbG91ZGZyb250Lm5ldC9kaXN0cmlidXRlX3dlYl90aC5waHA/Y2NzX3Byb2R1Y3RfaWQ9')
caturl = baseurl + '?r=category/series-category&platform_flag_label=web&area_id=4&language_flag_id=4&'
# key = "X-API-KEY=qx3zCittLUGs4arjaopxri2xPGUcANUq"
key = b64decode('WC1BUEktS0VZPXF4M3pDaXR0TFVHczRhcmphb3B4cmkyeFBHVWNBTlVx')
urlapi = b64decode('aHR0cHM6Ly9hcHAubW92aWVjbHViLnR2L2FwaS8=')

def getgenre():
    url = baseurl
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('ul',{'class':'list-unstyled components'})
    # print ul
    li = ul.find_all('li')[4:-16]
    # print li
    genlist=[]
    for i in li:
        url=i.a.get('href')
        if '#' in url:
            title = '> '*10 + i.a.text +' <'*10
        else:
            title = i.a.text
        # print i.a.text
        # print  i.a.get('href')
        genlist.append({'title': title, 'url': i.a.get('href')})

    return genlist
    # return movielist

def getvodlist(url):

    r = requests.get(url)
    print r.content
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    a = soup.findAll('a', {'class': 'moviecover-detail'})
    # print len(a)
    itemslist = []
    for items in a :

        url = items.get('href')
        img = items.img.get('src')
        title = items.h3.text
        itemslist.append({'title': title, 'url': url, 'thumbnail': img, 'action':'section'})

    anext = soup.find('a', {'rel': 'next'})
    if anext:
        nurl = anext.get('href')
        itemslist.append({'title': u"Next", 'thumbnail': 'http://clipartmag.com/images/next-button-clipart-17.png',
                          'url': nurl, 'action':'subcate'})

    return itemslist

def get_sub(url):
    itype  = url.split('/')
    mv = itype[4]
    mvid = itype[5]
    print mv,mvid
    link = urlapi + 'vdo/'+ mv + '?' + mv + '_id=' +  mvid + '&' + key
    r = requests.get(link)
    print r.text
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    # print soup
    div = soup.find('div',{'class':'topmenu-player'})
    print div
    a = div.findAll('a')
    print len(a)
    # print a
    for sub in a :
        print sub.text.strip()
        print sub.get('href')

def get_select(url):
    itype  = url.split('/')
    mv = itype[4]
    mvid = itype[5]
    # print mv,mvid
    link = urlapi + 'vdo/' + mv + '?' + mv + '_id=' + mvid + '&' + key
    if 'movie' in mv:
        return get_mov(link)
    else:
        return get_series(link)





def get_series(link):
    hjson = requests.get(link).json()
    # print hjson
    subjson = hjson['res']
    sublist = []

    th = subjson['link_series']
    if len(th)> 0 : sublist.append({'title':'Thai','extra':'link_series',
                        'thumbnail': 'img', 'action': 'ep','url':link})
    # sublist.append(items)
    st = subjson['link_series_soundtrack']
    if len(st) > 0: sublist.append({'title':'Soundtrack','extra':'link_series_soundtrack',
                        'thumbnail': 'img', 'action': 'ep','url':link})
    ss = subjson['ep_series_soundtrack_5_1_e']
    if len(ss) > 0: sublist.append({'title':'soundtrack51','extra':'ep_series_soundtrack_5_1_e',
                        'thumbnail': 'img', 'action': 'ep','url':link})

    return sublist


def get_ep(url,mmsid):
    # url = url.split('/')
    # itype = url[0]
    # sid = url[1]
    hjson = requests.get(url).json()
    # print hjson
    eplist = []
    eps = hjson['res'][mmsid]
    for genre in eps:
        # print genre

    # # print genre[0]['ep_id']
    #         # print genre.values()
        title = genre['ep_title']
        url =  genre['ep_link']
    # else:
        eplist.append({'title': title, 'url': url,
                    'thumbnail': 'img', 'action': 'stream'})
    return eplist  # r.encoding = "utf-8"



def get_mov(link):
    hjson = requests.get(link).json()
    # print hjson
    items = hjson['res']['link_movie']
    # print len(items)
    seclist = []
    for genre in items:
        url = genre['link_movies']
        title =  genre['describe_type']
        seclist.append({'title': title, 'url': url,
                        'thumbnail': 'img', 'action': 'stream','extra':''})


    return seclist# r.encoding = "utf-8"



def getsearch(arg):
    url =shbaseurl+ arg +'&limit=13&offset=0&'+key
    return getsearchlist(url)



def getsearchlist(url):
    ofs = url.split('offset=')[1].split('&')[0]
    arg = url.split('term=')[1].split('&')[0]
    r = requests.get(url).json()

    total = r['num_rows']
    items = r['res'][1:]
    shlist=[]
    for i in items:
        # print i
        id = i['id']
        itype = i['type']
        title =  i['label'] + ' (' +  itype.capitalize() + (')')
        img = i['link_img']


        if itype =='m':
            url = baseurl + 'movie/'+str(id)
        else:
            url = baseurl + 'series/' + str(id)

        shlist.append({'title': title, 'url': url,
                    'thumbnail': img, 'action': 'section'})


    ofs = int(ofs) + 30
    # print total
    # print ofs
    if total > ofs:
        url = shbaseurl + arg + '&limit=13&offset=' + str(ofs) + '&' + key
        shlist.append({'title': u'NEXT', 'url': url,
                       'thumbnail': 'http://clipartmag.com/images/next-button-clipart-17.png',
                       'action': 'searchlist'})
    return shlist

def savelast(url,title,thumbnail):
    # path =plugintools.get_runtime_path()
    information = {'url': url, 'title': title, 'thumbnail': thumbnail}
    lasttitle = information['url']
    try:
        with open(tmplastpath, "r") as info_read:
            dict_info = json.load(info_read)
            # plugintools.message('title',str(lasttitle))
            for n in dict_info['list']:
                print n
                if lasttitle == n['url']:
                    n_status=True
                    break
                else:
                    n_status = False
            # plugintools.message('n_status',str(n_status))
            if n_status is False:
                dict_info['list'].append(information)
            if len(dict_info['list']) > 10:
                dict_info['list'].pop(1)
    except:
        dict_info = {"list": [{'url': url, 'title': title, 'thumbnail': thumbnail}]}
            # plugintools.message('len',str(len(dict_info)))
    with open(tmplastpath, "w") as data:
        data.write(json.dumps(dict_info))
        data.close()

def loadlast():
    seriesList = []
    with open(tmplastpath, "r") as info_read:
        dict_info = json.load(info_read)
        info_read.close()

    for lv in dict_info['list'][::-1]:
        # print p
        seriesList.append({'title': lv['title'], 'url': lv['url'],'thumbnail':lv['thumbnail']})
    return seriesList

def getstreams(link):
    from random import randint
    uid =  randint(1000,2200)
    slink = b64decode(link)
    url = urlapi + 'buildSecurelink/key?user_id=' + str(uid) + '&' + key
   
    ste = requests.get(url).json()
    ste  = ste['res']
    return slink + ste






if __name__ == '__main__':
    # test_op()
    # getstreams()
    pass
   