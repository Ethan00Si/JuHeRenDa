// pages/demo/demo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    news_items:[
      { newsID:'1',title:'title_01', publish_date:'2020-08-26',source:'info'},
      { newsID:'2',title:'title_02', publish_date:'2020-08-27',source:'econ'},
      { newsID:'3',title:'title_03', publish_date:'2020-08-28',source:'news'},
      { newsID:'4',title:'title_04', publish_date:'2020-08-26',source:'law'},
      { newsID:'5',title:'title_05', publish_date:'2020-08-16',source:'finance'}
    ]
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 测试用的打印函数
    console.log('value is '+options.item)

    wx.request({
      url: 'http://127.0.0.1:8000/search',
      data: {
        key_word: options.item
      },
      success: res => {
        if (res.statusCode == 200) {
          console.log(res.data)
          this.setData({
            news_items: res.data
          })
        }
      }
    })

    console.log(this.data.news_items)

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  
  search: function () {

  }
})