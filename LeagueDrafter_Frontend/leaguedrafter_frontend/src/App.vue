<template>
  <div id="app">
    <HeaderBar class="Header"> </HeaderBar>
    <router-view> </router-view>
  </div>
</template>


<script>
import HeaderBar from './components/HeaderBar.vue'
export default {
  name: 'App',
  components: {
    'HeaderBar': HeaderBar
  }
  
}
</script>

<style lang="scss">
.Header{
  position:relative;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  }
</style>

