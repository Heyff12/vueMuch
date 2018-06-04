# 1. 参数定义

## 1.1. 公共返回参数

- 成功

``` javascript
{
    "respcd": "0000",
    "respmsg": "OK",
    "resperr": "",
    "data": {},  // 或 []
}
```

- 失败

``` javascript
{
    "respcd": "1101",
    "respmsg": "FAIL",
    "resperr": "Invalid request."
}

```

## 1.2 其它返回参数

### 1.2.1 销售放款列表

```javascript
{
    "real_name": "张三",
    "lender_sysdtm": "2018-01-02 12:12:12", // 放款时间
    "trade_amt": "2000.00", //放款金额
    "trade_syssn": "12334234234", // 订单号
    "royalty_amt": "20.00" // 我的分润金额
}
```

### 1.2.2 门店销售情况

```javascript
{
    "district_name": "荣华大区", // 大区名称
    "store_name": "门店名称", // 门店名称
    "store_total_amt": "1000", // 门店放款总金额
    "royalty_amt": "100", // 我的分润
}
```

### 1.2.3 大区销售情况

```javascript
{
    "district_name": "荣华大区", // 大区名称
    "store_total_amt": "1000", // 门店放款总金额
    "royalty_amt": "100", // 我的分润
}
```



# 2. 接口

## 2.1 用户管理类

### 2.1.1 用户绑定手机号
- path: /fenqi/v1/api/user/bind
- methods: POST
- params:

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | mobile | 是    | 手机号  |
    | verify_code | 是    | 手机验证码 |
    | redirect_url | 是  | 记录的上一个地址 |

- return:
```json
{
    "role_type": "1",   // 角色类型 销售人员=1，门店管理人员=3，大区负责人=5，合作商=6，放款方=7，借款人=8
    "redirect_url": "https://xxx.com" // 跳转到某个地址
}
```

### 2.1.2 激活页面，验证码检查,和用户类型检查
- path: /fenqi/v1/api/user/check/info
- methods: POST
- params:

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | mobile | 是    | 手机号  |
    | verify_code | 是 | 验证码 |
    
- return: 
```json
    {
        "status": "1", // 用户状态 1:未绑定手机号 2:已绑定手机号，未激活 3:已绑定手机号并激活( 3 的情况跳转到首页)
        "redirect_url": "xxxxxx",  // 跳转链接，激活状态的时候调用
    }
```

### 2.1.3 用户激活
- path: /fenqi/v1/api/user/active
- methods:POST
- params:

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | mobile | 是    | 手机号  |
    | role_type | 是 | 角色类型 |


- return:

```json
    {
        "redirect_url": "xxxxxx",  // 成功返回跳转页面
    }
```


### 2.1.4 用户基本信息获取
- path: /fenqi/v1/api/user/info
- methods: GET
- params:

- return:
```json
    {
        "base": {
            "nick_name": "张三", // 微信昵称
            "mobile": "123456",  // 手机号
            "status": "1", // 用户状态 1:未绑定手机号 2:已绑定手机号，未激活 3:已绑定手机号并激活 4:已注销
            "role_type": "1", // 角色类型 销售人员=1，门店管理人员=3，大区负责人=5，合作商=6，放款方=7，借款人=8
            "head_url": "", // 微信头像
            "idnumber": "1234"，// 身份证号
            "real_name": "张三", // 真实姓名
        },
        "info": [
            {
                "district_name": "荣华大区", // 大区名称
                "role_name": "大区负责人", // 角色名称
                "store_name": "苹果店铺", // 门店名称
                "address": "成都市高新区", // 门店地址
            },
        ]
    }
```

## 2.2 订单相关

### 2.2.1 销售订单列表查询

- path: /fenqi/v1/api/trade/opuser/list
- methods: GET
- params:
    - page: 页数
    - page_size: 每页记录数

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | user_id | 否    | 用户id  |

- return:
```json
    {
        "opuser_cnt": 200,  // 销售放款记录总数
        "page": 1,
        "page_size": 10,
        "total_trade_amt": "123123", //总的放款金额
        "total_royalty_amt": "1234", // 总的分润金额
        "opuser_trade_infos": [...]  //  销售订单列表
    }
```

### 2.2.2 门店详情列表

- path: /fenqi/v1/api/trade/store/list

- methods: GET

- params:

  - page: 页数
  - page_size: 每页记录数

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | user_id | 否    | 用户id  |

- return:

```json
    {
        "store_cnt": 200,  // 门店记录总数
        "page": 1,
        "page_size": 10,
        "store_trade_infos": [...]  // 门店销售列表
    } 
```

### 2.2.3 大区详情列表
- path: /fenqi/v1/api/trade/district/list

- methods: GET

- params:

  - page: 页数
  - page_size: 每页记录数

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | user_id | 否   | 用户id  |

- return:

```json
    {
        "district_cnt": 200,  // 记录总数
        "page": 1,
        "page_size": 10,
        "district_trade_infos": [...]  // 大区销售列表
    }
```

## 2.4 装修分期相关

### 2.4.1 分期关联用户跳转到析木h5
- path: /fenqi/v1/api/fitment/bind
- methods: GET
- params:

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | mobile | 是    | 手机号  |

- return:
```json
{
    "status": "1", // 用户状态 1:未绑定手机号 2:已绑定手机号，未激活 3:已绑定手机号并激活 4:已注销
    "role_type": "1", // 角色类型 销售人员=1，门店管理人员=3，大区负责人=5，合作商=6，放款方=7，借款人=8
    "redirect_url": "xxxxxx",  // 报错的时候不会出现在这个字段
}
```


## 2.5 工具类

### 2.5.1 发送短信验证码
- path: /fenqi/v1/api/tools/send
- methods: POST
- params:

    | 参数名    | 必填   | 备注   |
    | ------ | ---- | ---- |
    | mobile | 是    | 手机号  |

- return:
```json
{}
```
