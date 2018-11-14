<template>
  <div class="container-redPlayer">
      <div class="roleText">{{this.role}}</div>
        <ChampionBox :champion="this.pvChamp" id="champBox"> </ChampionBox>
  </div>
</template>

<script>
import ChampionBox from "./ChampionBox.vue"
export default {
  name: "PlayerSlot",
  props: ["champion","role","floatRole"],
  data (){
    return{
      pvChamp: this.champion
    }
  },
  methods:{
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

  #champBox{
    float:left;
  }
}



</style>