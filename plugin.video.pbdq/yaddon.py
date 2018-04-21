# -*- coding: utf-8 -*-
import requests,re,urllib,os,json,binascii,sys
import urllib2
from bs4 import BeautifulSoup

# def get_html
import time
# from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def getMenu():
    r = requests.get('https://www.viu.com/ott/th/')
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('ul', {'class':"v-nav test"})
    li = ul.findAll('a',{'class':''})
    seriesList = []
    # print (li)
    for link in li:
            # print link.text.replace('\n', '')
            # print link.get('href')
            seriesList.append({'title':link.text.replace('\n', ''),'url':link.get('href')})
    return seriesList

def getgerne(url):
    # url = 'https://www.viu.com/ott/th/th/category/27/'
    # driver = webdriver.Firefox()

    pt = sys.path[0] + '/phantomjs.exe'
    dr = webdriver.PhantomJS(executable_path=pt)
    dr.get(url)
    html = dr.page_source
    dr.close()
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    # ul = soup.findAll('ul', {"id": "nav2"})
    ul = soup.find('ul', {"class": "dropdown-content"})
    # print ul
    gernelist =[]
    for id in ul:
        # print id.find('a')
        if id.find('a').get('id') != None:
            gerneid = id.find('a').get('data-value')
            title = id.find('a').text

        else:
            continue
        gernelist.append({'title': title, 'url': urllib.unquote(url).decode('utf8'),'gid':gerneid})

    return gernelist


def getyear(url):
    # url = 'https://www.viu.com/ott/th/th/category/27/'
    # driver = webdriver.Firefox()

    pt = sys.path[0] + '/phantomjs.exe'
    dr = webdriver.PhantomJS(executable_path=pt)

    dr.get(url)
    html = dr.page_source
    dr.close()
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    # ul = soup.findAll('ul', {"id": "nav2"})
    div = soup.find('div', {"id": "cat-filter-dd-1"})
    ul = div.find('ul',{'class':'dropdown-content'})
    # print li
    yearlist = []
    for id in ul:
        # print id.find('a')
        if id.find('a').get('id') != None:
            yearid = id.find('a').get('data-value')
            title = id.find('a').text
        else:
            continue
        yearlist.append({'title': title, 'url':urllib.unquote(url).decode('utf8'), 'yid':yearid})
    return yearlist


def getSeries(url,yid):
    pt = sys.path[0] + '/phantomjs.exe'
    dr = webdriver.PhantomJS(executable_path=pt)

    dr.get(url)

    # geid = 'cat_dd_0_'+str(gid)
    idy = 'cat_dd_1_'+str(yid)
    # dr.find_element_by_id('cat-filter-dd-0').click()
    # dr.find_element_by_id(geid).click()
    dr.find_element_by_id('cat-filter-dd-1').click()
    dr.find_element_by_id(idy).click()
    time.sleep(5)

    html = dr.page_source
    dr.quit()
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    # ul = soup.findAll('ul', {"id": "nav2"})
    # ul = soup.find('ul', {"class": "dropdown-content"})
    ul = soup.find('div', {"id": "cat_list"})
    div = ul.findAll('div', {"class": "item float-left "})
    # img = div.find('img')
    seriesList = []
    for item in div:
        # print item.a.get('href')
        # print item.find('div').find('a').text
        # print item.find('a').find('img').get('src').replace('/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', '')
        # seriesList.append({'title': item.find('div').find('a').text, 'url': urllib.unquote(url).decode('utf8'),
        #                    'thumbnail': ''})
        seriesList.append({'title': item.find('div').find('a').text, 'url': item.a.get('href'),
                           'thumbnail': item.find('a').find('img').get('src').replace(
                               '/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', '')})

    next = soup.find('a',{'class':'load-more-btn'})
    if next != None:
        seriesList.append({'title':u"โหลดทังหมด" ,'url': urllib.unquote(url).decode('utf8')})
    return seriesList



def getSeriesAll(url,yid):
    pt = sys.path[0] + '/phantomjs.exe'
    dr = webdriver.PhantomJS(executable_path=pt)

    dr.get(url)

    idy = 'cat_dd_1_' + str(yid)
    dr.find_element_by_id('cat-filter-dd-1').click()
    dr.find_element_by_id(idy).click()
    time.sleep(5)
    wait = WebDriverWait(dr, 10)
    while True:
    # scrape some data on a page and extract table

    # click next link
        try:
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'แสดงเพิ่ม')]")))
            # element =wait.until(EC.visibility_of_element_located("//a[contains(text(), 'Next')]"))
            element.click()
        except TimeoutException:
            break

    html = dr.page_source
    dr.quit()
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    # ul = soup.findAll('ul', {"id": "nav2"})
    # ul = soup.find('ul', {"class": "dropdown-content"})
    ul = soup.find('div', {"id": "cat_list"})
    div = ul.findAll('div', {"class": "item float-left "})
    # img = div.find('img')
    seriesList = []
    for item in div:
        # print item.a.get('href')
        # print item.find('div').find('a').text
        # print item.find('a').find('img').get('src').replace('/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', '')
        # seriesList.append({'title': item.find('div').find('a').text, 'url': urllib.unquote(url).decode('utf8'),
        #                    'thumbnail': ''})
        seriesList.append({'title': item.find('div').find('a').text, 'url': item.a.get('href'),
                           'thumbnail': item.find('a').find('img').get('src').replace(
                               '/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', '')})

    # next = soup.find('a', {'class': 'load-more-btn'})
    # if next != None:
    #     seriesList.append({'title': u"โหลดทังหมด", 'url': urllib.unquote(url).decode('utf8')})
    return seriesList


def getEpisodes(url):
    r = requests.get('https://www.viu.com'+url)
    soup = BeautifulSoup(r.text, 'html5lib')
    soup.prettify()
    ul = soup.find('ul', {'class': "video-alllist clearfix common-panel"})
    li = ul.findAll('li', {'class': "episode-item released"})
    # print li
    episodesList = []
    for ep in li:
        # print ep.get('id')
        id = ep.get('data-id')
        title =  ep.find('p',{ 'class':"video-num"}).text.strip()
        title = title +'--' + ep.find('p').text
        # img = ep.find('img').get('data-original').replace('/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', '')
        # print ep.find('a').get('href')
        episodesList.append({"title":title,"url":ep.find('a').get('href'),'thumbnail':ep.find('img').get('data-original').replace('/ott/th/v1/imgprocess/reduceImage.php?p=30&img=', ''),'epid':id })
    return episodesList 
        
def getStreams(url,epid):
    # url = 'https://www.viu.com/ott/th/th/vod/63165/Witchs-Court'
    pt = sys.path[0] + '/phantomjs.exe'
    dr = webdriver.PhantomJS(executable_path=pt)
    dr.get('https://www.viu.com'+url)
    html = dr.page_source
    dr.quit()
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    div = soup.findAll('a', {"class": "undefined"})
    sourceList = []
    get_sub(url)
    for item in div:
        # print item.get('href')
        title = 'HD' if item.text == ""else item.text
        # print title

        sourceList.append({"title":title,"url":item.get('href')})

    return sourceList


def get_sub(url):
    # url = '/ott/th/th/vod/63165/Witchs-Court'
    epid = url.split('/')[5]
    gurl = 'https://play.grabvdo.com/viu/th/' + str(epid)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Referer': 'http://www.kseries.co/'}
    source = requests.get(gurl, headers=headers)
    sub_qry = re.compile('file.."([^"]+)","label".".u0e20').findall(source.text)
    # vdo_qry = re.compile('sources.*?file.."([^"]+)"').findall(source.text)
    surl = sub_qry[0].replace('\/','/')
    # url = vdo_qry[0].replace('\/','/')

    downloadsub(surl)

def downloadsub(url):
    dest = sys.path[0] + '/resources/temp/s.srt'
    # dest ='/home/yaya/PycharmProjects/untitled/sub.srt'
    pip = '127.0.0.1:3128'
    proxy_handler = urllib2.ProxyHandler({'http': pip})
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req)

    fi = open(dest, "w")
    fi.write(sock.read())
    fi.close()

def adFly(url):
    r = requests.get('http://skizzerz.net/scripts/adfly.php?url='+url)
    soup = BeautifulSoup(r.text , 'html5lib')
    return soup.find('a').get('href')

def yandex(url):
    try:
        s = requests.Session()
        r = s.get(url)
        r = re.sub(r'[^\x00-\x7F]+',' ', r.text)

        sk = re.findall('"sk"\s*:\s*"([^"]+)', r)[0]

        idstring = re.findall('"id"\s*:\s*"([^"]+)', r)[0]

        idclient = binascii.b2a_hex(os.urandom(16))

        post = {'idClient': idclient, 'version': '3.9.2', 'sk': sk, '_model.0': 'do-get-resource-url', 'id.0': idstring}
        #post = urllib.urlencode(post)

        r = s.post('https://yadi.sk/models/?_m=do-get-resource-url', data=post)
        r = json.loads(r.text)

        url = r['models'][0]['data']['file']

        return url
    except:
        return

def getSpecialEpisodes(url,find='p'):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html5lib')

    ul = soup.find('div', {"class": "post-wrapper"})

    p = ul.findAll(find)

    epsList = []
    last = None
    for eps in p:
        if last == None:
            last=eps
        a = eps.findAll('a')
        if a != []:
            strong = eps.find('strong')
            subject = ''
            if strong != None:
                subject = strong.text
            else:
                laststrong = last.find('strong')
                if laststrong != None:
                    subject = laststrong.text
                else:
                    epstext = eps.text
                    if u'פרק' in epstext:
                        subject=epstext
                    else:
                        subject = last.text
            
            subject = re.sub('\n.*','',subject)
            if u'פרק' in subject:
                epsList.append({'title':subject,'url':a})
        last = eps
    
    if epsList == [] and find=='p':
        return getSpecialEpisodes(url,'address')
        
    return epsList

def getSpecialStreams(url,episode):
    epsList = getSpecialEpisodes(url)
    strmList = []
    for item in epsList:
        if item.get('title') == episode.decode('utf-8'):
            return item.get('url')
    return strmList
def extractLinks(a):
    linkList = []
    for link in a:
        linkList.append(link.get('href'))
    return linkList

#print yandex("https://yadi.sk/i/cF7-Y0tGhZ94G")
# print getEpisodes("/ott/th/th/vod/67440/Hate-to-Love-You")
# print getStreams('/ott/th/th/vod/67440/Hate-to-Love-You',67440)
#print getSpecialStreams('http:/,token=""/www.asia4hb.com/view/jeon-woo-chi', u'פרק 2')
# print getMenu()


# print getVdosub('/ott/th/th/vod/67440/Hate-to-Love-You')
# default.Download_subtitle(sys.path[0] + '/resources/temp', 'nameteat', subtitle_url )
# url = urllib2.urlopen("http://myjamtv.com/stream_url.txt").readline().strip()
# url = 'https://www.viu.com/ott/th/th/category/27/'
# url = 'https://www.viu.com/ott/th/th/category/27/'
# print getgerne(url)
# print getSeriesAll(url,'2011')