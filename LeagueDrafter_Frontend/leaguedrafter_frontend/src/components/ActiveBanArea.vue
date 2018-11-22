<template>
  <div class="outerContainer">
      <h2>Drag'n'Drop banned champions</h2>
       <Container :should-animate-drop="()=>false" v-for="placeHolder in placeHolders" :key="placeHolder.id" :orientation="'vertical'" behaviour="drop-zone" group-name="champGrid" @drop="onDrop('placeHolders', $event, placeHolder.id)">
            <div id="banSlot" @click="removeChampion(placeHolder)">
              <PlayerSlot :champion="placeHolder.champion" :role="''"></PlayerSlot>
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
      placeHolders: [
        {
          id: 0,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Ban",
            newId:-1,
            tags:"Ban"
          },
          role: "Top"
        },
        {
          id: 1,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Mid",
            newId:-1,
            tags:"MidLaner"
          },
          role: "Mid"
        },
        {
          id: 2,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Jungle",
            newId:-1,
            tags:"Jungler"
          },
          role: "Jungle"
        },
        {
          id: 3,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Support",
            newId:-1,
            tags:"Supporter"
          },
          role: "Support"
        },
        {
          id: 4,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 5,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 6,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 7,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 8,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        },
        {
          id: 9,
          champion: {
            orgId:-1,
            imgPath:"Ban_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
        }
      ],
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
        if(result[index].champion.newId >= 0)  this.$store.commit('greyScaleChampion',{index:result[index].champion.newId,value:false})
        this.$store.commit('greyScaleChampion',{index:itemToAdd.newId,value:true})
        result[index].champion=itemToAdd;
      }

      return result;
    },
    setDone(arg1,arg2){
      this.$store.commit('banChampions',{champions:this.placeHolders.filter(placeHolder => placeHolder.champion.newId != -1),ban:true})
      this.$store.commit('setStepperDone',{id:arg1,index:arg2})
      //this.$parent.$parent.methods.setDone(arg1,arg2);
    },
    removeChampion(placeHolder){
      this.$store.commit('greyScaleChampion',{index:placeHolder.champion.newId,value:false});
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
