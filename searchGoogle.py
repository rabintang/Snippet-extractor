#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import urllib
import simplejson

class GoogleSnippet:
    counter = 0
    def __init__(self,keyfile):
        self.keys = []
        self.cx = None
        reader = open(keyfile)
        for key in reader:
            self.keys.append(key.strip())
        if len(self.keys) > 0:
            self.cx = self.keys[0]
            del self.keys[0]
    
    def __searchKey(self,key,cx,keyword):
        url = ('https://www.googleapis.com/customsearch/v1?'
                'key=%s'
                '&cx=%s'
                '&alt=json'
                '&q=%s'
                '&num=1')%(key,cx,urllib.quote(keyword))
        try:
            request = urllib2.Request(url, None)
            response = urllib2.urlopen(url)
            #Process the JSON string.
            results = simplejson.load(response)
            print results
            info = results['items']
            return info
        except Exception,e:
            print e
            return None

    def get_snippet(self, title):
        index = GoogleSnippet.counter / 100
        results = self.__searchKey(self.keys[index],self.cx,title)
        print results
        GoogleSnippet.counter = GoogleSnippet.counter+1
        if results:
            return results[0]['snippet']
        else:
            return None

if __name__ == '__main__':
    title = '中国'
    googleSnippet = GoogleSnippet('keys')
    print googleSnippet.get_snippet(title)
