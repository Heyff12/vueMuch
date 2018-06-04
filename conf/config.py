# coding:utf-8
import os
from conf.webconfig import *

# 服务地址
HOST = '0.0.0.0'

# 服务端口
PORT = 7010

# 调试模式: True/False
# 生产环境必须为False
DEBUG = False

# 日志文件配置
LOGFILE = {
    'root': {
        'filename': {
            'DEBUG': os.path.join(os.path.dirname(HOME), 'log', 'fenqi_portal.log'),
            'ERROR': os.path.join(os.path.dirname(HOME), 'log', 'fenqi_portal.error.log'),
        },
    },
}
LOGFILE = 'stdout'
LOG_WHEN = None

# 数据库配置
dbcf = {
    'qf_fenqi': {
        'token': 'server_core',
        'engine': 'pymysql',
        'conn': 10,
    }
}

APOLLO_SERVER = [{'addr': ('192.168.0.7', 6900), 'timeout': 20000}]

# 微信服务地址
WEIXIN_SERVER = [{'addr': ('172.100.101.107', 6120), 'timeout': 3000}]

# openuser 地址
OPENUSER_SERVER = [{'addr': ('172.100.101.107', 7700), 'timeout': 3000}]
OPENUSER_APPID = 10004

# fenqi_api 地址
FENQI_SERVER = [{'addr': ('192.168.0.7', 8002), 'timeout': 30000}]

# CAPTCHA
CAPTCHA_SERVER = [{'addr': ('172.100.101.107', 6000), 'timeout': 30000}]
CAPTCHA_SRC = 'fenqi' # 服务
CAPTCHA_EXPIRES = 10 # 验证码过期时间
CAPTCHA_LENGTH = 6 # 验证码长度
CAPTCHA_MODE = 1 # 验证码类型 1:纯数字
CAPTCHA_LIMIT_TIME = 5 # 获取验证码时间间隔
CAPTCHA_VERIFY_MODE_NOT_DELETE = 0 # 0:验证之后不删除
CAPTCHA_CONTENT = '【好近分期】验证码：%s，有效期5分钟。请勿轻易透露验证码给他人。' # 短信内容
CAPTCHA_TARGET = '测试' # 消息来源类型

# PRESMS 服务地址
PRESMS_SERVER = [{'addr': ('172.100.101.107', 4444), 'timeout': 5000}]
PRESMS_TAG = '验证码是:'

# 本服务地址, 用于拼接URL返回给前端
DOMAIN = "http://cd.qa.qfpay.net"
# 新版获取CID
CID_URL = 'https://o2.qa.qfpay.net/trade/v1/customer/get'
# 好近分期 appid
APPID = 'wx087a3fc3f3757766'

# errmsg 表缓存有效期
ERRMSG_CACHE_EXPIRE = 3600

# 未绑定手机号时跳转到绑定页面
REGISTER_URL = '/fenqi/v1/page/register.html'
# 我的页面
MINE_URL = '/fenqi/v1/page/mine.html'
# 激活页面
ACTIVE_URL = '/fenqi/v1/page/activate.html'
# 绑定销售人员页面
OPUSER_BIND_URL = '/fenqi/v1/page/relevance.html'
# 404 页面
NOT_FUND_PAGE = '/fenqi/v1/page/notfound.html'
