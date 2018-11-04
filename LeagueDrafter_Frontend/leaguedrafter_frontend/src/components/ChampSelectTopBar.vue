
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
      <md-field class="searchField"> 
      <label>Search</label>
      <md-input></md-input>
      <md-icon>search</md-icon>
    </md-field>

    </div>
  </div>  
</template>




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
    .searchField{
      margin-top:15px;
      overflow:hidden;
    }
  }
}

</style>