<template>
  <div id="app">
    <NavigationTab> </NavigationTab>
    <router-view> </router-view>
  </div>
</template>


<script>
import NavigationTab from './components/NavigationTab.vue'
export default {
  name: 'App',
  components: {
    'NavigationTab': NavigationTab
  },
  methods:{
    getChampions: function(){
        this.$http.get(this.$api.champions.getChampions)
        .then(response => {
            this.$store.commit('setupChampions',response.data);
        })
    }
  },
  created(){
    this.getChampions();
  }  
}
</script>

<style lang="scss">
.Header{
  position:relative;
}

</style>

