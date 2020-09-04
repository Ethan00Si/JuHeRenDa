//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    headerTitleName: [
      { name: '热门', nameID: '201701', newsType: 'top' },
      { name: '信息', nameID: '201701', newsType: 'info' },
      { name: '财金', nameID: '201702', newsType: 'finance' },
      { name: '经济', nameID: '201703', newsType: 'economy' },
      { name: '数学', nameID: '201704', newsType: 'math' }
    ],
    swiperIndex: '1/4',
    topPic: [],
    tapID: 201701, // 判断是否选中
    contentNewsList: [],
    showCopyright: false,
    refreshing: false,
    news_items:[
      { newsID:'1',title:'title_01', publish_date:'2020-08-26',source:'info',url:'http://info.ruc.edu.cn/notice_detail.php?id=2066'},
      { newsID:'2',title:'title_02', publish_date:'2020-08-27',source:'econ',url:'http://info.ruc.edu.cn/notice_convert_detail.php?id=2067'},
      { newsID:'3',title:'title_03', publish_date:'2020-08-28',source:'news',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1783'},
      { newsID:'4',title:'title_04', publish_date:'2020-08-26',source:'law',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1778'},
      { newsID:'5',title:'title_05', publish_date:'2020-08-16',source:'finance',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1779'}
    ]
  },
  onPullDownRefresh: function(){
    let user_id = '1'
    wx.request({
      url: 'http://127.0.0.1:8000/recommender/'+user_id,
      data: {},
      // header: {'content-type':'application/json'},
      // method: 'GET',
      // dataType: 'json',
      // responseType: 'text',
      success: res =>{
        if (res.statusCode == 200){
          this.setData({
            news_items: res.data
          })
        }
      },
      fail: ()=>{},
      complete: ()=>{}
    });
    wx.stopPullDownRefresh({
      success: (res) => {},
    })
  },
  viewDetail: function(e){
    var util = require('../../utils/util.js'); //获取时间
    var m=app.globalData.userInfo  //获取全局变量
    //传回用户日志
    wx.request({
      url: 'test.php', //仅为示例，并非真实的接口地址
      data: {
        user_id:m['openId'],
        art_id:newsurl,
        behavior_time:util.formatTime(new Date())
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res.data)
      }
    })

    let newsurl = escape(e.currentTarget.dataset['newsurl']);
    wx.navigateTo({
      url: '/pages/out/out?id='+newsurl ,
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {}
    })
  },
  //事件处理函数
//   bindViewTap: function() {
//     wx.navigateTo({
//       url: '../logs/logs'
//     })
//   },
//   onLoad: function () {
//     if (app.globalData.userInfo) {
//       this.setData({
//         userInfo: app.globalData.userInfo,
//         hasUserInfo: true
//       })
//     } else if (this.data.canIUse){
//       // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
//       // 所以此处加入 callback 以防止这种情况
//       app.userInfoReadyCallback = res => {
//         this.setData({
//           userInfo: res.userInfo,
//           hasUserInfo: true
//         })
//       }
//     } else {
//       // 在没有 open-type=getUserInfo 版本的兼容处理
//       wx.getUserInfo({
//         success: res => {
//           app.globalData.userInfo = res.userInfo
//           this.setData({
//             userInfo: res.userInfo,
//             hasUserInfo: true
//           })
//         }
//       })
//     }
//   },
//   getUserInfo: function(e) {
//     console.log(e)
//     app.globalData.userInfo = e.detail.userInfo
//     this.setData({
//       userInfo: e.detail.userInfo,
//       hasUserInfo: true
//     })
//   }
 })
