import axios from 'axios'
import router from './router'
import Vue from 'vue'

Vue.use(axios)

const apiUrl = 'http://127.0.0.1:5000/api'

//API routes
const apiRoutes = {
    base: (url) => {
        return `${apiUrl}${url}`
    },
    champions: {
        getChampions: 'get/champions'
    },
    MCTS:{
        postCurrentState: 'post/currentState'
    }
}

const api = axios.create({
    baseURL: apiUrl
})


export {
    apiUrl,
    apiRoutes,
    api
  }