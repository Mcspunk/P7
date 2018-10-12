<template>
  <div class="container">
    <ul>
      <li><PlayerSlot :champion="this.champ1" :role="'Top'" :floatRole="this.blueTeam"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.champ1" :role="'Jungle'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.champ1" :role="'Mid'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.champ1" :role="'Bottom'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.champ1" :role="'Support'"></PlayerSlot></li>
    </ul>
  </div>
</template>

<script>
import PlayerSlot from './PlayerSlot.vue'
export default {
  props:["blueTeam"],
  name:"Team",
  data () {
    return {
        champ1:{
          id:1,
          imgPath:"kata.png"
        }
    }
  },
  components:{
    'PlayerSlot' : PlayerSlot
  }
}
</script>

<style lang="scss" scoped>
.container{
  display:inline-block;
  width:100%;
}
ul{
  list-style-type:none;
  width: 100%;
  li{
    margin-right: -20px;
  }
}
</style>
