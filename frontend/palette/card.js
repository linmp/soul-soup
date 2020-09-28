export default class LastMayday {
  palette(avatar,soupText) {
    return ({
      width: '650rpx',
      height: '750rpx',
      borderRadius: '30rpx',
      background: '#75b79e',
      views: [
        {
          type: 'image',
          url: avatar,
          css: {
            top: '40rpx',
            left: '40rpx',
            borderRadius: '60rpx',
            width: '120rpx',
            height: '120rpx',
          },
        },
        {
          id: 'text-id-2',
          type: 'text',
          text: soupText,
          css: [{
            top: '200rpx',
            align: 'center',
            width: '400rpx',
            textAlign: 'center',
            textAlign: 'left',
            padding: '20rpx',
            scalable: true,
            deletable: true,
          }, common,
           { left: '325rpx' }],
        },
        // {
        //   type: 'image',
        //   url: '/palette/励志鸡汤.png',
        //   css: {
        //     bottom: '40rpx',
        //     right: '40rpx',
        //     borderRadius: '30rpx',
        //     width: '160rpx',
        //     height: '160rpx',
        //   },
        // },
        {
          type: 'text',
          text: "长按识别小程序码",
          css: [{
            fontSize: '38rpx',
            left: '100rpx',
            bottom: '100rpx',
            width: '500rpx',
            maxLines: 1,
          }, 
        ],
        },
        {
          type: 'qrcode',
          content: 'https://m.q.qq.com/a/p/1110242745',
          css: {
            bottom: '40rpx',
            right: '40rpx',
            color: 'black',
            borderColor: 'white',
            borderRadius: '20rpx',
            borderWidth: '10rpx',
            width: '120rpx',
            height: '120rpx',
          },
        },
      ],
    });
  }
}

const common = {
  fontSize: '54rpx',
};
