# coding:utf-8

import logging
from re import match
from hashlib import sha256

import config
from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined
from utils.session import Session


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
            passwd = sha256(mobile + config.passwd_hash_key + passwd).hexdigest()
            res = self.db.execute(sql, mobile, mobile, passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="添加出错"))

        # 删除redis中的sms_code
        try:
            self.redis.delect("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)

        # 添加该用户session
        try:
            self.session = Session(self)
            self.session.data['user_id'] = res
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)

        return self.write(dict(errno=RET.OK, errmsg="OK"))


class LogInHandler(BaseHandler):
    """登录"""
    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all([mobile, password]):
            return self.write({"errno":RET.PARAMERR, "errmsg":"参数错误"})
        res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s", mobile=mobile)
        password = sha256(mobile + config.passwd_hash_key + password).hexdigest()
        if res and res["up_passwd"] == unicode(password):
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write({"errno":RET.OK, "errmsg":"OK"})
        else:
            return self.write({"errno":RET.DATAERR, "errmsg":"手机号或密码错误！"})


class LogOutHandler(BaseHandler):
    """登出"""
    @require_logined
    def get(self):
        self.session.clear()
        self.write({"errno":0, "errmsg":"OK"})


class CheckLogInHandler(BaseHandler):
    """检查登陆状态"""
    def get(self):
        if self.get_current_user():
            self.write({"errno":RET.OK, "errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errno":RET.SESSIONERR, "errmsg":"false"})

