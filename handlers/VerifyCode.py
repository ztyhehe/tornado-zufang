# coding:utf-8

import logging
import constants

from .Basehandler import BaseHandler
from utils.captcha.captcha import captcha

class ImageCodeHandler(BaseHandler):
	'''图片验证码传输'''

	def get(self):
		code_id = self.get_argument("codeid")
		pre_code_id = self.get_argument("pcodeid")
		if pre_code_id:
			try:
				self.redis.deleter("image_code_%s" % pre_code_id)
			except Exception as e:
				logging.error(e)
		# name 图片验证码名称
		# text 图片验证码文本
		# image 图片验证码二进制数据
		name, text, image = captcha.generate_captcha()
		try:
			self.redis.setex("image_code_%s" % code_id, constants.IMAGE_CODE_EXPIRES_SECONDS, text)
		except Exception as e:
			logging.error(e)
			self.write("")
		else:
			self.set_header("Content-Type", "image/jpg")
			self.write(image)


class PhoneCodeHandler(BaseHandler):
	'''发送手机验证码'''
	
	def post(self):
		# 获取参数
		# 判断图片验证码
		# 若成功：
		# 发送短信
		# 不成功：
		# 返回错误信息
		pass