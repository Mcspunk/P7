<template>
  <div class="container-redPlayer">
    <h3>{{this.role}}</h3>
    <ChampionBox class="champBox" :champion="this.champion"> </ChampionBox>
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
.container-bluePlayer{
  position:relative;
  width:100%;
  float:left;
  h3{float:left}

  .champBox{
    float:right;
  }
}

.container-redPlayer{
  position:relative;
  width:100%;
  float:right;
  h3{float:right}

  .champBox{
    float:left;
  }
}



</style>