# coding: utf-8

import json
from contextlib import contextmanager
import logging
import copy

from qfcommon.base.tools import thrift_callex
from qfcommon.server.client import ThriftClient
from qfcommon.base.tools import mask_card
from qfcommon.thriftclient.captcha import CaptchaServer
from qfcommon.thriftclient.qf_customer import QFCustomer
from qfcommon.qfpay.presmsclient import PreSms
from qfcommon.base.tools import smart_utf8
from qfcommon.thriftclient.fenqi_api import FenqiServer
from qfcommon.thriftclient.fenqi_api import ttypes as fenqi_api_ttypes

from conf.config import (
    OPENUSER_SERVER, OPENUSER_APPID,
    CAPTCHA_SERVER, CAPTCHA_SRC,
    CAPTCHA_EXPIRES, CAPTCHA_LENGTH, CAPTCHA_MODE,
    CAPTCHA_LIMIT_TIME, CAPTCHA_CONTENT, CAPTCHA_TARGET,
    CAPTCHA_VERIFY_MODE_NOT_DELETE, PRESMS_SERVER,
    PRESMS_TAG, FENQI_SERVER
)

log = logging.getLogger()


def call_captcha(func, *args, **kwargs):
    log.info('req captcha func=%s|args=%s|kwargs=%s', func, args, kwargs)
    client = ThriftClient(CAPTCHA_SERVER, CaptchaServer)
    client.raise_except = True
    ret = client.call(func, *args, **kwargs)
    log.info('req captcha func=%s|ret=%s', func, ret)
    return ret


def call_fenqi_api(func, *args, **kwargs):
    log.info('<<<< req fenqi_api func=%s | args=%s | kwargs=%s', func, args, kwargs)
    client = ThriftClient(FENQI_SERVER, FenqiServer, framed=True)
    client.raise_except = True
    ret = client.call(func, *args, **kwargs)
    log.info('>>>> resp fenqi_api func=%s | result=%s', func, ret)
    return ret


def mask_customer_info(req, in_place=False):
    """
    """
    # 判断是否原地替换
    if not in_place:
        req = copy.deepcopy(req)

    if 'pri_acct_no' in req:
        req['pri_acct_no'] = mask_card(req['pri_acct_no'])

    return req


def get_weixin_profile(customer_id):
    ''' 获取微信基本信息'''
    spec = json.dumps({'id': customer_id})
    profiles = thrift_callex(
        OPENUSER_SERVER, QFCustomer, 'get_profiles',
        OPENUSER_APPID, spec
    )
    if not profiles:
        return {}
    return profiles[0].__dict__


def gen_code(mobile):
    ''' 获取验证码'''
    code = call_captcha(
        'captcha_get_ex', ucode=mobile, src=CAPTCHA_SRC,
        expires=CAPTCHA_EXPIRES, length=CAPTCHA_LENGTH,
        mode=CAPTCHA_MODE, limit_time=CAPTCHA_LIMIT_TIME
    )
    return code


def send_sms(mobile, code):
    '''发送验证码'''
    sms = PreSms(PRESMS_SERVER)
    content = CAPTCHA_CONTENT % code
    ret, msg = sms.sendSms(mobile, smart_utf8(content), PRESMS_TAG, CAPTCHA_SRC, CAPTCHA_TARGET)
    log.info('func=send_sms|mobile=%s|code=%s|ret=%s|msg=%s', mobile, code, ret, unicode(msg, 'utf-8'))
    return ret, msg


def check_code(mobile, code):
    ''' 验证验证码'''
    flag = False
    ret = call_captcha(
        'captcha_check_ex', ucode=mobile, src=CAPTCHA_SRC,
        code=code, mode=CAPTCHA_VERIFY_MODE_NOT_DELETE
    )
    if ret == 0:
        flag = True
    log.info('func=check_code|mobile=%s|code=%s|ret=%s|flag=%s', mobile, code, ret, flag)
    return flag


def create_cid_user(cid, role, mobile, admin):
    """创建关系"""
    log.info('func=create_cid_user|cid=%s|role=%s', cid, role)
    info = fenqi_api_ttypes.Cid2user()
    info.cid = int(cid)
    info.role = int(role)
    info.mobile = int(mobile)
    ret = call_fenqi_api('cid2user_create', info, admin)
    return ret


def query_cid_user(cid=None, mobile=None):
    log.info('func=query_cid_user|cid=%s', cid)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.Cid2userQueryArg()
    arg.query_meta = meta
    if cid:
        arg.cids = [int(cid)]
    if mobile:
        arg.mobiles = [int(mobile)]
    ret = call_fenqi_api('cid2user_query', arg)
    return ret


def update_cid_user(cid_user_id, cid, admin=-1):
    '''更新关系表'''

    log.info('func=update_district_mgr|input=%s|%s', cid_user_id, cid)
    info = fenqi_api_ttypes.Cid2user()
    info.cid = int(cid)
    infos = {cid_user_id: info}
    ret = call_fenqi_api('cid2user_update', infos, admin)
    return ret


def get_cid_user(cid_user_ids):
    log.info('func=get_cid_user|input=%s', cid_user_ids)
    cid_user_map = call_fenqi_api('cid2user_get', cid_user_ids)
    real_name_id = cid_user_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def query_district_mgr(cid=None, userid=None):
    ''' 查询大区信息'''
    log.info('func=query_district_mgr|cid=%s', cid)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.DistrictMgrQueryArg()
    arg.query_meta = meta
    if cid:
        arg.cids = [int(cid)]
    if userid:
        arg.userids = [userid]
    ret = call_fenqi_api('district_mgr_query', arg)
    return ret


def get_district_mgr(district_mgr_ids):
    ''' 大区信息获取'''
    log.info('func=get_district_mgr|input=%s', district_mgr_ids)
    cid_user_map = call_fenqi_api('district_mgr_get', district_mgr_ids)
    real_name_id = district_mgr_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def update_district_mgr(district_mgr_id, status, cid=None, admin=-1):
    ''' 更新 大区负责人信息'''

    log.info('func=update_district_mgr|input=%s|%s', district_mgr_id, status)
    info = fenqi_api_ttypes.DistrictMgr()
    info.status = status
    if cid:
        info.cid = int(cid)
    infos = {district_mgr_id: info}
    ret = call_fenqi_api('district_mgr_update', infos, admin)
    return ret


def query_store_mgr(cid=None, userid=None):
    ''' 查询门店管理人员信息'''
    log.info('func=query_store_mgr|cid=%s|userid=%s', cid, userid)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.StoreMgrQueryArg()
    arg.query_meta = meta
    if cid:
        arg.cids = [int(cid)]
    if userid:
        arg.userids = [userid]
    ret = call_fenqi_api('store_mgr_query', arg)
    return ret


def get_store_mgr(store_mgr_ids):
    '''门店管理人员信息获取'''
    log.info('func=get_store_mgr|input=%s', store_mgr_ids)
    cid_user_map = call_fenqi_api('store_mgr_get', store_mgr_ids)
    real_name_id = store_mgr_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def update_store_mgr(store_mgr_id, status, cid=None, admin=-1):
    ''' 更新门店管理人状态'''
    log.info('func=udpate_store_mgr|inpur=%s:%s', store_mgr_id, status)
    info = fenqi_api_ttypes.StoreMgr()
    info.status = status
    if cid:
        info.cid = int(cid)
    infos = {store_mgr_id: info}
    ret = call_fenqi_api('store_mgr_update', infos, admin=-1)
    return ret


def query_opuser(cid=None, opuid=None, userid=None):
    ''' 查询销售人员信息'''
    log.info('func=query_opuser|cid=%s', cid)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.OpuserQueryArg()
    arg.query_meta = meta
    if cid:
        arg.cids = [int(cid)]
    if opuid:
        arg.opuids = [int(opuid)]
    if userid:
        arg.userids = [int(userid)]
    # 不管有没有实名认证都有返回
    ret = call_fenqi_api('opuser_query', arg)
    return ret


def get_opuser(opuser_ids):
    ''' 销售人员信息获取'''
    log.info('func=get_opuser|input=%s', opuser_ids)
    cid_user_map = call_fenqi_api('opuser_get', opuser_ids)
    real_name_id = opuser_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def update_opuser(opuser_id, status, cid=None, admin=-1):
    ''' 更新销售人员信息'''
    log.info('func=udpate_opuser|inpur=%s:%s', opuser_id, status)
    info = fenqi_api_ttypes.Opuser()
    info.status = status
    if cid:
        info.cid = int(cid)
    infos = {opuser_id: info}
    ret = call_fenqi_api('opuser_update', infos, admin)
    return ret


def create_borrower(cid, status, mobile, admin):
    ''' 创建借款人'''
    log.info('func=create_borrower|')
    info = fenqi_api_ttypes.Borrower()
    info.cid = int(cid)
    info.user_status = status
    info.mobile = int(mobile)
    ret = call_fenqi_api('borrower_create', info, admin)
    return ret


def query_borrower(cid):
    ''' 查询消费者信息'''
    log.info('func=query_borrower|cid=%s', cid)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.BorrowerQueryArg()
    arg.query_meta = meta
    arg.cids = [int(cid)]
    ret = call_fenqi_api('borrower_query', arg)
    return ret


def get_borrower(borrower_ids):
    ''' 消费者获取'''
    log.info('func=get_opuser|input=%s', borrower_ids)
    cid_user_map = call_fenqi_api('borrower_get', borrower_ids)
    real_name_id = borrower_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def query_store(store_mgr_uids=None, userids=None):
    ''' 查询门店信息'''
    log.info('func=query_store|userids=%s|store_mgr_uids=%s', userids, store_mgr_uids)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.StoreQueryArg()
    arg.query_meta = meta
    if store_mgr_uids:
        arg.store_mgr_uids = [store_mgr_uids]
    if userids:
        arg.userids = [int(userids)]
    ret = call_fenqi_api('store_query', arg)
    return ret


def get_store(store_ids):
    '''获取门店信息'''
    log.info('func=get_store|input=%s', store_ids)
    cid_user_map = call_fenqi_api('store_get', store_ids)
    real_name_id = store_ids[0]
    info = cid_user_map.get(real_name_id)
    return info


def query_district(district_mgr_uids=None, ids=None):
    ''' 查询门店信息'''
    log.info('func=query_district|district_mgr_uids=%s|ids=%s', district_mgr_uids, ids)
    meta = fenqi_api_ttypes.QueryMeta()
    meta.offset = None
    meta.count = None
    arg = fenqi_api_ttypes.DistrictQueryArg()
    arg.query_meta = meta
    if district_mgr_uids:
        arg.district_mgr_uids = [int(district_mgr_uids)]
    if ids:
        arg.district_ids = [int(ids)]
    ret = call_fenqi_api('district_query', arg)
    return ret


def get_district(district_ids):
    '''获取门店信息'''

    log.info('func=get_district|input=%s', district_ids)
    cid_user_map = call_fenqi_api('district_get', district_ids)
    real_name_id = district_ids[0]
    info = cid_user_map.get(real_name_id)
    return info
