# coding:utf-8

import os

from handlers import BaseHandler
from handlers import Passport
from handlers import VerifyCode
from handlers import SignUpAndLogIn

handlers = [
	(r"/api/imagecode", VerifyCode.ImageCodeHandler),
	(r"/api/smscode", VerifyCode.SMSCodeHandler),
	(r"/api/signup", SignUpAndLogIn.SignUpHandler),
	(r"/(.*)", BaseHandler.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]