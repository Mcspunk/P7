<template>
  <div class="OuterContainer" v-loading="!this.myTurn && !locked"
    element-loading-text="Please pick for the other team"
    element-loading-background="rgba(0, 0, 0, 0.8)"
    element-loading-spinner="../assets/roleIcons/Mage_icon.png">
       <Container class="dropContainer" :should-accept-drop="() => myTurn && !locked" :should-animate-drop="() => false" v-for="placeHolder in placeHolders" :key="placeHolder.id" :orientation="'vertical'" behaviour="drop-zone" group-name="champGrid" @drop="onDrop(placeholderName(), $event, placeHolder.id)">
            <div @click="removeChampion(placeHolder)">
              <PlayerSlot :champion="placeHolder.champion" :role="placeHolder.role"></PlayerSlot>
            </div>
      </Container>
  </div>
</template>

<script>
import PlayerSlot from "./PlayerSlot.vue";
import { Container } from "vue-smooth-dnd";
export default {
  props: ["isAllyTeam","locked"],
  name: "Team",
  data() {
    return {
    };
  },
  methods: {
    onDrop(collection, dropresult, index) {
      this.$store.commit("championChosen",{placeholderName:collection,dropresult:dropresult,placeHolderIndex:index})
    },
    removeChampion(placeHolder){
      if(!this.locked){
      this.$store.commit('greyScaleChampion',{index:placeHolder.champion.newId,value:false});
      this.$store.commit('removeFromTeam',{champion:placeHolder.champion,team:this.isAllyTeam ? "allyTeam":"enemyTeam"})
      placeHolder.champion = {
            orgId:-1,
            imgPath:placeHolder.role+"_icon.png",
            name:placeHolder.role,
            newId:-1,
            tags:placeHolder.role
          } 
      }
    },
    placeholderName(){
      if(this.isAllyTeam) return 'allyPlaceholders';
      else return 'enemyPlaceholders';
    }
  },
  components: {
    PlayerSlot,
    Container
  },
  computed:{
    myTurn(){
      if(this.isAllyTeam && this.allyTurn) return true;
      else if(!this.isAllyTeam && !this.allyTurn ) return true;
      else return false;
    },
    allyTurn(){
      return this.$store.state.allyTurn;
    },
    placeHolders(){
      if(this.isAllyTeam) return this.$store.state.allyPlaceholders;
      else return this.$store.state.enemyPlaceholders;
    }
  }
};
</script>

<style lang="scss" scoped>
.OuterContainer {
  display: flex;
  flex-direction: column;
  flex-wrap:wrap;
  align-items: center;
  padding-bottom: 15px;
  padding-top:10px;
}
.dropContainer{
  width: 75px;
}
</style>
