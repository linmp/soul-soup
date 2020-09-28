import Card from '../../palette/card';

// src/pages/xml2can/xml2can.js
Page({
  imagePath: '',
  isSave: false,

  /**
   * 页面的初始数据
   */
  data: {
    template: {},
  },

  onImgOK(e) {
    this.imagePath = e.detail.path;
    this.setData({
      image: this.imagePath
    })
        console.log("分享")

    if (this.isSave) {
      this.saveImage(this.imagePath);
    }
  },

  saveImage(imagePath = '') {
    if (!this.isSave) {
      this.isSave = true;
      this.setData({
        paintPallette: this.data.template,
      });
    } else if (imagePath) {
      this.isSave = false;
      wx.saveImageToPhotosAlbum({
        filePath: imagePath,
      });
    }
  },

  // saveImage(imagePath = '') {
  //   if (!this.isSave) {
  //     this.isSave = true;
  //     this.setData({
  //       paintPallette: this.data.template,
  //     });
  //   } else if (imagePath) {
  //     this.isSave = false;
  //     qq.openQzonePublish({
  //       footnote: '干了这碗鸡汤',
  //       path: 'pages/soup/getSoup/index',
  //       // text: this.data.soupsData[this.data.index].content,
  //       text: "this.data.soupsData[this.data.index].content",

  //       media: [
  //         {
  //           type: 'photo',
  //           path: imagePath
  //         }
  //       ]
  //     })
  //   }
  // },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    var avatar = "https://hicaiji.com/avatar"
    var soupText = "内容在这里"
    this.setData({
      template: new Card().palette(avatar,soupText),
    });
  },
});
