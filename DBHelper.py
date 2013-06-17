#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb as mdb
import MySQLdb.cursors

class DBHelper:
	def __init__(self,host,user,passwd,db=None):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.conn = None
		self.cursor = None
		self.db = db

	def __connect(self,db=None):
		if db or self.db:
			try:
				if db:
					self.conn = mdb.connect(self.host,self.user,self.passwd,db)
				else:
					self.conn = mdb.connect(self.host,self.user,self.passwd,self.db,charset='utf8')
			except Exception, e:
				print e
				return
		else:
			try:
				self.conn = mdb.connect(self.host,self.user,self.passwd)
			except Exception, e:
				print e
				return
		self.cursor = self.conn.cursor()
		#self.cursor = mdb.cursors.DictCursor(self.conn)

	def __close(self):
		if self.cursor:
			try:
				self.cursor.close()
			except Exception, e:
				print e
		if self.conn:
			try:
				self.conn.close()
			except Exception, e:
				print e

	def select(self, query, db=None):
		self.__connect(db)
		self.cursor.execute(query)
		data = self.cursor.fetchall()
		self.__close()
		return data

	def update(self, query, value, db=None):
		self.__connect(db)
		self.cursor.execute(query, value)
		self.conn.commit()
		count = self.cursor.rowcount
		self.__close()
		return count

if __name__ == '__main__':
	db = DBHelper('localhost','root','tangbin//','weiboapp')
	#for row in db.select('select * from userlist'):
	#	print row[0]
	print "update userlist set sx='%s'"%('male')
	count = db.update("update userlist set an=%s,qq=%s,email=%s",['22',None,'tbin@gmail.com'])
	print count
	for row in db.select('select * from userlist'):
		print row[2]