# coding: utf-8
import logging
import os
from urllib import urlencode

from bin.handler.base_handler import BaseHandler, with_weixin_cid
from bin.util import tools

from qfcommon.qfpay.qfuser import with_customer
from qfcommon.thriftclient.fenqi_api import ttypes as fenqi_api_ttypes

from conf.config import (
    REGISTER_URL, ACTIVE_URL, NOT_FUND_PAGE, OPUSER_BIND_URL, DOMAIN,
    MINE_URL
)

log = logging.getLogger()


class MineHandler(BaseHandler):

    ALLOWED_METHODS = ('GET', 'POST')

    def _redirect_url(self, status):
        if status == fenqi_api_ttypes.USER_STATUS.NOT_BIND:
            return REGISTER_URL + '?redirect_url=' + self.base_path
        elif status == fenqi_api_ttypes.USER_STATUS.BIND:
            return ACTIVE_URL
        elif status == fenqi_api_ttypes.USER_STATUS.ACTIVED:
            return MINE_URL
        else:
            return NOT_FUND_PAGE

    @with_weixin_cid
    @with_customer
    def _handle(self):
        cid = self.customer.customer_id
        cid_user_ids = tools.query_cid_user(cid)
        self.base_path = DOMAIN + self.req.path
        if cid_user_ids:
            cid_user_info = tools.get_cid_user(cid_user_ids)
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.BORROWER:
                borrower_ids = tools.query_borrower(cid)
                borrower_info = tools.get_borrower(borrower_ids)
                if borrower_info.user_status == fenqi_api_ttypes.USER_STATUS.BIND:
                    return self.redirect(MINE_URL)
                return self.redirect(REGISTER_URL + '?redirect_url=' + self.base_path)

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(cid)
                opuser_info = tools.get_opuser(opuser_ids)
                return self.redirect(self._redirect_url(opuser_info.status))

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
                store_mgr_ids = tools.query_store_mgr(cid)
                store_mgr_info = tools.get_store_mgr(store_mgr_ids)
                return self.redirect(self._redirect_url(store_mgr_info.status))

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
                district_mgr_ids = tools.query_district_mgr(cid)
                district_mgr_info = tools.get_district_mgr(district_mgr_ids)
                return self.redirect(self._redirect_url(district_mgr_info.status))

        return self.redirect(REGISTER_URL + '?redirect_url=' + self.base_path)


class PeriodHandler(BaseHandler):
    """ 装修分期"""

    ALLOWED_METHODS = ('GET', 'POST')

    def _redirect_url(self, status):
        if status == fenqi_api_ttypes.USER_STATUS.NOT_BIND:
            return REGISTER_URL + '?redirect_url=' + self.base_path
        elif status == fenqi_api_ttypes.USER_STATUS.BIND:
            return ACTIVE_URL
        elif status == fenqi_api_ttypes.USER_STATUS.ACTIVED:
            return OPUSER_BIND_URL
        else:
            return NOT_FUND_PAGE

    @with_weixin_cid
    @with_customer
    def _handle(self, *args, **kwargs):
        cid = self.customer.customer_id
        cid_user_ids = tools.query_cid_user(cid)
        self.base_path = DOMAIN + self.req.path
        if cid_user_ids:
            cid_user_info = tools.get_cid_user(cid_user_ids)
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.BORROWER:
                borrower_ids = tools.query_borrower(cid)
                borrower_info = tools.get_borrower(borrower_ids)
                if borrower_info.status == fenqi_api_ttypes.USER_STATUS.BIND:
                    return self.redirect(OPUSER_BIND_URL)
                return self.redirect(REGISTER_URL + '?redirect_url=' + self.base_path)

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(cid)
                opuser_info = tools.get_opuser(opuser_ids)
                return self.redirect(self._redirect_url(opuser_info.status))

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
                store_mgr_ids = tools.query_store_mgr(cid)
                store_mgr_info = tools.get_store_mgr(store_mgr_ids)
                return self.redirect(self._redirect_url(store_mgr_info.status))

            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
                district_mgr_ids = tools.query_district_mgr(cid)
                district_mgr_info = tools.get_district_mgr(district_mgr_ids)
                return self.redirect(self._redirect_url(district_mgr_info.status))
        return self.redirect(REGISTER_URL + '?redirect_url=' + self.base_path)


class PageHandler(BaseHandler):
    ALLOWED_METHODS = ('GET', 'POST')

    @with_weixin_cid
    def _handle(self):
        filename = os.path.basename(self.req.path)
        return self.render(filename)
