# coding:utf-8

import os

from handlers import BaseHandler
from handlers import Passport
from handlers import VerifyCode
from handlers import SignUpAndLogIn
from handlers import House
from handlers import Profile

handlers = [
    (r"/api/imagecode", VerifyCode.ImageCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r"/api/signup", SignUpAndLogIn.SignUpHandler),
    (r"/api/login", SignUpAndLogIn.LogInHandler),
    (r"/api/logout", SignUpAndLogIn.LogOutHandler),
    (r"/api/check_login", SignUpAndLogIn.CheckLogInHandler),
    (r'^/api/profile$', Profile.ProfileHandler),
    (r'^/api/profile/avatar$', Profile.AvatarHandler),
    (r'^/api/profile/name$', Profile.NameHandler),
    (r'^/api/profile/auth$', Profile.AuthHandler),
    (r'^/api/house/info$', House.HouseInfoHandler),
    (r'^/api/house/image$', House.HouseImageHandler),
    (r'^/api/house/area$', House.AreaInfoHandler),
    (r'^/api/house/my$', House.MyHousesHandler),
    (r'^/api/house/index$', House.IndexHandler),
    (r'^/api/house/list$', House.HouseListHandler),
    (r"/(.*)", BaseHandler.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]