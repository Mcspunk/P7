<template>
  <div class="Outercontainer">
      <VuePerfectScrollbar class="test">
    <Container :get-child-payload="getPayload" :group-name="'champGrid'" :orientation="'horizontal'" behaviour="drop-zone" >
        <Draggable v-if="activeTab!='tab-suggestion'" v-for="Champion in filteredChampions" :key="Champion.id" :class="determineDraggable(Champion)" >
            <div v-on:click="banChampion(Champion)">
              <ChampionBox :champion="Champion" class="championSlot"> </ChampionBox>
            </div>
        </Draggable>
        <Div v-if="(suggestedChampions.length > 0 && suggestedChampions[0].champ2 != null && activeTab==='tab-suggestion')" v-for="i in 10" :key="i" >
              <ChampionPairBox :champ1="filteredChampions[i+i-2]" :champ2="filteredChampions[i+i-1]" :score="suggestedChampions[i-1].score"> </ChampionPairBox>
        </Div>
        <Draggable v-if="suggestedChampions.length > 0 && suggestedChampions[0].champ2 === null && activeTab==='tab-suggestion'" v-for="Champion in filteredChampions" :key="Champion.id" :class="determineDraggable(Champion)" >
            <div class="singleSuggestion">
              <ChampionBox :champion="Champion" class="championSlot"> </ChampionBox>
              <h2>
                <md-tooltip id="scoreToolTip" md-direction="bottom">The score is a representation of <br> how well the champion(s) are  <br> expected to contribute towards victory</md-tooltip>
                Score: {{suggestedChampions.find(x => x.champ1.newId === Champion.newId).score}}
              </h2>
            </div>
        </Draggable>
    </Container>
      </VuePerfectScrollbar>
  </div>
</template>

<script>
import { Container, Draggable } from "vue-smooth-dnd";
import ChampionBox from './ChampionBox.vue'
import SimpleBar from 'simplebar-vue'
import 'simplebar/dist/simplebar.min.css'
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import ChampionPairBox from "./ChampionPairBox.vue"
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
    },
    banChampion:function(champion){
      console.log(champion)
      if(this.allyTurn === null){
        var firstFreeIndex = this.banPlaceholders.findIndex(placeHolder => placeHolder.champion.newId === -1)
        if(firstFreeIndex != -1){
          this.$store.commit("championBanned",{
            placeHolderIndex:firstFreeIndex,
            dropresult:{
              payload:champion,
              removedIndex: null,
              addedIndex: 0
            }
            })
        }
      }
    }
  },
  components:{
    ChampionBox,Container,Draggable,SimpleBar,VuePerfectScrollbar,ChampionPairBox
  },
  computed:{
    filteredChampions(){
      return this.$store.state.filteredChampions
    },
    champions(){
      return this.$store.state.champions
    },
    banPlaceholders(){
      return this.$store.state.banPlaceholders
    },
    allyTurn(){
      return this.$store.state.allyTurn
    },
    suggestedChampions(){
      return this.$store.state.suggestedChampions
    },
    activeTab(){
      return this.$store.state.activeTab
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
  .Outercontainer{
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
  .test {
  height: 500px;
}

.singleSuggestion{
  display:block;
  margin:10px;
  text-align: center;
  padding-left: 5px;
  padding-right: 5px;
  background-color:rgba(70, 71, 71, 0.575);
  h2{
    padding-bottom:5px;
  }
  border-radius: 5px;
  border-style:solid;
  border-width: 1px;
  border-color: rgb(134, 93, 2)
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
