# coding: utf-8
import functools
import json
import copy
import logging
import traceback
import data_packer
from urllib import urlencode

from data_packer.container import DictContainer
from qfcommon.qfpay.apollouser import ApolloUser
from qfcommon.qfpay.qfuser import user_from_session, QFUser
from qfcommon.web.core import Handler
from qfcommon.thriftclient.captcha import ttypes as captcha_ttypes
from qfcommon.thriftclient.payquick_api import ttypes as pay_quick_api_ttypes

from bin.constant import RESP_CODE, RESP_ERR
from bin.util import tools
from conf.config import (
    DOMAIN, APPID, CID_URL
)

log = logging.getLogger()


def with_weixin_cid(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        try:
            self.csid = self.get_cookie('csid')
            if not self.csid:
                log.info("===>> start get cid @ NEWCID 1")
                redirect_uri = "%s%s?%s" % (DOMAIN, self.req.path, self.req.query_string)
                req_param = {'redirect_uri': redirect_uri, 'appid': APPID}
                cidurl="%s?%s"%(CID_URL, urlencode(req_param))
                log.info('NEWCID==>>cidurl=%s', cidurl)
                return self.redirect(cidurl)
        except:
            log.error('check_login error: %s' % traceback.format_exc())
            return self.request_finish(RESP_CODE.USER_NOT_LOGIN, resperr=' 微信公众号授权问题')

        log.info('csid: %s', self.csid)
        return func(self, *args, **kwargs)
    return _


class HandlerException(Exception):

    def __init__(self, respcd, respmsg=''):
        self.respcd = respcd
        self.respmsg = respmsg


class BaseHandler(Handler):
    ALLOWED_METHODS = ()
    REQ_FIELDS = []  #

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.cid = None

    def initial(self):
        pass

    def GET(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def POST(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def handle(self, *args, **kwargs):
        if self.req.method not in self.ALLOWED_METHODS:
            return getattr(super(BaseHandler, self), self.req.method)()

        try:
            log.info('<<<< START %s.%s >>>>', self.__class__.__module__, self.__class__.__name__)
            ret = self._handle(*args, **kwargs)
            log.info('<<<< END %s.%s >>>>', self.__class__.__module__, self.__class__.__name__)
            return ret
        except HandlerException as e:
            log.warn(traceback.format_exc())
            return self.request_finish(e.respcd, resperr=e.respmsg)
        except captcha_ttypes.CaptchaException as e:
            log.warn(traceback.format_exc())
            return self.request_finish(respcd=e.respcd, resperr=e.respmsg)
        except pay_quick_api_ttypes.PayquickException:
            log.warn(traceback.format_exc())
            return self.request_finish(RESP_CODE.OUTTER_SERVICE_ERR)
        except Exception:
            log.warn(traceback.format_exc())
            return self.request_finish(RESP_CODE.INNER_SERVICE_ERR)

    def _handle(self, *args, **kwargs):
        raise NotImplementedError()

    def parse_request_params(self, check_params=True):
        if self.req.method == 'GET':
            req_params = self.req.input()
            tools.mask_customer_info(self.req.input(), in_place=True)
        else:
            try:
                req_params = json.loads(self.req.postdata())
                self.req.storage.value = json.dumps(
                    tools.mask_customer_info(req_params),
                )
            except Exception:
                log.warn(traceback.format_exc())
                raise HandlerException(RESP_CODE.PARAM_ERROR, respmsg='parse params error')

        # TODO IMPORTANT   屏蔽掉req中的敏感信息，避免在日志中被qfcommon/web/core.py打出
        log.info('Request params: %s', tools.mask_customer_info(req_params))

        if check_params:
            req_params = self.check_params(req_params)
            log.info('func=check_params|req_params=%s', req_params)

        return req_params

    def check_params(self, params):
        ret = {}
        dp = data_packer.DataPacker(self.REQ_FIELDS)
        try:
            dp.run(
                DictContainer(params),
                DictContainer(ret),
            )
        except data_packer.err.DataPackerError:
            log.warn(traceback.format_exc())
            raise HandlerException(RESP_CODE.PARAM_ERROR, respmsg='参数非法')

        return ret

    def request_finish(self, respcd, respmsg='', resperr='', **kwargs):
        self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
        if not resperr:
            resperr = RESP_ERR.get(respcd, '')
        resp = {
            'respcd': respcd,
            'respmsg': respmsg,
            'resperr': resperr,
        }
        resp.update(kwargs)
        resp = json.dumps(resp, separators=(',', ':'), sort_keys=True)
        log.info('Response: %s', resp)
        return resp
