<template>
  <div class="container">
    <ul>
      <li><PlayerSlot :champion="this.topPlaceHolder" :role="'Top'" :floatRole="this.blueTeam"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.junglePlaceHolder" :role="'Jungle'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.midPlaceHolder" :role="'Mid'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.botPlaceHolder" :role="'Bottom'"></PlayerSlot></li>
      <li><PlayerSlot :champion="this.supportPlaceHolder" :role="'Support'"></PlayerSlot></li>
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
        topPlaceHolder:{
          id:-1,
          imgPath:"Top_icon.png"
        },
        midPlaceHolder:{
          id:-1,
          imgPath:"Mid_icon.png"
        },
        junglePlaceHolder:{
          id:-1,
          imgPath:"Jungle_icon.png"
        },
        supportPlaceHolder:{
          id:-1,
          imgPath:"Support_icon.png"
        },
        botPlaceHolder:{
          id:-1,
          imgPath:"Bot_icon.png"
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
  overflow:hidden;
  display:block;
  width:100%;
  float:left;
  ul{
  list-style-type:none;
  width: 100%;
  float:inherit;
  li{
    margin-right: -20px;
  }
}
}

</style>
