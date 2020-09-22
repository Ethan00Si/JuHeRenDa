//app.js
App({
  onLaunch: function () {
    var that = this;
    //1、调用微信登录接口，获取code
    wx.login({
      success: function (r) {
        var code = r.code;//登录凭证
        if (code) {
          //2、调用获取用户信息接口
          wx.getUserInfo({
            success: function (res) {
              //3.请求自己的服务器，解密用户信息
              wx.request({
                url: 'http://127.0.0.1:8000/get_openid/index',
                method: 'post',
                header: {
                  'content-type': "application/x-www-form-urlencoded"
                },
                data: { encryptedData: res.encryptedData, iv: res.iv, code: code },
                success: function (res) {
                  console.log(res.data);
                  that.globalData.userInfo=res.data;
                },
                fail: function () {
                  console.log('系统错误')
                }
              })
            },
            fail: function () {
              console.log('获取用户信息失败')
            }
          })
        }
      } 
    })
  },    
    // var that = this;
    // //1、调用微信登录接口，获取code
    // wx.login({
    //   success: function (r) {
    //     var code = r.code;//登录凭证
    //     if (code) {
    //       //2、调用获取用户信息接口
    //       wx.getUserInfo({
    //         success: function (res) {
    //           //3.请求自己的服务器，解密用户信息
    //           wx.request({
    //             url: 'http://127.0.0.1:8000/app1/index',
    //             method: 'post',
    //             header: {
    //               'content-type': "application/x-www-form-urlencoded"
    //             },
    //             data: { encryptedData: res.encryptedData, iv: res.iv, code: code },
    //             success: function (res) {
    //               console.log(res.data);
    //               that.globalData.userInfo=res.data;
    //             },
    //             fail: function () {
    //               console.log('系统错误')
    //             }
    //           })
    //         },
    //         fail: function () {
    //           console.log('获取用户信息失败')
    //         }
    //       })
    //     } else {
    //       console.log('获取用户登录态失败！' + r.errMsg)
    //     }
    //   },
    //   fail: function () {
    //     console.log('登陆失败')
    //   }
    // })
  globalData: {
    userInfo: null
  },
})