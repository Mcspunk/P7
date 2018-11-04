<template>
  <div class="container">
    <div class="championGrid" v-for="(Champion,index) in this.Champions" :key="Champion.id">
      <ChampionBox :champion="Champion" class="championSlot"> </ChampionBox>
    </div>
  </div>
</template>

<script>
import ChampionBox from './ChampionBox.vue'
export default {
  props:['Champions'],
  data(){
    return{
      
    }
  },
  components:{
    'ChampionBox':ChampionBox
  }
}
</script>


<style lang="scss" scoped>
  .container{
    margin-left:25px
  }
  .championSlot{
    margin:5px;
    float:left;
  }
</style>
