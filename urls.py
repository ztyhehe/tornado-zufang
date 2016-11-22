# coding:utf-8

import os
from tornado.web import StaticFileHandler

from handlers import Passport, VerifyCode

handlers = [
	(r"/api/imagecode", VerifyCode.ImageCodeHandler),
	(r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]