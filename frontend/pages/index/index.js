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
      { newsID:'1',title:[{content: 'title', isLight: 1, entity: {'major': ['机器学习', '信息检索', '数据管理', '数据挖掘'], 'phone': '010-85203315', 'var': '文继荣', 'position': ['教授'], 'department': '信息学院', 'email': 'jirong.wen@gmail.com, jrwen@ruc.edu.cn', 'url': 'http://info.ruc.edu.cn/academic_professor.php?teacher_id=64','homepage':'https://www.baidu.com'} }, {content: '_1', isLight: 0}], publish_date:'2020-08-26',source:'info',url:'http://info.ruc.edu.cn/notice_detail.php?id=2066'},
      { newsID:'2',title:[{content: 'title', isLight: 1, entity: {'major': ['数据管理', '数据挖掘'], 'phone': '0203315', 'var': '文荣', 'position': ['助理教授'], 'department': '信息学院', 'email': 'jirong.wen@gmail.com, jrwen@ruc.edu.cn', 'url': 'http://info.ruc.edu.cn/academic_professor.php?teacher_id=64','homepage':'www.baidu.com'} }, {content: '_2', isLight: 0}], publish_date:'2020-08-27',source:'econ',url:'http://info.ruc.edu.cn/notice_convert_detail.php?id=2067'},
      { newsID:'3',title:[{content: 'title', isLight: 1}, {content: '_3', isLight: 0}], publish_date:'2020-08-28',source:'news',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1783'},
      { newsID:'4',title:[{content: 'title', isLight: 1}, {content: '_4', isLight: 0}], publish_date:'2020-08-26',source:'law',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1778'},
      { newsID:'5',title:[{content: 'title', isLight: 1}, {content: '_5', isLight: 0}], publish_date:'2020-08-16',source:'finance',url:'http://info.ruc.edu.cn/news_convert_detail.php?id=1779'}
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
    // this.onLoad()
    console.log('log_time')
  },
  viewDetail: function(e){
    var util = require('../../utils/util.js'); //获取时间
    var m=app.globalData.userInfo  //获取全局变量
    //传回用户日志
    let newsid = escape(e.currentTarget.dataset['newsid']);
    wx.request({
      url: 'http://127.0.0.1:8000/userlog/index', //仅为示例，并非真实的接口地址
      data: {
        user_id:m['openId'],
        art_id:newsid,
        behavior_time:util.formatTime(new Date())
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res.data)
      }
    })
    // var util = require('../../utils/util.js'); //获取时间
    // var m=app.globalData.userInfo  //获取全局变量
    // //传回用户日志
    // wx.request({
    //   url: 'test.php', //仅为示例，并非真实的接口地址
    //   data: {
    //     user_id:m['openId'],
    //     art_id:newsurl,
    //     behavior_time:util.formatTime(new Date())
    //   },
    //   header: {
    //     'content-type': 'application/json' // 默认值
    //   },
    //   success (res) {
    //     console.log(res.data)
    //   }
    // })
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
  viewUrl: function(e){
    let newsurl = escape(e.currentTarget.dataset['newsurl']);
    wx.navigateTo({
      url: '/pages/out/out?id='+newsurl ,
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {}
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
//   getUserInfo: function(e) {
//     console.log(e)
//     app.globalData.userInfo = e.detail.userInfo
//     this.setData({
//       userInfo: e.detail.userInfo,
//       hasUserInfo: true
//     })
//   }

  // 弹窗
  powerDrawer: function (e) {
    var currentStatu = e.currentTarget.dataset.statu;
    var entity = e.currentTarget.dataset.entity;
    this.util(currentStatu, entity)
  },
  util: function(currentStatu, entity){
    /* 动画部分 */
    // 第1步：创建动画实例 
    var animation = wx.createAnimation({
      duration: 200,  //动画时长
      timingFunction: "linear", //线性
      delay: 0  //0则不延迟
    });
    
    // 第2步：这个动画实例赋给当前的动画实例
    this.animation = animation;

    // 第3步：执行第一组动画
    animation.opacity(0).rotateX(-100).step();

    // 第4步：导出动画对象赋给数据对象储存
    this.setData({
      animationData: animation.export()
    })
    
    // 第5步：设置定时器到指定时候后，执行第二组动画
    setTimeout(function () {
      // 执行第二组动画
      animation.opacity(1).rotateX(0).step();
      // 给数据对象储存的第一组动画，更替为执行完第二组动画的动画对象
      this.setData({
        animationData: animation
      })
      
      //关闭
      if (currentStatu == "close") {
        this.setData(
          {
            showModalStatus: false
          }
        );
      }
    }.bind(this), 200)

    // 显示
    if (currentStatu == "open") {
      this.setData(
        {
          showModalStatus: true,
          entity_file: entity
        }
      );
    }
  }
 })
