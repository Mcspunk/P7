<template>
  <div class="container">
    <div>
      <ChampSelectTopBar> </ChampSelectTopBar>
    </div>
    <div id="grid-container">
      <ChampSelectGrid> </ChampSelectGrid>
    </div> 
  </div>
</template>


<script>
import ChampSelectTopBar from './ChampSelectTopBar.vue'
import ChampSelectGrid from './ChampSelectGrid.vue'
import BanArea from './BanArea.vue'
export default {
  data(){
    return{
    }
  },
  methods:{
  },
  components:{
    'ChampSelectTopBar':ChampSelectTopBar,
    'ChampSelectGrid':ChampSelectGrid,
    BanArea
  }
}
</script>


<style lang="scss" scoped>
.container{
  position: relative;
  display:block;
}
#grid-container{
  overflow-y:scroll;
  height: 500px;
}
</style>
