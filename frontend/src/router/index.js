import Vue from 'vue'
import Router from 'vue-router'
import Girl from '@/components/Girl'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'girl',
      component: Girl
    }
  ]
})
