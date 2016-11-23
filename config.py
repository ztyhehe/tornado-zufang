# coding:utf-8

import os


# Application配置参数
settings = dict(
	static_path = os.path.join(os.path.dirname(__file__), "static"),
	# template_path = os.path.join(os.path.dirname(__file__), "template"),
	coookie_secret = "m4NYpBm/R3e+2drYi0dxl+73KjdobUbgjaFbiis3coo=",
	xsrf_cookies = True,
	debug = True,
)

# mysql
mysql_options = dict(
	host = "127.0.0.1",
	database = "ihome",
	user = "root",
	password = "root",
)

# reids
redis_options = dict(
	host = "127.0.0.1",
	port = 6379,
)

# 日志
log_file = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"    # 显示级别

session_expires = 86400 # session数据有效期，秒
