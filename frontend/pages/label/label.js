const app = getApp()
Page({
  data:{
    albumName:'',
    checked:false,
    state:"",
    showID:"",
    inputValue:"",
    label:[],
    obtnArry:[
      {
        name:"信息学院",
        num:0,
        selected:false,
      },
      {
        name:"数学学院",
        num:1,
        selected:false,
      },
      {
        name:"环境学院",
        num:1,
        selected:false,
      },
      {
        name:"理学院",
        num:1,
        selected:false,
      },
      {
        name:"高瓴人工智能学院",
        num:1,
        selected:false,
      },
      {
        name:"经济学院",
        num:1,
        selected:false,
      },
      {
        name:"法学院",
        num:1,
        selected:false,
      },
      {
        name:"社会人口学院",
        num:1,
        selected:false,
      },
    ]
  },
// 选择标签并输入到label数组中
  dealTap:function(e){  
    let string = "obtnArry[" + e.target.dataset.index + "].selected";
    // const checkedicon = "obtnArry[" + e.target.dataset.index + "].selected"; 
    console.log(!this.data.obtnArry[e.target.dataset.index].selected);
    this.setData({
      [string]: !this.data.obtnArry[e.target.dataset.index].selected
    })
    let detailValue = this.data.obtnArry.filter(it => it.selected).map(it => it.name)
    this.setData({
      label: detailValue
    })
    console.log(this.data.label)
  },
  //返回用户数据
  comfirm:function(e){
    var util = require('../../utils/util.js'); //获取时间
    var m=app.globalData.userInfo  //获取全局向量
    wx.request({
      url: 'test.php', //访问地址
      data: {
        user_id: m['openId'],
        user_name:m['nickName'],
        user_tags:this.data.label,  //list
        user_create_time:util.formatTime(new Date())     //格式：2020/09/03 22:56:19
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res.data)
      }
    })
    //点击确定跳转index页面，navigateTo不能跳转tabbar page，因此使用switchTab
    wx.switchTab({
      url: '/pages/index/index',  
    })

  }

  
})
