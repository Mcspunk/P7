<template>
  <div class="OuterContainer">
    <Container :get-child-payload="getPayload" :group-name="'champGrid'" :orientation="'horizontal'" behaviour="drop-zone" >
    <Draggable id="champ1Box" :class="determineDraggableChamp1(champ1)" >
      <ChampionBox :champion="champ1"> </ChampionBox>
    </Draggable>
    
    <Draggable id="champ2Box" :class="determineDraggableChamp2(champ2)" >
      <ChampionBox :champion="champ2"> </ChampionBox>
    </Draggable>
    </Container>
    <h2>
      <md-tooltip id="scoreToolTip" md-direction="bottom">The score is a representation of <br> how well the champion(s) are  <br> expected to contribute towards victory</md-tooltip>
      Score: {{this.score}}
    </h2>
  </div>
</template>



<script>
import ChampionBox from "./ChampionBox.vue";
import {Draggable, Container} from "vue-smooth-dnd";
export default {
  props:['champ1','champ2','score'],
  name:"ChampionPairBox",
  methods:{
    determineDraggableChamp1(champion){
      if(champion.picked) return "undraggable"
      else return ""
    },
    determineDraggableChamp2(champion){
      if(champion.picked) return "undraggable"
      else return ""
    },
    getPayload:function(index){
      if(index === 0){
        return this.champ1
      }
      else return this.champ2
    }
  },
  components:{
    ChampionBox,Draggable,Container
  },
  computed:{
    filteredChampions(){
      return this.$store.state.filteredChampions
    }
  }
}
</script>


<style lang="scss" scoped>
.OuterContainer{
  display:block;
  margin:10px;
  text-align: center;
  background-color:rgba(70, 71, 71, 0.575);
  h2{
    padding-bottom:5px;
  }
  border-radius: 5px;
  border-style:solid;
  border-width: 1px;
  border-color: rgb(134, 93, 2)
}

#champ1Box{
  margin:2px;
}

#champ2Box{
  margin:2px;
}

.undraggable{
    pointer-events: none;
  }

#scoreToolTip{
  background-color: rgba(165, 164, 164, 0.747);
  width: 220px;
  height:65px;
  font-size: 12px;
  border-radius: 5px;
  border-style:solid;
  border-width: 1px;
  border-color: rgb(134, 93, 2)
}
</style>


