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
      Champions: []
    }
  },
  methods:{
    getChampions: function(){
        this.$http.get(this.$api.champions.getChampions)
        .then(response => {
            this.Champions = response.data;
            console.log(this.Champions);
        })
    },
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
    this.getChampions();
    this.filteredChampions = this.Champions;
  },
  mounted(){
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
