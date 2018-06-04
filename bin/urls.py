# -*- coding: utf-8 -*-

from bin.handler import (
    user_handler, trade_handler, page_handler,
    other_handler, tool_handler,
)


urls = (
    # 用户相关
    # 用户绑定手机号
    (r'^/fenqi/v1/api/user/bind$', user_handler.BindHandler),
    # 用户个人信息获取
    (r'^/fenqi/v1/api/user/info$', user_handler.InfoHandler),
    # 检查用户是否激活，是否需要继续发送短信
    (r'^/fenqi/v1/api/user/check/info$', user_handler.CheckInfoHandler),
    # 激活用户
    (r'^/fenqi/v1/api/user/active$', user_handler.ActiveHandler),


    # 贷款订单相关
    # 销售订单列表查询
    (r'^/fenqi/v1/api/trade/opuser/list$', trade_handler.OpuserHandler),
    # 门店订单列表查询
    (r'^/fenqi/v1/api/trade/store/list$', trade_handler.StoreHandler),
    # 大区订单列表查询
    (r'^/fenqi/v1/api/trade/district/list$', trade_handler.DistrictHandler),

    # 借款人相关操作
    # 析木跳转相关
    (r'^/fenqi/v1/api/fitment/bind$', other_handler.XimuBindHandler),

    # 工具方法
    # 发送短信
    (r'^/fenqi/v1/api/tools/send$', tool_handler.SendCodeHandler),


    # 页面托管
    (r'^/fenqi/v1/page/me.html$', page_handler.MineHandler),  # 我的
    (r'^/fenqi/v1/page/period.html$', page_handler.PeriodHandler),  # 装修分期

    (r'^/fenqi/v1/page/activate.html$', page_handler.PageHandler),  # 激活页面
    (r'^/fenqi/v1/page/single.html$', page_handler.PageHandler),
    (r'^/fenqi/v1/page/relevance.html$', page_handler.PageHandler),  # 填写销售人员
    (r'^/fenqi/v1/page/register.html$', page_handler.PageHandler),  # 绑定手机号
    (r'^/fenqi/v1/page/mine.html$', page_handler.PageHandler),  # 我的页面
    (r'^/fenqi/v1/page/notfound.html$', page_handler.PageHandler),  # 404 页面
)
