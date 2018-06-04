# -*- coding: utf-8 -*-
import json, requests


def getstreams(url):
    response = requests.get(url)
    todos = json.loads(response.text)
    dictodo =todos['result']['channels']
    strmlist = []
    for ch in dictodo:
        # print ch['streamer']
        # print ch['server']
        # print ch['logo']
        # print ch['name']
        # for k in ch:
        urlString = "http://" + ch['server'] + ":1935/" +'liveedge'+ "/" + ch['streamer'] + "_" + '600' + "/playlist.m3u8"
        # print urlString
        strmlist.append({"url": urlString, "title": ch['name'],'thumbnail':ch['logo']})
    return strmlist
if __name__ == '__main__':
    print getstreams('http://psitv.tv/api/Channels')