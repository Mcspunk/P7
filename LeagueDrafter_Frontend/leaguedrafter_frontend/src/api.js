import axios from 'axios'
import router from './router'
import Vue from 'vue'

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
        postChampChoice: 'post/champChoice'
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