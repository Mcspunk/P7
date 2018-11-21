<template>
  <div class="container">
    <Container :get-child-payload="getPayload" :group-name="'champGrid'" :orientation="'horizontal'" behaviour="move">
        <Draggable v-for="Champion in this.Champions" :key="Champion.id">
            <ChampionBox :champion="Champion" class="championSlot"> </ChampionBox>
        </Draggable>
    </Container>
  </div>
</template>

<script>
import { Container, Draggable } from "vue-smooth-dnd";
import ChampionBox from './ChampionBox.vue'
export default {
  data(){
    return{
      
    }
  },
  methods:{
    getPayload:function(index){
      return this.Champions[index];
    }
  },
  components:{
    ChampionBox,Container,Draggable
  }
}
</script>


<style lang="scss" scoped>
  .container{
    display:flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-left:4%;
  }
  .championSlot{
    display:inline-block;
    margin:8px;
  }

</style>
