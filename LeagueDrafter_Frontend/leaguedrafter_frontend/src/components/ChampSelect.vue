<template>
  <div class="container">
    <div>
      <ChampSelectTopBar> </ChampSelectTopBar>
    </div>
    <div id="grid-container">
      <ChampSelectGrid> </ChampSelectGrid>
    </div>
      <md-button id="lock-btn" class="md-raised md-primary" @click="changeTurn" v-if="this.$store.state.allyTurn != null" :disabled="!getValidState">Lock In</md-button>
  </div>
</template>


<script>
import ChampSelectTopBar from './ChampSelectTopBar.vue'
import ChampSelectGrid from './ChampSelectGrid.vue'
export default {
  data(){
    return{
    }
  },
  methods:{
    changeTurn(){
      this.$store.commit('changeTurn')
    }
  },
  components:{
    'ChampSelectTopBar':ChampSelectTopBar,
    'ChampSelectGrid':ChampSelectGrid,
  },
  computed:{
    getValidState(){
      return this.$store.getters.validState
    }
  }
}
</script>


<style lang="scss" scoped>
.container{
  position: relative;
  display:block;
}
#grid-container{
  background-color: rgb(35, 35, 36);
  height: 500px;
}
#lock-btn{
  margin-left:40%;
  width:20%;
  height:75px;

}
</style>
