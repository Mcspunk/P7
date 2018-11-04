<template>
  <div class="container-redPlayer">
      <div class="roleText md-body2">{{this.role}}</div>
      <ChampionBox :champion="this.champion" class="champBox"> </ChampionBox>
  </div>
</template>

<script>
import ChampionBox from "./ChampionBox.vue"
export default {
  name: "PlayerSlot",
  props: ["champion","role","floatRole"],
  date (){
    return{
    }
  },
  components:{
    'ChampionBox' : ChampionBox
  }
}
</script>

<style lang="scss" scoped>

.container-redPlayer{
  position:relative;
  width:75%;
  float: left;
  h3{float: inherit;}

  .champBox{
    
    float:left;
  }
}



</style>