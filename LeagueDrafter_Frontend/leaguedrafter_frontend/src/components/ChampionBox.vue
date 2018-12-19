<template>
<div class="container">
  <md-card>
    <md-ripple>
    <md-card-area>
      <md-card-media md-ratio="1:1">
          <img :class="getImgClass()" :src="getImgFile()">
        </md-card-media>
    </md-card-area>
    </md-ripple>
  </md-card>
</div>

</template>

<script>
export default {
  name: "ChampionBox",
  props: ["champion"],
  data() {
    return {};
  },
  methods: {
    getImgFile() {
      return require("../assets/champIcons/" + this.getChampion.imgPath);
    },
    getImgClass(){
      if(this.champion.banned || this.champion.picked) return "imgGreyScale"
      else return ""
    }
  },
  computed:{
    getChampion(){
      return this.champion
    }
  }
};
</script>



<style lang="scss" scoped>
.container {
  height: 75px;
  width: 75px;
  background-color: rgba(0, 255, 255, 0);
  :hover{
    box-shadow: 0px 1px 20px rgba(255, 255, 255, 0.719);
    cursor:-webkit-grab
  }
}
img {
  width: 100%;
  height: 100%; 
}
.imgGreyScale{
  filter: grayscale(100%);
}
</style>


