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
  }
  
}
</script>

<style lang="scss">
.Header{
  position:relative;
}

</style>

