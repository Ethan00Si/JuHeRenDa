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
      { newsID:'1',title:'title_01', publish_date:'2020-08-26',source:'info'},
      { newsID:'2',title:'title_02', publish_date:'2020-08-27',source:'econ'},
      { newsID:'3',title:'title_03', publish_date:'2020-08-28',source:'news'},
      { newsID:'4',title:'title_04', publish_date:'2020-08-26',source:'law'},
      { newsID:'5',title:'title_05', publish_date:'2020-08-16',source:'finance'}
    ]
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
