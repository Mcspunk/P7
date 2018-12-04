<template>
<VuePerfectScrollbar class="test">
  <div id="app">
    <router-view> </router-view>

  </div>
</VuePerfectScrollbar>

</template>


<script>
import NavigationTab from './components/NavigationTab.vue'
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
export default {
  name: 'App',
  components: {
    'NavigationTab': NavigationTab, VuePerfectScrollbar
  },
  created(){
    this.$store.dispatch('createSession')
    this.$store.dispatch('getChampions')
  } 
}
</script>

<style lang="scss">
.Header{
  position:relative;
}

.test{
  height:100%;
}

body   {
position: absolute;
top: 0;
left: 0;
bottom: 0;
right: 0px;
overflow-y: hidden;
overflow-x: hidden;
}


</style>

