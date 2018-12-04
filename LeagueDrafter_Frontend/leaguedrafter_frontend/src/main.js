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
import { MdButton, MdTabs, MdIcon, MdSteppers } from 'vue-material/dist/components'
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

var postOptions = {
  withCredentials:true,
  credentials:'same-origin'
}

const store = new Vuex.Store({
  state:{
    champions:[],
    filteredChampions:[],
    bannedChampions:[],
    allyTeam:[],
    enemyTeam:[],
    suggestedChampions:[],
    loading:true,
    activeStepper:'first',
    ally_starting:false,
    firstStep: false,
    secondStep: false,
    thirdStep: false,
    allyTurn:null,
    activeTab:"tab-all"
  },
  mutations:{
    changeTurn(state){
      state.allyTurn = !state.allyTurn
      if(state.allyTurn){
        state.activeTab ="tab-suggestion"
        store.commit('sendState')
      } 
      else{
        state.activeTab = "tab-all"
      } 
    },
    isAllyStarting(state,payload){
      state.ally_starting = payload.value
    },
    sendState(state){
      Vue.prototype.$http.post(Vue.prototype.$api.MCTS.postCurrentState, store.getters.getCurrentState)
      .then(response =>{
        console.log(response)
      })
    },
    gotoPickPhase(state){
      state.allyTurn = state.ally_starting;
      if(state.ally_starting){
        state.activeTab = "tab-suggestion"
        store.commit('sendState')
      } 
    },
    addToTeam(state,payload){
      state[payload.team].push(payload.champion)
    },
    removeFromTeam(state,payload){
      var startIndex = state[payload.team].findIndex(champ => champ.newId === payload.champion.newId);
      state[payload.team].splice(startIndex,1)
      console.log(state.allyTeam);
      console.log(state.enemyTeam);
    },
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
    banChampions(state,payload){
      payload.champions.forEach(champ => {
        state.bannedChampions.push(champ.champion)
      });
    }
  },
  getters: {
    getChampionNames: state => {
      var champNames = [];
      state.champions.forEach(champ => {
        champNames.push(champ.name)
      });
      return champNames
    },
    getBannedChampionCount: state => {
      return state.bannedChampions.length
    },
    getCurrentState: state => {
      return {
        ally_starting:state.ally_starting,
        ally_team:state.allyTeam.map(x => x.newId),
        enemy_team:state.enemyTeam.map(x => x.newId),
        banned_champs:state.bannedChampions.map(x => x.newId)
      }
    },
    validState: state => {
      if(state.ally_starting && state.allyTurn && (state.allyTeam.length - state.enemyTeam.length) === 1 ) return true;
      if(state.ally_starting && !state.allyTurn && (state.enemyTeam.length - state.allyTeam.length) === 1) return true;
      if(!state.ally_starting && state.allyTurn && (state.allyTeam.length - state.enemyTeam.length) === 1) return true;
      if(!state.ally_starting && !state.allyTurn && (state.enemyTeam.length - state.allyTeam.length) === 1 ) return true;
      if(state.allyTeam.length === 5 && state.enemyTeam.length === 5) return true;
      return false; 

    }
  },
  actions:{
    getChampions({commit}){
      Vue.prototype.$http.get(Vue.prototype.$api.champions.getChampions)
        .then(response => {
            commit('setupChampions',response.data);
            commit('setLoading',false);
        })
    },
    createSession({commit}){
      var cookieFound = false
      Vue.prototype.$http.get(Vue.prototype.$api.sessions.checkSession)
        .then(response => {
          if(response.status === 200) cookieFound = true;
        })
      if(!cookieFound){
        Vue.prototype.$http.post(Vue.prototype.$api.sessions.createSession)
        .then(response => {
          if(response.status === 200) cookieFound = true;
        })
      }
      if(!cookieFound) console.log("Session not created correctly in backend")
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
