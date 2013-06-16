#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import urllib
import urllib2
from bs4 import BeautifulSoup

class BaikeSnippet:
    def get_html(self,title):
        title = title.decode('utf-8').encode('gbk')
        keyword = urllib.quote(title)
        url = 'http://baike.baidu.com/search?word='+keyword+'&type=0&pn=0&rn=10&submit=search'
        print url
        try:
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            data = result.read()
            result.close()
        except:
            data = None
        return data

    def __parse_snippet(self, data):
        if data:
            soup = BeautifulSoup(data)
            param = soup.find('div',class_="abstract")
            if param:
                #return re.sub(r'<[^>]*?>', '', param).strip()
                return param.get_text().strip()
        return None

    def __parse_url(self, data):
        if data:
            soup = BeautifulSoup(data)
            try:
                href = soup.find('h2').a
                if href:
                    return 'http://baike.baidu.com' + href['href']
            except:
                return None
        return None

    def get_snippet(self,title):
        data = self.get_html(title)
        return self.__parse_snippet(title)

    def get_url(self, title):
        data = self.get_html(title)
        return self.__parse_url(data)

    def get_both(self, title):
        data = self.get_html(title)
        collector = dict()
        if data:
            collector['snippet'] = self.__parse_snippet(data)
            collector['url'] = self.__parse_url(data)
        return collector
                

if __name__ == '__main__':
    baikeSnippet = BaikeSnippet()
    #baikeSnippet.get_keywords('result_sorted')
    keyword = 'ai'
    #print baikeSnippet.get_snippet(keyword)
    #print baikeSnippet.get_url(keyword)
    collector = baikeSnippet.get_both(keyword)
    print collector['snippet']
    print collector['url']
            
