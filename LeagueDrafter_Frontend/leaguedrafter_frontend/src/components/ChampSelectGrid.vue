<template>
  <div class="container">
    <Container :get-child-payload="getPayload" :group-name="'champGrid'" :orientation="'horizontal'" behaviour="move">
        <Draggable v-for="Champion in this.filteredChampions" :key="Champion.id" :class="determineDraggable(Champion)">
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
      return this.filteredChampions[index]
    },
    determineDraggable(champion){
      if(champion.picked) return "undraggable"
      else return ""
    }
  },
  components:{
    ChampionBox,Container,Draggable
  },
  computed:{
    filteredChampions(){
      return this.$store.state.filteredChampions
    },
    champions(){
      return this.$store.state.champions
    }
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
    width:75px;
    height:75px;
  }

  .undraggable{
    pointer-events: none;

  }

</style>
