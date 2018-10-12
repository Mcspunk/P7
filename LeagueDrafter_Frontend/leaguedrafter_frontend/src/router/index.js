import Vue from 'vue'
import Router from 'vue-router'
import FrontPage from '@/components/FrontPage'
import About from '@/components/About'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'FrontPage',
      component: FrontPage
    },
    {
      path: '/About',
      name: 'About',
      component: About
    }
  ]
})
