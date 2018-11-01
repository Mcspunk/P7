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
      return require("../assets/champIcons/" + this.champion.imgPath);
    }
  }
};
</script>



<style lang="scss" scoped>
.container {
  height: 75px;
  width: 75px;
  background-color: aqua;
}
img {
  width: 100%;
  height: 100%;
}
</style>


