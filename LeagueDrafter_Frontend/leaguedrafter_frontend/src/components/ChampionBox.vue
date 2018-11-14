<template>
<div class="container">
  <md-card md-with-hover>
    <md-ripple>
    <md-card-area>
      <md-card-media md-ratio="1:1">
          <img :src="getImgFile()">
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
}
img {
  width: 100%;
  height: 100%;
}
</style>


