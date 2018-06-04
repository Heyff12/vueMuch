# coding: utf-8
from data_packer import RequiredField, OptionalField, DefaultField, CompositedField
from data_packer.checker import (
    ReChecker, LenChecker, TypeChecker, CheckerWrapper,
    text_checker, url_checker
)


class RESP_CODE(object):
    SUCCESS = '0000'

    SYSTEM_ERROR = '1000'
    INNER_SERVICE_ERR = '1001'
    OUTTER_SERVICE_ERR = '1002'

    PARAM_ERROR = '2000'
    DATA_ERROR = '2002'
    ROLE_ERROR = '2003'

    DB_ERROR = '3000'

    PERMISSION_ERROR = '4000'
    USER_NOT_LOGIN = '4001'
    AUTH_FAIL_ERROR = '4002'


RESP_ERR = {
    RESP_CODE.SUCCESS: '成功',

    RESP_CODE.SYSTEM_ERROR: '系统错误',
    RESP_CODE.INNER_SERVICE_ERR: '内部服务错误',
    RESP_CODE.OUTTER_SERVICE_ERR: '外部服务错误',

    RESP_CODE.PARAM_ERROR: '请求参数错误',
    RESP_CODE.DATA_ERROR: '数据错误',
    RESP_CODE.ROLE_ERROR: '用户角色错误',

    RESP_CODE.DB_ERROR: 'DB错误',

    RESP_CODE.PERMISSION_ERROR: '权限错误',
    RESP_CODE.AUTH_FAIL_ERROR: '授权状态未知',
}


FIELD_mobile = RequiredField('mobile', checker=ReChecker(r'[0-9]{11}'))
FIELD_verify_code = RequiredField('verify_code', checker=ReChecker(r'[0-9]{6}'))
FIELD_return_url = OptionalField('return_url', checker=url_checker)
FIELD_user_id = RequiredField('userid', checker=ReChecker(r'[0-9]{1,30}'))
FIELD_role_type = RequiredField('role_type', checker=ReChecker(r'[0-9]{1}'))
FIELD_redirect_url = RequiredField('redirect_url', checker=url_checker)
