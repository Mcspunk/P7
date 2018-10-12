<template>
  <div class="container">
    <img :src="getImgFile()">
  </div>
</template>

<script>
export default {
  name: "ChampionBox",
  props: ["champion"],
  data() {
    return{

    }
  },
  methods:{
    getImgFile(){
      return require("../assets/champIcons/" + this.champion.imgPath)
    }
  }
  
}
</script>



<style lang="scss" scoped>
.container{
  height:75px;
  width:75px;
  background-color: aqua;
}
img{
  width:100%;
  height:100%;
}
</style>


