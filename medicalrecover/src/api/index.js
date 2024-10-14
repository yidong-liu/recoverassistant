import request from '@/utils/request'

//注册
export const goRegister = (role, username, password, name) => request({ url: `/${role}/register`, method: 'post', data: { username, password, name } })

//登录
export const goLogin = (role, username, password) => request({ url: `${role}/login`, method: 'post', data: { username, password } })

//退出登陆
export const logOut = (role, username) => request({ url: `${role}/exit`, method: 'delete', data: { username } })

//得到用户信息
export const getUserInformation = (role) => request({ url: `${role}/getUser`, method: 'get' })

//修改密码
export const updatePassword = (role, username, password, newPassword) => request({ url: `${role}/changePassword`, method: 'put', data: { username, password, newPassword } })

//更新信息
export const updateInformation = (info, role) => {
  //console.log(info)
  const data = Object.entries(info)
    .filter(([key, value]) => (value !== '' || value !== null) && key !== 'address')
    .reduce((obj, [key, value]) => { obj[key] = value; return obj }, {})
  //console.log(data)
  return request({ url: `${role}/update`, method: 'patch', data: data })
}

//获得历史成绩
export const getHistory = () => request({ url: '/user/history', method: 'get' })

//测试题(完整句子)
export const uploadSentence = (sentence) => request({ url: '/user/sentence', method: 'post', data: { sentence } })

//上传音频
export const uploadAudio = (record1) => {
  //console.log(record1)
  if (!record1) {
    return
  }
  const formData = new FormData()
  formData.append('record1', record1, 'audio.mp3')
  formData.append('_record1', '祝出入平安')
  return request({ url: '/user/judge/audio', method: 'post', data: formData })
}

//上传图片
import dataURLtoBlob from '@/utils/translate'
export const uploadImage = async (canvasDataURL) => {
  let imageURL = '../assets/images/testImg.png'
  const response = await fetch(imageURL)
  const imageBlob = await response.blob()
  let formData = new FormData()
  formData.append('pic1', dataURLtoBlob(canvasDataURL), 'canvasImage.png') // 添加 Canvas 图片数据
  formData.append('_pic1', imageBlob, 'standard.png') // 添加 assets 图片数据
  return request({ url: '/user/judge/image', method: 'post', data: formData })
}

//上传视频
/* import compressAndUploadVideo from '@/utils/zip' */
export const uploadVideo = (videoBlob) => {
  //console.log(videoBlob)
  let formData = new FormData()
  formData.append('videoFile', videoBlob, 'recordedVideo.mp4')
  return request({
    url: '/user/judge/video',
    method: 'post',
    data: formData, // 使用 data 选项发送 FormData 对象
    headers: {
      'Content-Type': 'multipart/form-data' // 设置请求头为 multipart/form-data
    }
  })
}

//保存本次测试成绩
export const keepScore = (score = 0) => {
  //console.log(score)
  return request({ url: '/user/saveScore', method: 'post', data: { score } })
}

/* 获取医生诊断 */
export const getSituations = (uid) => request({ url: '/user/getSituations', method: 'get',query:{uid} })

/* 获取医生建议 */
export const getSuggestion = (uid) => request({ url: '/user/getSuggestions', method: 'get',query:{uid} })


/* 医生版块 */

/* 获取所有患者 */
export const getAllUsers = () => request({ url: '/doctor/getAllUsers', method: 'get' })

/* 添加诊治 */
export const setSituation = (id, treatSituation) => request({ url: '/doctor/setSituation', method: 'post', data: { userId: id, treatSituation } })

/* 添加意见建议 */
export const setSuggestion = (id, treatSuggestions) => request({ url: '/doctor/setSuggestion', method: 'post', data: { userId: id, suggestion:treatSuggestions } })

/* 添加我的患者 */
export const addMyPatient = (id) => request({ url: '/doctor/changeUserDoctor', method: 'patch', data: { id } })

/* 查看我的病人 */
export const getMyPatient = () => request({ url: '/doctor/getUsers', method: 'get' })

/* 查看病人测试分数 */
export const getPatientTestScore = (userId) => request({ url: '/doctor/getUserHistoryByUserId', method: 'get', params: { userId: userId } })

