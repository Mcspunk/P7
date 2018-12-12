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
import { MdButton, MdTabs, MdIcon, MdSteppers, MdTooltip } from 'vue-material/dist/components'
import { Loading } from 'element-ui'
Vue.use(MdButton)
Vue.use(VueMaterial)
Vue.use(MdTabs)
Vue.use(MdIcon)
Vue.use(MdTooltip)
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

var applyDrag = function(arr, dragResult,index) {
  const { removedIndex, addedIndex, payload } = dragResult;
  if (removedIndex === null && addedIndex === null) return arr;

  const result = [...arr];
  let itemToAdd = payload;

  if (removedIndex !== null) {
    itemToAdd = result.splice(removedIndex, 1)[0];
  }

  if (addedIndex !== null) {
    if(result[index].champion.newId >= 0)  store.commit('greyScaleChampion',{index:result[index].champion.newId,value:false})
    store.commit('greyScaleChampion',{index:itemToAdd.newId,value:true})
    if(store.state.allyTurn != null) store.commit('addToTeam',{champion:itemToAdd,team:store.state.allyTurn? "allyTeam":"enemyTeam"})
    result[index].champion=itemToAdd;
  }

  return result;
}


const store = new Vuex.Store({
  state:{
    champions:[],
    banPlaceholders:[],
    allyPlaceholders:[],
    enemyPlaceholders:[],
    filteredChampions:[],
    bannedChampions:[],
    allyTeam:[],
    enemyTeam:[],
    suggestedChampions:[],
    roles:["Top","Jungle","Mid","Bot","Support"],
    loading:true,
    activeStepper:'first',
    allyWinChance:"",
    ally_starting:false,
    firstStep: false,
    secondStep: false,
    thirdStep: false,
    allyTurn:null,
    activeTab:"tab-all",
    loadSuggestions:false,
    progressCounter:0
  },
  mutations:{
    changeTab(state,payload){
      state.activeTab = payload.newTabName
    },
    championBanned(state,payload){
      state.banPlaceholders = applyDrag(state.banPlaceholders,payload.dropresult,payload.placeHolderIndex)
    },
    championChosen(state,payload){
      state[payload.placeholderName] = applyDrag(state[payload.placeholderName],payload.dropresult,payload.placeHolderIndex)

    },
    changeTurn(state){
      if(state.allyTeam.length === 5 && state.enemyTeam.length === 5){
        store.commit('setStepperDone',{id:'thirdStep', index:'fourth'});
        store.commit('sendFinalState');
        window.scrollY(0);
      }
      else{
        state.allyTurn = !state.allyTurn
        if(state.allyTurn){
          state.activeTab ="tab-suggestion"
          store.commit('sendState')
        } 
        else{
          state.suggestedChampions = []
          state.activeTab = "tab-all"
        } 
      }
    },
    sendFinalState(state){
      Vue.prototype.$http.post(Vue.prototype.$api.NN.postFinalState, store.getters.getCurrentState)
      .then(response =>{
        state.allyWinChance = (Math.round((response.data)*10)/10).toFixed(1)
      })
    },
    isAllyStarting(state,payload){
      state.ally_starting = payload.value
    },
    sendState(state){
      var intervalID = window.setInterval(updateLoading, 100);

      function updateLoading() {
        state.progressCounter = state.progressCounter += 1
        if(state.progressCounter === 100){
          window.clearInterval(intervalID)
        }
      }
      Vue.prototype.$http.post(Vue.prototype.$api.MCTS.postCurrentState, store.getters.getCurrentState)
      .then(response =>{
        if(response.status === 200){
          var suggChamps = []
          response.data.forEach(element => {
            var newElement = {
              champ1:null,
              champ2:null,
              score:null
            };
            newElement.champ1 = state.champions.find(champ => champ.newId === element[0])
            if(element[1] != null){
              newElement.champ2 = state.champions.find(champ => champ.newId === element[1])
            }
            newElement.score = (Math.round((element[2]*100)*10)/10).toFixed(1);
            console.log(newElement)
            suggChamps.push(newElement)
          });
          state.suggestedChampions = suggChamps
          state.loadSuggestions = false;
          store.commit('filterChampions',{tag:"suggestion",searchString:""})
        }
        else if(response.status === 204){
          store.dispatch("createSession");
          store.commit("sendState");
        }
        state.activeTab = "tab-suggestion"
      })
      
      state.progressCounter = 0;
    },
    gotoPickPhase(state){
      state.allyTurn = state.ally_starting;
      if(state.ally_starting){
        state.activeTab = "tab-suggestion"
        store.commit('sendState')
      }
      store.dispatch('createSession')
    },
    addToTeam(state,payload){
      state[payload.team].push(payload.champion)
    },
    removeFromTeam(state,payload){
      var startIndex = state[payload.team].findIndex(champ => champ.newId === payload.champion.newId);
      state[payload.team].splice(startIndex,1)
    },
    setupChampions(state, payload){
      payload.forEach(champ => {
        champ = Object.assign({},champ,{
          picked:false,
          banned:false,
          locked:false,
        })
        state.champions.push(champ)
      });
      state.filteredChampions = state.champions;

      for (let index = 0; index < 10; index++) {
        state.banPlaceholders.push({
          id: index,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Ban",
            newId:-1,
            tags:"Ban"
          },
          role: "Ban"
        })        
      }
      for (let index = 0; index < 5; index++) {
        var newRole = state.roles[index]
        state.allyPlaceholders.push({
          id:index,
          champion:{
            orgId:-1,
            imgPath:newRole+"_icon.png",
            name:newRole,
            newId:-1,
            tags:newRole
          },
          role:newRole
        })
      }
      for (let index = 0; index < 5; index++) {
        var newRole = state.roles[index]
        state.enemyPlaceholders.push({
          id:index,
          champion:{
            orgId:-1,
            imgPath:newRole+"_icon.png",
            name:newRole,
            newId:-1,
            tags:newRole
          },
          role:newRole
        })
      }
    },
    setLoading(state,payload){state.loading = payload},
    filterChampions(state,payload){
      var filteredChampions = []
      if(payload.tag === "all") filteredChampions = state.champions;
      else if(payload.tag ==='suggestion'){
        if(state.suggestedChampions.length === 0) state.loadSuggestions = true;
        payload.searchString = "";
        state.suggestedChampions.forEach(element => {
          filteredChampions.push(element.champ1)
          if(element.champ2 != null) filteredChampions.push(element.champ2)
        });
      } 
      else filteredChampions = state.champions.filter((champion) => champion.tags.toLowerCase().includes(payload.tag));
      filteredChampions = filteredChampions.filter((champion) => champion.name.toLowerCase().includes(payload.searchString.toLowerCase()));
      state.filteredChampions = filteredChampions;
    },
    greyScaleChampion(state,payload){
      var foundChamp = state.champions.find(champ => champ.newId === payload.index)
      foundChamp.banned = payload.value;
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
    getProgressText: state => {
      if(state.progressCounter === 100) return "Retrieving suggestions, please hold on"
      return "Calculating Suggestions: " + state.progressCounter + "%"
    },
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
      console.log(state.allyTeam)
      console.log(state.enemyTeam)
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
