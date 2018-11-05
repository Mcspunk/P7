<template>
  <div class="container">
    <ChampSelectTopBar :Champions="this.Champions"> </ChampSelectTopBar>
    <ChampSelectGrid :Champions="this.filteredChampions"> </ChampSelectGrid>
  </div>
</template>


<script>
import ChampSelectTopBar from './ChampSelectTopBar.vue'
import ChampSelectGrid from './ChampSelectGrid.vue'
export default {
  data(){
    return{
      filteredChampions:[],
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
  methods:{
    filterChampions:function(tag,searchString){
      if(tag === "all") this.filteredChampions = this.Champions;
      else this.filteredChampions = this.Champions.filter((champion) => champion.tags.toLowerCase().includes(tag));
      this.filteredChampions = this.filteredChampions.filter((champion) => champion.name.toLowerCase().includes(searchString.toLowerCase()));
    }
  },
  components:{
    'ChampSelectTopBar':ChampSelectTopBar,
    'ChampSelectGrid':ChampSelectGrid
  },
  created(){
    this.filteredChampions = this.Champions;
  }
}
</script>


<style lang="scss" scoped>
.container{
  position: relative;
  display:block;
}
</style>
