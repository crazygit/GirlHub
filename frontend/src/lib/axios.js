import { Toast } from 'mint-ui'
import axios from 'axios'

var instance = axios.create({
  timeout: 1000,
  baseURL: process.env.BASE_URL
})

instance.defaults.headers.post['Content-Type'] = 'application/json'
instance.interceptors.response.use(function (response) {
  return response
}, function (error) {
  console.log(error)
  Toast({
    message: '网络错误，请稍后再试!'
  })
  return Promise.reject(error)
})

export default instance
