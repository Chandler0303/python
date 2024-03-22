CryptoJS = require('./crypto-js')

// 秀动加密
const encrypt = function(word) {
  word = JSON.stringify(word)
  var encrypted = CryptoJS.AES.encrypt(word, CryptoJS.enc.Base64.parse('XjjkaLnlzAFbR399IP4kdQ=='), {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7,
      length: 128
  });
  return encrypted.toString()
}

const sign = function(data) {
  return CryptoJS.SHA1(data + 'QGZUanpSaSy9DEPQFVULJQ==').toString()
}

const decrypt = function(t) {
  var e = CryptoJS.enc.Utf8.parse('TheKeyOfmyDatadx')
  return CryptoJS.AES.decrypt(t, e, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
  }).toString(CryptoJS.enc.Utf8);
}
