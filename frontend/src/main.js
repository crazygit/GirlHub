// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { InfiniteScroll, Lazyload, Toast, Spinner } from 'mint-ui'
import 'mint-ui/lib/style.css'
import axios from 'axios'
import VueAxios from 'vue-axios'

axios.defaults.timeout = 10000
axios.defaults.baseURL = 'http://localhost:8888/api/v1/'
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  console.log(error)
  Toast({
    message: '网络错误，请稍后再试!'
  })
  return Promise.reject(error)
})

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(InfiniteScroll)
Vue.use(Lazyload)
Vue.component(Spinner.name, Spinner)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
})
