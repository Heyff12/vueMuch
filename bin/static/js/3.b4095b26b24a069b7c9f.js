webpackJsonp([3],{"7zr6":function(t,s){},UToy:function(t,s,a){"use strict";Object.defineProperty(s,"__esModule",{value:!0});a("34+y");var e=a("X+yh"),n=a.n(e),o={name:"store",components:{},data:function(){return{store_url:"/fenqi/v1/api/trade/store/list",pages_all:0,pages:1,page_per:20,page_now:1,list_now:[]}},created:function(){this.getStoreList()},methods:{getStoreList:function(){var t=this,s={page:this.page_now,page_size:this.page_per};this.$ajax_axios.ajax_get(this,this.store_url,s,function(s){t.pages_all=s.data.store_cnt,t.pages_all<=0?n()("暂无信息"):t.list_now=s.data.store_trade_infos})}}},_={render:function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"salesBank"},t._l(t.list_now,function(s){return a("section",{staticClass:"salesList"},[a("div",{staticClass:"salesTop"},[t._v("\n            "+t._s(s.district_name)+"-"+t._s(s.store_name)+"\n        ")]),t._v(" "),a("div",{staticClass:"totalHead"},[a("ul",[a("li",[a("dl",[a("dt",[t._v("共放款（元）")]),t._v(" "),a("dd",{class:s.store_total_amt.toString().length>=12?"fontS":""},[t._v(t._s(t._f("crash_format")(s.store_total_amt)))])])]),t._v(" "),a("li",[a("dl",[a("dt",[t._v("我的分润（元）")]),t._v(" "),a("dd",{class:s.royalty_amt.toString().length>=12?"fontS":""},[t._v("+"+t._s(t._f("yuan")(s.royalty_amt)))])])])])])])}))},staticRenderFns:[]};var i=a("VU/8")(o,_,!1,function(t){a("7zr6")},null,null);s.default=i.exports}});
//# sourceMappingURL=3.b4095b26b24a069b7c9f.js.map