# coding:utf-8

import logging
import constants
from re import match
from time import time
from random import randint

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp

class ImageCodeHandler(BaseHandler):
	'''图片验证码传输'''

	def get(self):
		code_id = self.get_argument("codeid")
		pre_code_id = self.get_argument("pcodeid")
		if pre_code_id:
			try:
				self.redis.delete("image_code_%s" % pre_code_id)
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


class SMSCodeHandler(BaseHandler):
	'''发送手机验证码'''

	def post(self):
		# 获取参数
		mobile = self.json_args.get("mobile")
		image_code_id = self.json_args.get("image_code_id")
		image_code_text = self.json_args.get("image_code_text")
		if not all((mobile, image_code_text, image_code_id)):
			return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
		if not match(r'1\d{10}', mobile):
			return self.write(dict(errno=RET.PARAMERR, errmsg="手机号格式错误"))

		# 判断距上次成功发送是否超过60秒
		try:
			self.redis.get("sms_time_%s" % mobile)
		except Exception as e:
			logging.error(e)
			logging.error("不到60秒,多次请求")
			return self.write(dict(errno=RET.REQERR, errmsg="不到60秒"))

		# 判断图片验证码
		try:
			real_image_code_text = self.redis.get("image_code_%s" % image_code_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		# 判断是否过期
		if not real_image_code_text:
			return self.write(dict(errno=RET.NODATA, errmsg="验证码失效"))
		if real_image_code_text.lower() != image_code_text.lower():
			return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))

		# 若成功：
		# 生成随机短信验证码
		sms_code = "%04d" % randint(0, 9999)
		try:
			self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="生成验证码错误"))

		# 发送短信
		try:
			json_sms_return_data = ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)
			# 判断返回值
			if not "000000" == json_sms_return_data["statusCode"]:
				logging.error("yuntongxun SMS is error")
				logging.error(json_sms_return_data)
				logging.debug(type(json_sms_return_data))
				return self.write(dict(errno=RET.THIRDERR, errmsg="短信发送错误"))
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.THIRDERR, errmsg="短信发送错误"))

		self.redis.setex("sms_time_%s" % mobile, constants.SMS_CODE_FORBIDDEN_EXPIRES, int(time()))
		return self.write(dict(errno=RET.OK, errmsg="OK"))

