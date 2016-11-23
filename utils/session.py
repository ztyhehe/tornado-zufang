# coding:utf-8

import logging
import json
from uuid import uuid4

import config


class Session(object):
	'''添加session的模块'''
	def __init__(self, request_handler):
		self.request_handler = request_handler
		self.session_id = self.request_handler.get_secure_cookie("session_id")
		if not self.session_id:
			# 第一次访问 生成session_id
			self.session_id = uuid4().get_hex()
			self.data = {}
		else:
			# 已经有session_id
			# 取出并在redis中获取数据data
			try:
				data = self.request_handler.redis.get("sess_%s" % self.session_id)
			# 如果读取数据库出错
			except Exception as e:
				logging.error(e)
				self.data = {}
			# 如果读取出的数据为空
			if not self.data:
				self.data = {}
			else:
				self.data = json.loads(data)

	def save(self):
		# 序列化成json
		json_data = json.dumps(self.data)
		try:
			self.request_handler.redis.setex("sess_%s" % self.session_id, config.session_expires, json_data)
		except Exception as e:
			logging.error(e)
			raise Exception("save session failed")
		else:
			# 如果没出错 设置cookie
			self.request_handler.set_secure_cookie("session_id", self.session_id)

	def clera(self):
		self.request_handler.set_secure_cookie("session_id")
		try:
			self.request_handler.redis.delect("sess_%s" % self.session_id)
		except Exception as e:
			logging.error(e)

