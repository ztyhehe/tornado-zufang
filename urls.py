# coding:utf-8

import os

from handlers import Passport
from handlers import VerifyCode
from handlers import BaseHandler

handlers = [
	(r"/api/imagecode", VerifyCode.ImageCodeHandler),
	(r"/api/smscode", VerifyCode.SMSCodeHandler),
	(r"/(.*)", BaseHandler.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]