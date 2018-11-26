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
  created(){
    this.$store.dispatch('getChampions')
  } 
}
</script>

<style lang="scss">
.Header{
  position:relative;
}

</style>

