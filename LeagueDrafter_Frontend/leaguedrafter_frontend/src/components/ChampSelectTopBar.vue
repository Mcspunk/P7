
<template>
  <div class="container">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <div class="categoryTabs">
      <md-tabs md-alignment="left" @md-changed="tabChanged">
        <md-tab id="tab-all" md-label="All" md-icon="verified_user"></md-tab>
        <md-tab id="tab-fighter" md-label="Fighter" md-icon="verified_user"></md-tab>
        <md-tab id="tab-tank" md-label="Tank" md-icon="verified_user"></md-tab>
        <md-tab id="tab-support" md-label="Support" md-icon="verified_user"></md-tab>
        <md-tab id="tab-mage" md-label="Mage" md-icon="verified_user"></md-tab>
        <md-tab id="tab-assassin" md-label="Assassin" md-icon="verified_user"></md-tab>
        <md-tab id="tab-marksman" md-label="Marksman" md-icon="verified_user"></md-tab>
      </md-tabs>
    </div>
    <div class="searchBar">
      <md-autocomplete id="searchField" v-model="searchTerm" :md-options="this.ChampionNames" :md-open-on-focus="false" @md-changed="searchChanged">
      <label>Search</label>
      </md-autocomplete>
      <template slot="md-autocomplete-item" slot-scope="{ item, term }"> ... </template>
    </div>
  </div>  
</template>

<script>
export default {
  props:['Champions'],
  data(){
    return{
      searchTerm:"",
      currentTag:"",
      matchedChamps:[]
    }
  },
  methods:{
    tabChanged:function(id){
      this.currentTag = id.split('-')[1];
      this.$parent.filterChampions(this.currentTag,this.searchTerm.toLowerCase());
    },
    searchChanged:function(){
      this.$parent.filterChampions(this.currentTag,this.searchTerm.toLowerCase());
    }
  },
  computed:{
    ChampionNames(){
      var champNames = [];
      this.Champions.forEach(champion => {
        champNames.push(champion.name);
      });
      return champNames;
    }
  }
}
</script>





<style lang="scss" scoped>
.container{
  position:relative;
  display:block;
  width:100%;
  height: 100%;
  overflow:hidden;
  background-color: rgb(66, 66, 66);
  .categoryTabs{
    position:relative;
    width:65%;
    float:left;
    overflow:hidden;
  }
  .searchBar{
    position: relative;
    width: 25%;
    float:right;
    overflow:hidden;
    margin-right:10px;
    background-color: rgb(66, 66, 66);
  }
}

</style>