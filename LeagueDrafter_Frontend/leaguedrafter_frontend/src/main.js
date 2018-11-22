// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import { api, apiRoutes, apiUrl } from './api'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default-dark.css' // This line here
import 'element-ui/lib/theme-chalk/index.css';
import { MdButton, MdTabs, MdIcon,MdSteppers } from 'vue-material/dist/components'
import { Loading } from 'element-ui'
Vue.use(MdButton)
Vue.use(VueMaterial)
Vue.use(MdTabs)
Vue.use(MdIcon)
Vue.use(Loading)
Vue.use(MdSteppers)
Vue.use(Vuex)
Vue.config.productionTip = false


Vue.prototype.$http = api
Vue.prototype.$api = apiRoutes
Vue.prototype.$apiUrl = apiUrl

const store = new Vuex.Store({
  state:{
    champions:[],
    filteredChampions:[],
    loading:true,
    activeStepper:'first',
    firstStep: false,
    secondStep: false,
    thirdStep: false
  },
  mutations:{
    setupChampions(state, payload){
      payload.forEach(champ => {
        champ = Object.assign({},champ,{
          picked:false
        })
        state.champions.push(champ)
      });
      state.filteredChampions = state.champions;
    },
    setLoading(state,payload){state.loading = payload},
    filterChampions(state,payload){
      var filteredChampions = []
      if(payload.tag === "all") filteredChampions = state.champions;
      else filteredChampions = state.champions.filter((champion) => champion.tags.toLowerCase().includes(payload.tag));
      filteredChampions = filteredChampions.filter((champion) => champion.name.toLowerCase().includes(payload.searchString.toLowerCase()));
      state.filteredChampions = filteredChampions;
    },
    greyScaleChampion(state,payload){
      var foundChamp = state.champions.find(champ => champ.newId === payload.index)
      foundChamp.picked = payload.value;
      var startIndex = state.filteredChampions.findIndex(champ => champ.newId === payload.index);
      state.filteredChampions.splice(startIndex,1,foundChamp)
    },
    setStepperDone (state,payload) {
      state[payload.id] = true

      if (payload.index) {
        state.activeStepper = payload.index
      }
    },
  },
  getters: {
    getChampionNames: state => {
      var champNames = [];
      state.champions.forEach(champ => {
        champNames.push(champ.name)
      });
      return champNames
    }
  },
  actions:{
    getChampions({commit}){
      Vue.prototype.$http.get(Vue.prototype.$api.champions.getChampions)
        .then(response => {
            commit('setupChampions',response.data);
            commit('setLoading',false);
        })
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>', 
})
