<template>
  <div class="OuterContainer" v-loading="!this.myTurn"
    element-loading-text="Please pick for the other team"
    element-loading-background="rgba(0, 0, 0, 0.8)"
    element-loading-spinner="../assets/roleIcons/Mage_icon.png">
       <Container class="dropContainer" :should-accept-drop="() => myTurn" :should-animate-drop="() => false" v-for="placeHolder in placeHolders" :key="placeHolder.id" :orientation="'vertical'" behaviour="drop-zone" group-name="champGrid" @drop="onDrop('placeHolders', $event, placeHolder.id)">
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
  props: ["isAllyTeam"],
  name: "Team",
  data() {
    return {
      placeHolders: [
        {
          id: 0,
          champion: {
            orgId:-1,
            imgPath:"Top_icon.png",
            name:"Top",
            newId:-1,
            tags:"TopLaner"
          },
          role: "Top"
        },
        {
          id: 1,
          champion: {
            orgId:-1,
            imgPath:"Jungle_icon.png",
            name:"Jungle",
            newId:-1,
            tags:"Jungler"
          },
          role: "Jungle"
        },
        {
          id: 2,
          champion: {
            orgId:-1,
            imgPath:"Mid_icon.png",
            name:"Mid",
            newId:-1,
            tags:"MidLaner"
          },
          role: "Mid"
        },   
        {
          id: 3,
          champion: {
            orgId:-1,
            imgPath:"Bot_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 4,
          champion: {
            orgId:-1,
            imgPath:"Support_icon.png",
            name:"Support",
            newId:-1,
            tags:"Supporter"
          },
          role: "Support"
        }
      ]
    };
  },
  methods: {
    onDrop(collection, dropresult, index) {
      this[collection] = this.applyDrag(this[collection], dropresult, index);
    },
    applyDrag(arr, dragResult,index) {
      const { removedIndex, addedIndex, payload } = dragResult;
      if (removedIndex === null && addedIndex === null) return arr;

      const result = [...arr];
      let itemToAdd = payload;

      if (removedIndex !== null) {
        itemToAdd = result.splice(removedIndex, 1)[0];
      }

      if (addedIndex !== null) {
        if(result[index].champion.newId != -1){
          this.$store.commit('greyScaleChampion',{index:result[index].champion.newId,value:false})
          this.$store.commit('removeFromTeam',{champion:result[index].champion,team:this.isAllyTeam ? "allyTeam":"enemyTeam"})
        }
        this.$store.commit('greyScaleChampion',{index:itemToAdd.newId,value:true});
        this.$store.commit('addToTeam',{champion:itemToAdd,team:this.isAllyTeam ? "allyTeam":"enemyTeam"}) 
        result[index].champion=itemToAdd;
      }
      return result;
    },
    removeChampion(placeHolder){
      console.log(placeHolder)
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
  components: {
    PlayerSlot: PlayerSlot,
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
