<template>
  <div class="container">
      <div class="roleText">{{this.role}}</div>
      <ChampionBox :class="this.displaySetting" :champion="this.pvChamp" id="champBox"> </ChampionBox>
  </div>
</template>

<script>
import ChampionBox from "./ChampionBox.vue"
export default {
  name: "PlayerSlot",
  props: ["champion","role","displaySetting"],
  data (){
    return{
    }
  },
  methods:{
  },
  components:{
    'ChampionBox' : ChampionBox
  },
  computed:{
    pvChamp: function () {
      // `this` points to the vm instance
      return this.champion
    }
  }
}
</script>

<style lang="scss" scoped>

.container{
  position:relative;
  width:100%;
  display:block;
  .roleText{
    text-align: center;
    font-size: 20px;
  }
}

.outerShadow{
  box-shadow: 0px 1px 10px rgba(255, 255, 255, 0.719);
}

#champBox{
  width: 75px;
  height: 75px;
}
</style>