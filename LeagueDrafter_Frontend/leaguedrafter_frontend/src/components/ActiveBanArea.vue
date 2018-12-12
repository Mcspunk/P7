<template>
  <div class="outerContainer">
      <h2>Drag'n'Drop banned champions</h2>
       <Container :should-animate-drop="()=>false" v-for="placeHolder in banPlaceholders" :key="placeHolder.id" :orientation="'vertical'" behaviour="drop-zone" group-name="champGrid" @drop="onDrop('banPlaceholders', $event, placeHolder.id)" @drag-start="onDragStart" @drag-end="onDragEnd">
            <div  id="banSlot" @click="removeChampion(placeHolder)">
              <PlayerSlot :displaySetting="displaySetting" :champion="placeHolder.champion" :role="''"></PlayerSlot>
            </div>
      </Container>
      <div class="continueButton">
        <md-button class="md-raised md-primary continueButton" @click="setDone('secondStep', 'third')">Continue</md-button>
      </div>
      
  </div>
</template>

<script>
import PlayerSlot from "./PlayerSlot.vue";
import { Container } from "vue-smooth-dnd";
export default {
  name: "ActiveBanArea",
  data() {
    return {
      displaySetting:"noShadow"
    };
  },
  methods: {
    onDrop(collection, dropresult, index) {
      this.$store.commit("championBanned",{dropresult:dropresult,placeHolderIndex:index})
    },
    onDragStart(){
      this.displaySetting = "outerShadow"
    },
    onDragEnd(){
      this.displaySetting = "noShadow"
    },
    setDone(arg1,arg2){
      this.$store.commit('banChampions',{champions:this.banPlaceholders.filter(placeHolder => placeHolder.champion.newId != -1),ban:true})
      this.$store.commit('setStepperDone',{id:arg1,index:arg2})
      this.$store.commit('gotoPickPhase')
      //this.$parent.$parent.methods.setDone(arg1,arg2);
    },
    removeChampion(placeHolder){
      this.$store.commit('greyScaleChampion',{index:placeHolder.champion.newId,value:false,type:"ban"});
      placeHolder.champion = {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Ban",
            newId:-1,
            tags:"Ban"
          } 
    },
    containerClass(){
      if(this.active) return "activeContainers"
      else return "inactiveContainers"
    }
  },
  components: {
    PlayerSlot: PlayerSlot,
    Container
  },
  computed:{
    banPlaceholders(){
      return this.$store.state.banPlaceholders
    }
  }
};
</script>

<style lang="scss" scoped>
.outerContainer {
  display: flex;
  flex-direction: row;
  flex-wrap:wrap;
  justify-content: center;
  align-items:center;
  background-color: rgb(58, 58, 58);
  h2{
    width: 100%;
    text-align:center;
  }
}


.container{
    margin:5px;
}

</style>
