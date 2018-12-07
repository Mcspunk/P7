
<template>
  <div class="container">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <div class="categoryTabs">
      <md-tabs md-alignment="left" @md-changed="tabChanged" :md-active-tab="this.activeTab">
        <md-tab v-if="this.allyTurn" id="tab-suggestion" md-label="Suggestions" md-icon="verified_user"></md-tab>
        <md-tab id="tab-all" md-label="All" md-icon="verified_user"></md-tab>
        <md-tab id="tab-fighter" md-label="Fighter" md-icon="verified_user"></md-tab>
        <md-tab id="tab-tank" md-label="Tank" md-icon="verified_user"></md-tab>
        <md-tab id="tab-support" md-label="Support" md-icon="verified_user"></md-tab>
        <md-tab id="tab-mage" md-label="Mage" md-icon="verified_user"></md-tab>
        <md-tab id="tab-assassin" md-label="Assassin" md-icon="verified_user"></md-tab>
        <md-tab id="tab-marksman" md-label="Marksman" md-icon="verified_user"></md-tab>
      </md-tabs>
    </div>
    <div v-if="activeTab != 'tab-suggestion' " class="searchBar">
      <md-autocomplete id="searchField" v-model="searchTerm" :md-options="this.championNames" :md-open-on-focus="false" @md-changed="searchChanged">
      <label>Search</label>
      </md-autocomplete>
      <template slot="md-autocomplete-item" slot-scope="{ item, term }"> ... </template>
    </div>
  </div>  
</template>

<script>
export default {
  data(){
    return{
      searchTerm:"",
      currentTag:"",

    }
  },
  methods:{
    tabChanged:function(id){
      this.$store.commit('changeTab',{newTabName:id})
      this.currentTag = id.split('-')[1];
      this.$store.commit('filterChampions',{tag:this.currentTag,searchString:this.searchTerm});
    },
    searchChanged:function(){
      this.$store.commit('filterChampions',{tag:this.currentTag,searchString:this.searchTerm});
    }
  },
  computed:{
    champions(){
      return this.$store.state.champions
    },
    championNames(){
      return this.$store.getters.getChampionNames
    },
    allyTurn(){
      return this.$store.state.allyTurn
    },
    activeTab(){
      return this.$store.state.activeTab
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