# coding: utf-8
import logging


from bin.handler.base_handler import BaseHandler, with_weixin_cid
from bin.constant import RESP_CODE, RESP_ERR
from bin.util import tools

from qfcommon.qfpay.qfuser import with_customer
from qfcommon.thriftclient.fenqi_api import ttypes as fenqi_api_ttypes
from qfcommon.qfpay.apolloclient import Apollo
from qfcommon.thriftclient.apollo import ttypes as apollo_ttyeps
from qfcommon.thriftclient.apollo import ApolloServer

from bin.constant import (
    FIELD_mobile, FIELD_verify_code, FIELD_role_type, FIELD_redirect_url
)

from conf.config import (
    APOLLO_SERVER, ACTIVE_URL, MINE_URL, DOMAIN
)

log = logging.getLogger()


class InfoHandler(BaseHandler):
    """ 用户基本信息获取 """

    ALLOWED_METHODS = ('GET',)

    @with_customer
    def _handle(self):
        cid = self.customer.customer_id
        wx_info = tools.get_weixin_profile(cid)
        log.info('cid %s weixin info ::: %s', cid, wx_info)
        if not wx_info:
            return self.request_finish(RESP_CODE.INNER_SERVICE_ERR, resperr='微信信息获取错误')
        cid_user_ids = tools.query_cid_user(cid)
        if cid_user_ids:
            cid_user_info = tools.get_cid_user(cid_user_ids)
            log.info('func=user_info|cid_user_info=%s', cid_user_info)
            role_type = cid_user_info.role
            base = {
                'nick_name': wx_info['nickname'], 'head_url': wx_info['avatar'],
                'role_type': role_type, 'mobile': cid_user_info.mobile,
            }
            info = []
            # 借款人基本信息查询
            if role_type == fenqi_api_ttypes.USER_ROLE.BORROWER:
                borrower_ids = tools.query_borrower(cid)
                borrower_info = tools.get_borrower(borrower_ids)
                base.update({
                    'status': borrower_info.user_status, 'real_name': '', 'idnumber': ''
                })
            # 销售基本信息查询
            elif role_type == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(cid)
                opuser_info = tools.get_opuser(opuser_ids)
                base.update({
                    'status': opuser_info.status, 'real_name': opuser_info.name,
                    'idnumber': opuser_info.idnumber
                })
                store_ids = tools.query_store(store_mgr_uids=opuser_info.userid)
                store_info = tools.get_store(store_ids)
                client = Apollo(APOLLO_SERVER)
                profile = client.userprofile_by_id(store_info.userid)
                if not profile:
                    return self.request_finish(RESP_CODE.PARAM_ERROR, resperr='查询用户信息失败')
                district_info = tools.get_district([store_info.district_id])

                info.append({
                    "district_name": district_info.name, "role_name": "销售员",
                    "store_name": profile['user']['shopname'], "address": store_info.address
                })
            # 门店管理人基本信息查询
            elif role_type == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
                store_mgr_ids = tools.query_store_mgr(cid)
                store_mgr_info = tools.get_store_mgr(store_mgr_ids)
                base.update({
                    'status': store_mgr_info.status, 'real_name': store_mgr_info.name,
                    'idnumber': store_mgr_info.idnumber
                })
                store_ids = tools.query_store(store_mgr_uids=store_mgr_info.userid)
                store_info = tools.get_store(store_ids)
                client = Apollo(APOLLO_SERVER)
                profile = client.userprofile_by_id(store_info.userid)
                if not profile:
                    return self.request_finish(RESP_CODE.PARAM_ERROR, resperr='查询用户信息失败')
                district_info = tools.get_district([store_info.district_id])
                info.append({
                    "district_name": district_info.name, "role_name": "门店管理人",
                    "store_name": profile['user']['shopname'], "address": store_info.address
                })
            # 大区负责人信息查询
            elif role_type == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
                district_mgr_ids = tools.query_district_mgr(cid)
                district_mgr_info = tools.get_district_mgr(district_mgr_ids)
                base.update({
                    'status': district_mgr_info.status, 'real_name': district_mgr_info.name,
                    'idnumber': district_mgr_info.idnumber
                })
                district_ids = tools.query_district(district_mgr_uids=district_mgr_info.userid)
                district_info = tools.get_district(district_ids)
                info.append({
                    'district_name': district_info.name, 'role_name': '大区负责人',
                })
            else:
                return self.request_finish(RESP_CODE.DATA_ERROR, resperr='暂不支持该类型用户查询')
            return self.request_finish(RESP_CODE.SUCCESS, data={'base': base, 'info': info})
        else:
            return self.request_finish(RESP_CODE.DATA_ERROR, resperr='用户没有绑定手机号')


class CheckInfoHandler(BaseHandler):
    """激活检查用户类型"""

    ALLOWED_METHODS = ('POST',)

    REQ_FIELDS = (
        FIELD_mobile, FIELD_verify_code
    )

    @with_customer
    def _handle(self):
        params = self.parse_request_params()
        cid = self.customer.customer_id
        mobile = params['mobile']
        verify_code = params['verify_code']
        flag = tools.check_code(mobile, verify_code)
        log.info('cid: %s, mobile: %s, verify_code: %s', cid, mobile, verify_code)
        if not flag:
            return self.request_finish(RESP_CODE.DATA_ERROR, resperr='请输入正确的短信验证码')
        cid_user_ids = tools.query_cid_user(mobile=mobile)
        cid_user_info = tools.get_cid_user(cid_user_ids)
        if cid_user_info:
            if cid_user_info.cid != cid:
                return self.request_finish(RESP_CODE.ROLE_ERROR, resperr='该手机号与当前用户不匹配')
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.BORROWER:
                return self.request_finish(RESP_CODE.ROLE_ERROR, resperr='销售信息匹配失败，请确保手机号填写正确')

            elif cid_user_info.role == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(cid)
                opuser_info = tools.get_opuser(opuser_ids)
                return self.request_finish(
                    RESP_ERR.SUCCESS,
                    data={'status': opuser_info.status, 'redirect_url': DOMAIN + MINE_URL}
                )

            elif cid_user_info.role == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
                store_mgr_ids = tools.query_store_mgr(cid)
                store_mgr_info = tools.get_store_mgr(store_mgr_ids)
                return self.request_finish(
                    RESP_ERR.SUCCESS,
                    data={'status': store_mgr_info.status, 'redirect_url': DOMAIN + MINE_URL}
                )

            elif cid_user_info.role == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
                district_mgr_ids = tools.query_district_mgr(cid)
                district_mgr_info = tools.get_district_mgr(district_mgr_ids)
                return self.request_finish(
                    RESP_ERR.SUCCESS,
                    data={'status': district_mgr_info.status, 'redirect_url': DOMAIN + MINE_URL}
                )
            else:
                return self.request_finish(RESP_CODE.ROLE_ERROR, resperr='销售信息匹配失败，请确保手机号填写正确')
        else:
            # TODO 不是销售人员
            return self.request_finish(RESP_CODE.ROLE_ERROR, resperr='销售信息匹配失败，请确保手机号填写正确')


class ActiveHandler(BaseHandler):
    """用户激活"""

    ALLOWED_METHODS = ('POST',)
    REQ_FIELDS = (
        FIELD_mobile, FIELD_role_type
    )

    @with_customer
    def _handle(self):
        cid = self.customer.customer_id
        params = self.parse_request_params()
        mobile = params['mobile']
        role_type = int(params['role_type'])
        log.info('func=activehandler|cid=%s|mobile=%s|role_type=%s', cid, mobile, role_type)
        if role_type == fenqi_api_ttypes.USER_ROLE.OPUSER:
            opuser_ids = tools.query_opuser(cid)
            tools.update_opuser(opuser_ids[0], fenqi_api_ttypes.USER_STATUS.ACTIVED)
        elif role_type == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
            store_mgr_ids = tools.query_store_mgr(cid)
            tools.update_store_mgr(store_mgr_ids[0], fenqi_api_ttypes.USER_STATUS.ACTIVED)
        elif role_type == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
            district_mgr_ids = tools.query_district_mgr(cid)
            tools.update_district_mgr(district_mgr_ids[0], fenqi_api_ttypes.USER_STATUS.ACTIVED)
        else:
            return self.request_finish(RESP_CODE.DATA_ERROR, resperr='销售信息匹配失败，请确保手机号填写正确')

        return self.request_finish(
            RESP_CODE.SUCCESS,
            data={'redirect_url': DOMAIN + MINE_URL}
        )


class BindHandler(BaseHandler):
    ''' 用户绑定手机号'''

    ALLOWED_METHODS = ('POST',)
    REQ_FIELDS = (
        FIELD_mobile, FIELD_verify_code, FIELD_redirect_url
    )

    @with_customer
    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        cid = self.customer.customer_id
        mobile = params['mobile']
        verify_code = params['verify_code']
        redirect_url = params['redirect_url']
        flag = tools.check_code(mobile, verify_code)
        log.info('cid: %s, mobile: %s, verify_code: %s', cid, mobile, verify_code)
        if not flag:
            return self.request_finish(RESP_CODE.DATA_ERROR, resperr='验证码错误，请输入正确的短信验证码')

        #TODO 处理处理判断用户类型，将来用户状态修改为已绑定, 根据用户类型返回跳转页面
        cid_user_ids = tools.query_cid_user(mobile=mobile)
        if cid_user_ids:
            cid_user_info = tools.get_cid_user(cid_user_ids)
            # 借款人 cid 查询
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.BORROWER:
                return self.request_finish(
                    RESP_CODE.SUCCESS,
                    data={'redirect_url': redirect_url, 'role_type': fenqi_api_ttypes.USER_ROLE.BORROWER}
                )
            # 根据销售人员id，修改状态，并且绑定 cid
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.OPUSER:
                opuser_ids = tools.query_opuser(opuid=cid_user_info.opuid, userid=cid_user_info.userid)
                tools.update_opuser(opuser_ids[0], fenqi_api_ttypes.USER_STATUS.BIND, cid=cid)
            # 根据门店管理人id，修改状态，并且绑定 cid
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.STORE_MGR:
                store_mgr_ids = tools.query_store_mgr(userid=cid_user_info.userid)
                tools.update_store_mgr(store_mgr_ids[0], fenqi_api_ttypes.USER_STATUS.BIND, cid=cid)
            # 根据大区负责人id，修改状态，并且绑定 cid
            if cid_user_info.role == fenqi_api_ttypes.USER_ROLE.DISTRICT_MGR:
                district_mgr_ids = tools.query_district_mgr(userid=cid_user_info.userid)
                tools.update_district_mgr(district_mgr_ids[0], fenqi_api_ttypes.USER_STATUS.BIND, cid=cid)

            # 更新 cid2user 表，添加 cid 字段
            tools.update_cid_user(cid_user_ids[0], cid)
            return self.request_finish(
                RESP_CODE.SUCCESS,
                data={'redirect_url': ACTIVE_URL, 'role_type': cid_user_info.role}
            )
        else:
            # 借款人初次绑定 cid 以及手机号
            admin = -1
            tools.create_borrower(cid, fenqi_api_ttypes.USER_STATUS.BIND, mobile, admin)
            tools.create_cid_user(cid, fenqi_api_ttypes.USER_ROLE.BORROWER, mobile, admin)
            return self.request_finish(
                RESP_CODE.SUCCESS,
                data={'redirect_url': redirect_url, 'role_type': fenqi_api_ttypes.USER_ROLE.BORROWER}
            )
