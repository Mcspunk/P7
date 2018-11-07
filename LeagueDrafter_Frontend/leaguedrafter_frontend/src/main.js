// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { api, apiRoutes, apiUrl } from './api'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default-dark.css' // This line here
import { MdButton, MdContent, MdTabs, MdIcon } from 'vue-material/dist/components'
Vue.use(MdButton)
Vue.use(VueMaterial)
Vue.use(MdContent)
Vue.use(MdTabs)
Vue.use(MdIcon)
Vue.config.productionTip = false


Vue.prototype.$http = api
Vue.prototype.$api = apiRoutes
Vue.prototype.$apiUrl = apiUrl

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
