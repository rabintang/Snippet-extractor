#!/usr/bin/python
#-*- coding: utf-8 -*-

from DBHelper import DBHelper
from searchBaike import BaikeSnippet
from searchWiki import WikiSnippet
from searchGoogle import GoogleSnippet

from Queue import Queue
import os
import threading
import logging

class Snippeter(threading.Thread):
	def __init__(self,t_name,queue):
		threading.Thread.__init__(self)
		self.name = t_name
		self.data = queue

	def run(self):
		db = init_db('db.config')
		baike = BaikeSnippet()
		wiki = WikiSnippet()
		google = GoogleSnippet('keys')

		while not self.data.empty():
			try:
				row = self.data.get()
				brif = None
				wiki_url = None
				baike_url = None

				collector = wiki.get_both(row[1])
				if collector['snippet']: # wikipedia has this item
					brif = collector['snippet']
					wiki_url = collector['url']
					baike_url = baike.get_url(row[1])
				else: # wikipedia doesn't have
					collector = baike.get_both(row[1])
					if collector['snippet']: # baike has
						brif = collector['snippet']
						baike_url = collector['url']
					else: # neither baike or wikipedia have
						brif = google.get_snippet(row[1])
				db.update('UPDATE `abbreviation` SET bk=%s,wk=%s,bf=%s WHERE abrid=%s',[baike_url,wiki_url,brif,row[0]])
				logging.info('%s is finished',row[1])
			except Exception,e:
				title = 'Not Known'
				if row:
					title = row[1]
				logging.error('%s '+e,title)
				continue

def init_db(dbconfpath):
	file = open(dbconfpath)
	dbconfig = []
	for line in file:
		dbconfig.append(line.strip())
	file.close()
	db = None
	if len(dbconfig) == 3:
		db = DBHelper(dbconfig[0],dbconfig[1],dbconfig[2])
	elif len(dbconfig) == 4:
		db = DBHelper(dbconfig[0],dbconfig[1],dbconfig[2],dbconfig[3])
	return db

if __name__ == '__main__':	
	logging.basicConfig(filename='snippet.log',filemode='a',format='[%(asctime)s]-%(levelname)s : %(message)s',level=logging.DEBUG)

	db = init_db('db.config')
	queue = Queue()
	for row in db.select('SELECT abrid,kl FROM `abbreviation`'):
		queue.put(row)

	snippet_list = []
	for i in range(0,10):
		snippet_list.append(Snippeter(i,queue))
		snippet_list[i].start()
	for i in range(0,10):
		snippet_list[i].join()
	logging.info('All is finished!')