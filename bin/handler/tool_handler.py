# coding: utf-8
import logging

from bin.util import tools
from bin.constant import RESP_CODE
from bin.handler.base_handler import BaseHandler
from bin.constant import (
    FIELD_mobile,
)
log = logging.getLogger()


class SendCodeHandler(BaseHandler):
    '''
     发送短信
    '''
    ALLOWED_METHODS = ('POST', )
    REQ_FIELDS = (FIELD_mobile, )

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        mobile = params.get('mobile')

        code = tools.gen_code(mobile)
        ret, msg = tools.send_sms(mobile, code)
        if ret:
            return self.request_finish(RESP_CODE.SUCCESS, resperr=msg)
        return self.request_finish(RESP_CODE, resperr=msg)
