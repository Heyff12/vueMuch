webpackJsonp([9],{"16mW":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});a("sVYa");var n=a("7+uW"),r=a("v5o6"),s=a.n(r),i=a("/ocq"),o={name:"salesrecord",components:{},data:function(){return{opuser_url:"/fenqi/v1/api/trade/opuser/list",pages_all:0,pages:1,page_per:20,page_now:1,list_now:[],total_trade_amt:0,total_royalty_amt:0}},created:function(){this.getList()},methods:{getList:function(){var t=this,e={page:this.page_now,page_size:this.page_per};this.$ajax_axios.ajax_get(this,this.opuser_url,e,function(e){t.pages_all=e.data.opuser_cnt,t.total_trade_amt=e.data.total_trade_amt,t.total_royalty_amt=e.data.total_royalty_amt,t.pages_all<=0?Toast("暂无信息"):t.list_now=e.data.opuser_trade_infos})}}},l={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("section",{staticClass:"totalHead"},[a("ul",[a("li",[a("dl",[a("dt",[t._v("共放款（元）")]),t._v(" "),a("dd",{class:t.total_trade_amt.toString().length>=12?"fontS":""},[t._v(t._s(t._f("crash_format")(t.total_trade_amt)))])])]),t._v(" "),a("li",[a("dl",[a("dt",[t._v("我的分润（元）")]),t._v(" "),a("dd",{class:t.total_royalty_amt.toString().length>=12?"fontS":""},[t._v("+"+t._s(t._f("yuan")(t.total_royalty_amt)))])])])])]),t._v(" "),a("section",{staticClass:"saleList"},[a("ul",t._l(t.list_now,function(e){return a("li",[a("dl",[a("dt",[a("span",{staticClass:"fr color"},[t._v("+"+t._s(t._f("yuan")(e.royalty_amt)))]),t._v(t._s(e.real_name))]),t._v(" "),a("dd",[t._v("分期单号："+t._s(e.trade_syssn))]),t._v(" "),a("dd",{staticClass:"grey"},[t._v("放款金额："+t._s(t._f("crash_format")(e.trade_amt))),a("span",{staticClass:"divide"}),t._v("放款日期："+t._s(t._f("date_cut")(e.lender_sysdtm,10)))])])])}))])])},staticRenderFns:[]};var u=a("VU/8")(o,l,!1,function(t){a("1wiS")},null,null).exports;n.default.use(i.a);var c=[{path:"/",redirect:"/salesrecord"},{name:"salesrecord",path:"/salesrecord",component:u}],d=new i.a({scrollBehavior:function(){return{x:0,y:0}},routes:c}),_=(a("bbc5"),a("rAnJ"),a("1avm"));n.default.prototype.$ajax_axios=_.a,window.FastClick=s.a,new n.default({el:"#app",router:d,template:"<App/>",components:{App:u}})},"1avm":function(t,e,a){"use strict";var n=a("34+y"),r=(a.n(n),a("X+yh")),s=a.n(r),i=a("qONS"),o=(a.n(i),a("UQTY")),l=a.n(o),u=a("7+uW"),c=a("mtWM"),d=a.n(c),_=a("Rf8U"),f=a.n(_);u.default.use(f.a,d.a);e.a={ajax_get:function(t,e,a,n,r,i,o){var u=t;l.a.open(),u.$http.get(e,{params:a}).then(function(t){if(l.a.close(),o)return o(a),!1;var e=t.data;"0000"==e.respcd?n&&n(e):(e.respmsg?s()(e.respmsg):s()(e.resperr),r&&r(e))},function(t){i&&i(),l.a.close(),s()("系统问题,请稍后再试")}).catch(function(t){i&&i(),l.a.close()})},ajax_post:function(t,e,a,n,r,i,o){var u=t;l.a.open(),u.$http.post(e,a).then(function(t){if(l.a.close(),o)return o(a),!1;var e=t.data;"0000"==e.respcd?n&&n(e):(e.respmsg?s()(e.respmsg):s()(e.resperr),r&&r(e))},function(t){i&&i(),l.a.close(),s()("系统问题,请稍后再试")}).catch(function(t){i&&i(),l.a.close()})}}},"1wiS":function(t,e){},"34+y":function(t,e){},ULTG:function(t,e){},bbc5:function(t,e,a){"use strict";var n=a("7+uW");n.default.filter("yuan",function(t){return(t/100).toFixed(2)}),n.default.filter("yuan_z",function(t){return(t/100).toFixed(0)}),n.default.filter("hide_code",function(t){if(t.length<=10)return t;var e=t.substr(0,6),a=t.substr(-4);return e+"********************".substr(0,t.length-10)+a}),n.default.filter("crash_float_format",function(t){if(t-0<=0)return 0;var e=t.split("."),a=e[0],n=void 0,r="",s="";if(e.length>1&&e[1]-0>0&&(n=e[1]),n&&(r="."+n),a.length<=3)return a+r;for(var i=a.split("").reverse(),o=0;o<i.length;o++)s+=i[o]+((o+1)%3==0&&o+1!=i.length?",":"");return s.split("").reverse().join("")+r}),n.default.filter("crash_format",function(t,e){var a=void 0;if((a="JPY"==e||"IDR"==e?t:(t/100).toFixed(2))-0<=0)return 0;var n=a.toString().split("."),r=n[0],s=void 0,i="",o="";if(n.length>1&&n[1]-0>0&&(s=n[1]),i=s?"."+s:".00",r.length<=3)return r+i;for(var l=r.split("").reverse(),u=0;u<l.length;u++)o+=l[u]+((u+1)%3==0&&u+1!=l.length?",":"");return o.split("").reverse().join("")+i}),n.default.filter("date_cut",function(t,e){return t.substr(0,e)})},qONS:function(t,e){},rAnJ:function(t,e){function a(){WeixinJSBridge.call("hideOptionMenu"),WeixinJSBridge.call("hideToolbar")}"undefined"==typeof WeixinJSBridge?document.addEventListener?document.addEventListener("WeixinJSBridgeReady",a,!1):document.attachEvent&&(document.attachEvent("WeixinJSBridgeReady",a),document.attachEvent("onWeixinJSBridgeReady",a)):a()}},["16mW"]);
//# sourceMappingURL=salesrecord.ec0aca0d148c32256062.js.map