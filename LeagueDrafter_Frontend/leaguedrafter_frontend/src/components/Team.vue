<template>
  <div class="container">
       <Container class="dropContainer" :should-animate-drop="()=>false" v-for="placeHolder in placeHolders" :key="placeHolder.id" :orientation="'vertical'" behaviour="drop-zone" group-name="champGrid" @drop="onDrop('placeHolders', $event, placeHolder.id)">
            <div>
              <PlayerSlot :champion="placeHolder.champion" :role="placeHolder.role"></PlayerSlot>
            </div>
      </Container>
  </div>
</template>

<script>
import PlayerSlot from "./PlayerSlot.vue";
import { Container } from "vue-smooth-dnd";
export default {
  props: ["blueTeam"],
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
            imgPath:"Mid_icon.png",
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
            imgPath:"Jungle_icon.png",
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
            imgPath:"Support_icon.png",
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
            imgPath:"Bot_icon.png",
            name:"Bot",
            newId:-1,
            tags:"BotLaner"
          },
          role: "Bot"
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
        result[index].champion=itemToAdd;
      }

      return result;
    }
  },
  components: {
    PlayerSlot: PlayerSlot,
    Container
  }
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  flex-wrap:wrap;
  align-items: center;
}
.dropContainer{
  width: 75px;
}
</style>
