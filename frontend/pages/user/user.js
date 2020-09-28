
const app = getApp();
var Api = require('../../utils/api.js');
Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    count: null
  },

  exit: function () {
    this.setData({
      hasUserInfo: false,
      userInfo: {},
      canIUse: wx.canIUse('button.open-type.getUserInfo')
    })
  },




  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
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
    // if (app.globalData.userInfo) {
    //   console.log("进入")
    //   updateuser(app.globalData.userInfo, app.globalData.openid)
    // }
  },

  getUserInfo: function (e) {
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
    wx.reLaunch({
      url: '/pages/user/user'
    })
  },



  onShow() {
    var that = this;
  },

  // 单击双击
  mytap: function (e) {
    console.log('成功点击');
    wx.showModal({
      title: '成功点击',
      content: '成功点击',
      showCancel: false,
    })
  },

  showQrcode() {
    wx.previewImage({
      urls: ['https://cdn.jamkung.com/card/user/1/202007/23/140522_25.png'],
      current: 'https://cdn.jamkung.com/card/user/1/202007/23/140522_25.png' // 当前显示图片的http链接      
    })
  },

  /**
 * 分享网页
 */
  onShareAppMessage: function () {
    return {
      title: '鸡汤鸡汤',
      desc: '鸡汤一时爽，一直鸡汤一直爽',
      path: '/pages/soup/getSoup/index'
    }
  },

})

function updateuser(user, openid) {
  var username = user.nickName;
  var avatar = user.avatarUrl;
  console.log("更新用户信息")
  wx.request({
    url: Api.update(),
    data: {
      openid: openid,
      username: username,
      avatar: avatar
    },
    header: {
      'content-type': 'application/json'
    },
    method: 'POST',
    success(res) {
      console.log(res.data);
    }
  })

}