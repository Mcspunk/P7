<template>
  <div class="outerContainer">
      <h3>Banned champions:</h3>
       <div class="banSlot" @click="removeChampion(placeHolder)" v-for="bannedChampion in this.bannedChampions" :key="bannedChampion.newId">
          <ChampionBox class="champSlot" :champion="bannedChampion"> </ChampionBox>
       </div>
  </div>
</template>

<script>
import ChampionBox from "./ChampionBox.vue";
export default {
  name: "ActiveBanArea",
  data() {
    return {
    }
  },
  methods: {
  },
  components: {
    ChampionBox
  },
  computed:{
    bannedChampions(){
      return this.$store.state.bannedChampions
    }
  }
};
</script>

<style lang="scss" scoped>
.outerContainer {
  display: flex;
  flex-direction: row;
  flex-wrap:wrap;
  justify-content: left;
  align-items:center;
  background-color: rgb(58, 58, 58);
  h3{
    margin-left:20px;
    margin-right:10px;
  }
}

.banSlot{
  width:45px;
  height:45px;
  .champSlot{
    width: inherit;
    height: inherit;
    
  }
  margin:2px;
}





</style>
