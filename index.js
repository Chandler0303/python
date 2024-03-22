
md5 = require('./md5')
CryptoJS = require('./crypto-js')

const Cdeviceinfo = encodeURI(JSON.stringify({
  vendorName: '', //uni.getSystemInfoSync().deviceBrand || ""
  deviceMode: 'SM-G955U', //uni.getSystemInfoSync().deviceModel || "",
  deviceName: "",
  systemName: 'android', //uni.getSystemInfoSync().osName || "",
  systemVersion: '8.0.0',//uni.getSystemInfoSync().osVersion || "",
  cpuMode: " ",
  cpuCores: "",
  cpuArch: "",
  memerySize: "",
  diskSize: "",
  network: 'UNKNOWN',
  resolution: '412*914', //uni.getSystemInfoSync().screenWidth + "*" + uni.getSystemInfoSync().screenHeight,
  pixelResolution: ""
}))

// 设置uuid: e：随机长度
const uuid = function(e) {
  for (var n = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + (new Date).getTime(), a = e || 20, t = [], i = 0; i < a; i++) {
    t.push(n.charAt(Math.floor(Math.random() * n.length)));
  }
  return t.join("")
}
// 时间长uid
const timeUuid = function(e){
  return uuid(e) + (new Date().getTime())
}
const setKey = function(headers = {}){ 
  let k = ''
  let t = headers.timeUuid.toString()
  let p = headers.token.toString()
  const list = [2, 11, 22, 23, 29, 30, 33, 36]
  const list2 = [1, 7, 8, 12, 15, 18, 19, 28]
  list.map(e => {
    k += t.charAt(e - 1)
  })
  list2.map(e => {
    k += p.charAt(e - 1)
  })
  return {
    k,
    t,
    p
  }
}
// 秀动加密
const encrypt = function(word, key) {
  key = key || '0RGF99CtUajPF0Ny';
  word = JSON.stringify(word)
  var a = CryptoJS.enc.Base64
  var srcs  = CryptoJS.enc.Utf8.parse(word)
  var new_key = CryptoJS.enc.Utf8.parse(key)
  var encrypted = CryptoJS.AES.encrypt(srcs, new_key, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
  });
  return a.stringify(encrypted.ciphertext)
}

const decrypt = function(e, n) {
  n = n || '0RGF99CtUajPF0Ny';
  var a = CryptoJS.enc.Utf8.parse(n)
    , t = CryptoJS.AES.decrypt(e, a, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
  });
  return CryptoJS.enc.Utf8.stringify(t).toString()
}




const getHeaders = function({
  st_flpv,
  sign,
  url,
  token,
  userId,
  idToken,
  timeUuid,
  accessToken = ''
}, requestData) {
  // const uuidVal = uuid(32).toLowerCase()
  const CRTRACEID = timeUuid
  const a = accessToken || '' // accessToken || ''
  const t = url === '/waf/gettoken' ? '' : sign // sign || ''
  const i = url === '/waf/gettoken' ? '' : idToken // idToken || ''
  const s = url === '/waf/gettoken' ? '' : userId // userInfo.userId || ''
  const _ = token // token || uuid(32).toLowerCase()
  const E = requestData ? JSON.stringify(requestData) : '' // n.data ? JSON.stringify(n.data) : ""
  const requestUrl = url//'/waf/gettoken' // n.url
  const v = CRTRACEID // uuid(32) + (new Date).getTime()
  const f = 'wap' // 'wap'
  const version = '997'
  const crpsing = a + t + i + s + f + _ + E + requestUrl + version + f + v
  return {
      'CDEVICEINFO': '', // Cdeviceinfo,
      'CRPSIGN': md5(crpsing),
      'CRTRACEID': CRTRACEID,
      'CSAPPID': f,
      'CSOURCEPATH':"",
      'CTERMINAL': f,
      'CTRACKPATH':"",
      'CUSAT': a || 'nil', // accessToken || 'nil'
      'CUSID': s || 'nil', // userId || "nil",
      'CUSIT': i || "nil", // idToken || "nil",
      'CUSNAME':"nil",
      'CUSUT': t || "nil", // sign || "nil",
      'CDEVICENO': _, // token || uuid(32).toLowerCase()
      'CUUSERREF': _, // token || uuid(32).toLowerCase()
      'CVERSION': version,
      'St_flpv': st_flpv
  }
}

// const st_flpv = uuid()
// const token = uuid(32).toLowerCase()