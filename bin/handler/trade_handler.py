# coding: utf-8
from decimal import Decimal
import datetime
import logging

from qfcommon.qfpay.qfuser import with_customer
from qfcommon.base.dbpool import get_connection_exception
from qfcommon.qfpay import defines
from bin.handler.base_handler import BaseHandler, with_weixin_cid, HandlerException
from bin.util import tools
from conf import config
from bin.constant import RESP_CODE

log = logging.getLogger()


class OpuserHandler(BaseHandler):
    ALLOWED_METHODS = ("GET",)

    @with_customer
    def _handle(self, *args, **kwargs):
        cid = self.customer.customer_id
        log.info('cid %s', cid)
        data = {
            "opuser_cnt": 0,
            "page": 0,
            "page_size": 0,
            "total_trade_amt": "0",
            "total_royalty_amt": "0",
            "opuser_trade_infos": []
        }
        return self.request_finish(RESP_CODE.SUCCESS, data=data)


class StoreHandler(BaseHandler):
    ALLOWED_METHODS = ("GET",)

    def _handle(self, *args, **kwargs):
        data = {
            "store_cnt": 0,
            "page": 0,
            "page_size": 0,
            "store_trade_infos": []
        }
        return self.request_finish(RESP_CODE.SUCCESS, data=data)


class DistrictHandler(BaseHandler):
    ALLOWED_METHODS = ("GET",)

    def _handle(self, *args, **kwargs):
        data = {
            "district_cnt": 0,
            "page": 0,
            "page_size": 0,
            "district_trade_infos": []
        }
        return self.request_finish(RESP_CODE.SUCCESS, data=data)
