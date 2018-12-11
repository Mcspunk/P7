import axios from 'axios'
import router from './router'
import Vue from 'vue'

Vue.use(axios)

const apiUrl = 'http://backend.leaguedraft.gg/api'
//API routes
const apiRoutes = {
    base: (url) => {
        return `${apiUrl}${url}`
    },
    champions: {
        getChampions: 'get/champions/'
    },
    MCTS:{
        postCurrentState: 'post/currentState/'
    },
    sessions:{
        checkSession: 'get/checksession/',
        createSession: 'post/newsession/'
    },
    NN:{
        postFinalState: 'post/endresult/'
    }
}

const api = axios.create({
    baseURL: apiUrl,
    withCredentials:true,
    credentials:'same-origin'
})


export {
    apiUrl,
    apiRoutes,
    api
  }