# coding:utf-8

import logging
from re import match

from .BaseHandler import BaseHandler
from utils.response_code import RET


class SignUpHandler(BaseHandler):
	'''注册接口'''
	def post(self):
		# 获取参数
		mobile = self.json_args.get("mobile")
		sms_code_text = self.json_args.get("phoneCode")
		passwd = self.json_args.get("passwd")
		if not all((mobile, sms_code_text)):
			return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
		if not match(r'1\d{10}', mobile):
			return self.write(dict(errno=RET.PARAMERR, errmsg="手机号格式错误"))

		# 判断手机号是否已经注册
		sql = "SELECT up_user_id FROM ih_user_profile WHERE up_mobile = %s"
		if self.db.get(sql, mobile):
			return self.write(dict(errno=RET.DATAEXIST, errmsg="该手机号已经注册过"))

		# 判断短信验证码
		try:
			real_sms_code_text = self.redis.get("sms_code_%s" % mobile)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		# 判断是否过期
		if not real_sms_code_text:
			return self.write(dict(errno=RET.NODATA, errmsg="验证码失效"))
		if real_sms_code_text.lower() != sms_code_text.lower():
			return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))

		# 存入数据库
		sql = "INSERT INTO ih_user_profile (up_name,up_mobile,up_passwd) VALUES (%s,%s,%s)"
		try:
			self.db.insert(sql, mobile, mobile, passwd)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="添加出错"))
		else:
			try:
				self.redis.delect("sms_code_%s" % mobile)
			except Exception as e:
				logging.error(e)
			return self.write(dict(errno=RET.OK, errmsg="OK"))


class LogInHandler(BaseHandler):
	pass