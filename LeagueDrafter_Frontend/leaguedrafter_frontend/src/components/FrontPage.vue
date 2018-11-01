<template>
  <div class="content">
    <div class="blueSide">
      <Team :blueTeam="true"></Team>
    </div>
    <div class="champArea">
      <ChampSelect> </ChampSelect>
    </div>
    <div class="redSide">
      <Team :blueTeam="false"></Team>
    </div>
  </div>
</template>


<script>
import Team from './Team.vue'
import ChampSelect from './ChampSelect.vue'
export default {
  name:"FrontPage",
  components:{
    'Team' : Team,
    'ChampSelect' : ChampSelect
  }
}
</script>

<style lang="scss" scoped>
.content{
  margin-top:30px;
  position:relative;
  width: 100%;
  display:block;
}

.blueSide{
  float:left;
  position: relative;
  width:15%;
  height:100%;
  display:block;
  background-color: rgb(5, 105, 199);
}

.redSide{
  float:right;
  position: relative;
  width:15%;
  height:100%;
  display:block;
  background-color: rgb(219, 58, 58);
}

.champArea{
  position:relative;
  width:70%;
  height:100%;
  display:inline-block;
  background-color: rgb(151, 150, 150);
}
</style>
