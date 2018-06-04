# coding: utf-8
import logging

from qfcommon.web import cache
from bin.util import tools
from bin.constant import RESP_CODE
from bin.handler.base_handler import BaseHandler, with_weixin_cid

from qfcommon.qfpay.qfuser import with_customer
from qfcommon.thriftclient.fenqi_api import ttypes as fenqi_api_ttypes

from bin.constant import (
    FIELD_mobile
)

log = logging.getLogger()


class XimuBindHandler(BaseHandler):
    ALLOWED_METHODS = ('GET',)
    REQ_FIELDS = (FIELD_mobile, )

    @with_customer
    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        mobile = params['mobile']
        cid_user_ids = tools.query_cid_user(mobile=mobile)
        if cid_user_ids:
            redirect_url = ''
            cid_user_info = tools.get_cid_user(cid_user_ids)
            role_type = cid_user_info.role
            status = fenqi_api_ttypes.USER_STATUS.NOT_BIND
            if role_type == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(
                    opuid=cid_user_info.opuid, userid=cid_user_info.userid
                )
                if not opuser_ids:
                    return self.request_finish(RESP_CODE.ROLE_ERROR, resperr='没有查到相关销售人员')
                opuser_info = tools.get_opuser(opuser_ids)
                status = opuser_info.status
        else:
            redirect_url = ''
            role_type = fenqi_api_ttypes.USER_ROLE.BORROWER
            status = fenqi_api_ttypes.USER_STATUS.NOT_BIND

        return self.request_finish(
            RESP_CODE.SUCCESS,
            data={
                'redirect_url': redirect_url,
                'status': status, 'role_type': role_type
            }
        )
