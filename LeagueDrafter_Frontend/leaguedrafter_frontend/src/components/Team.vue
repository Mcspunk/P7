<template>
  <div class="container">
    <ul v-for="placeHolder in this.placeHolders" :key="placeHolder.imgPath">
      <Container @drop="onDrop" :group-name="'champGrid'" :orientation="'vertical'" behaviour="drop-zone">
        <li><PlayerSlot :champion="placeHolder" :role="placeHolder.role"></PlayerSlot></li>
       </Container>
    </ul>
   
  </div>
</template>

<script>
import PlayerSlot from './PlayerSlot.vue'
import {Container} from "vue-smooth-dnd"
export default {
  props:["blueTeam"],
  name:"Team",
  data () {
    return {
      placeHolders:[
        {
          id:-1,
          imgPath:"Top_icon.png",
          role:"Top"
        },
        {
          id:-1,
          imgPath:"Mid_icon.png",
          role:"Mid"
        },
        {
          id:-1,
          imgPath:"Jungle_icon.png",
          role:"Jungle"
        },
        {
          id:-1,
          imgPath:"Support_icon.png",
          role:"Support"
        },
        {
          id:-1,
          imgPath:"Bot_icon.png",
          role:"Bot"
        }
      ]
        
    }
  },
  methods:{
    onDrop(dropResult){
      this.placeHolders.splice(0,1,dropResult.payload);
    }
  },
  components:{
    'PlayerSlot' : PlayerSlot,
    Container
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
