import requests,re
import HTMLParser

def get_streamitems(url,lblmatch,stmmatch):
    r = requests.get(url).text
    r = HTMLParser.HTMLParser().unescape(r)
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
    #            'Referer': 'https://stream.movie2free.com/api/sources/1371'}
    # page_data = requests.get(url, headers=headers).text
    # page_data = HTMLParser.HTMLParser().unescape(page_data)
    # r = r.decode('unicode_escape').encode('utf-8')
    # r.encoding = "utf-8"
    # if 'movie2free' in url:
    labelitem = re.compile(lblmatch).findall(r)
    streamitems = re.compile(stmmatch).findall(r)

    return labelitem,streamitems

def run(url):
    if 'leoplayer' in url:
        re_url = get_streamitems(url,'label."(.*?)"','file.."([^"]+)"')
        return re_url
    elif 'iptvz.net'in url:
        re_url = get_streamitems(url, 'label.."(.*?)"', 'file.."([^"]+)"')
        return re_url
    elif 'filebebo.com' in url:
        re_url = get_streamitems(url,'video id="(.*?)"','source.src="([^"]+)"')
        return re_url
    # return re_url
# def run (url,title,thumbnail):
#     if 'upf' in url:
#         resolved_url = upf(url.replace("upfile",'upf'))
#     elif "leoplay" in url:
        # resolved_url = Mya.leo(url)
    # else:
        # final=urlresolver.HostedMediaFile(url)
        # new_url=final.get_url()
        # resolved_url=urlresolver.resolve(new_url)

# if __name__ == '__main__':
    # url ='https://www.leoplayer5.com/watch5?v=908531'
    # url = 'https://www.leoplayer5.com/watch5?v=908531'
# url = 'https://iptv.net/redirector.php/player.php?v=UW7k6VT3w9G'
# print run(url)