# coding:utf-8

import logging

from .BaseHandler import BaseHandler

class IndexHanlder(BaseHandler):
	def get(self):
		self.write(index.html)