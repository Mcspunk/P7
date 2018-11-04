<template>
  <div class="container">
    <ChampSelectTopBar> </ChampSelectTopBar>
    <ChampSelectGrid :Champions="this.Champions"> </ChampSelectGrid>
  </div>
</template>


<script>
import ChampSelectTopBar from './ChampSelectTopBar.vue'
import ChampSelectGrid from './ChampSelectGrid.vue'
export default {
  data(){
    return{
      selectedTag:"All",
      searchString:"",
      Champions: [
        {name:"Katarina", tags:"Mage;Assassin",imgPath:"kata.png"},
        {name:"Garen",tags:"Fighter;Tank",imgPath:"garen.png"},
        {name:"Thresh",tags:"Support",imgPath:"thresh.png"},
        {name:"Twitch",tags:"Jungle;Marksman",imgPath:"twitch.png"},
        {name:"Katarina", tags:"Mage;Assassin",imgPath:"kata.png"},
        {name:"Garen",tags:"Fighter;Tank",imgPath:"garen.png"},
        {name:"Thresh",tags:"Support",imgPath:"thresh.png"},
        {name:"Twitch",tags:"Jungle;Marksman",imgPath:"twitch.png"},
        {name:"Katarina", tags:"Mage;Assassin",imgPath:"kata.png"},
        {name:"Garen",tags:"Fighter;Tank",imgPath:"garen.png"},
        {name:"Thresh",tags:"Support",imgPath:"thresh.png"},
        {name:"Twitch",tags:"Jungle;Marksman",imgPath:"twitch.png"},
        {name:"Katarina", tags:"Mage;Assassin",imgPath:"kata.png"},
        {name:"Garen",tags:"Fighter;Tank",imgPath:"garen.png"},
        {name:"Thresh",tags:"Support",imgPath:"thresh.png"},
        {name:"Twitch",tags:"Jungle;Marksman",imgPath:"twitch.png"}
      ]
    }
  },
  components:{
    'ChampSelectTopBar':ChampSelectTopBar,
    'ChampSelectGrid':ChampSelectGrid
  }
}
</script>


<style lang="scss" scoped>
.container{
  position: relative;
  display:block;
}
</style>
