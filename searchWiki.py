#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

class WikiSnippet:
    def __ini__(self):
        self.snippet = None
        self.url = None
    
    def get_html(self,title):
        title = title.decode('utf-8').encode('gbk')
        title = title.upper()
        article = urllib.quote(title)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
        self.url = "http://zh.wikipedia.org/zh-cn/" + article
        try:
            resource = opener.open(self.url)
            data = resource.read()
            resource.close()
        except:
            return None
        return data

    def __parse_snippet(self, data):
        if data:
            soup = BeautifulSoup(data)
            if soup.find('table',id='disambigbox') != None: # It is a disambiguate page
                try:
                    li = soup.find('div',id='mw-content-text').li
                    if li:
                        href_list = li.find_all('a')
                        title = href_list[len(href_list)-1]['title']
                        data = self.get_html(title)
                        return self.__parse_snippet(data)
                    else:
                        return None
                except:
                    return None
            elif soup.find('div',id='noarticletext_technical') == None:
                return soup.find('div',id='mw-content-text').p.get_text()
        return None

    def get_snippet(self,title):
        data = self.get_html(title)
        self.snippet = self.__parse_snippet(data)
        return self.snippet

    def get_url(self, title):
        data = self.get_html(title)
        self.get_snippet(title)
        if self.snippet == None:
            self.url = None
        return self.url

    def get_both(self, title):
        collector = dict()
        self.get_url(title)
        collector['snippet'] = self.snippet
        collector['url'] = self.url
        return collector
        
if __name__ == '__main__':
    title= "机器学习"
    wikiSnippet = WikiSnippet();
    collector = wikiSnippet.get_both(title)
    print collector['snippet']
    print collector['url']
