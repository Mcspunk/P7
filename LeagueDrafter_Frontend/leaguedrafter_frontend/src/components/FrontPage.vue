<template>
  <div class="content" v-loading.fullscreen.lock="this.loading"
    element-loading-text="Loading..."
    element-loading-background="rgba(0, 0, 0, 0.8)">
    <md-steppers :md-active-step.sync="this.activeStepper" md-horizontal md-linear md-alternative>
      <md-step id="first" md-label="Picking order" :md-editable="false" :md-done.sync="this.firstStep">
          <div id="pickOrderContainer">
            <md-button @click="sidePicked('firstPick')" class="md-raised md-primary pickOrderButton">We have first pick</md-button>
            <md-button @click="sidePicked('secondPick')" class="md-raised md-accent pickOrderButton">They have first pick</md-button>
          </div>
      </md-step>
      <md-step id="second" md-label="Ban phase" :md-editable="false" :md-done.sync="this.secondStep">
        <div class="champAreaBan">
          <div>
              <ActiveBanArea> </ActiveBanArea>
          </div>
          <ChampSelect> </ChampSelect>
        </div>
      </md-step>

      <md-step id="third" md-label="Champion select" :md-editable="false" :md-done.sync="this.thirdStep">
        <div class="blueSide">
          <team :isAllyTeam="true"></team>
        </div>
        <div class="champArea">
          <InactiveBanArea v-if="bannedChampionCount != 0"> </InactiveBanArea>
          <ChampSelect> </ChampSelect>
        </div>
        <div class="redSide">
          <team :isAllyTeam="false"></team>
        </div>
      </md-step>
      <md-step id="fourth" md-label="Fight" :md-editable="false" :md-done.sync="this.fourthStep">
        <div class="blueSide">
          <team :isAllyTeam="true"></team>
        </div>
        <div class="statBox">
          
        </div>
        <div class="redSide">
          <team :isAllyTeam="false"></team>
        </div>
      </md-step>
    </md-steppers>
  </div>
</template>


<script>
import Team from './Team.vue'
import ChampSelect from './ChampSelect.vue'
import ActiveBanArea from './ActiveBanArea.vue'
import InactiveBanArea from './InactiveBanArea.vue'
export default {
  name:"FrontPage",
  data(){
    return{
    }
  },
  methods: {
      sidePicked(input){
        if(input==="firstPick") this.$store.commit('isAllyStarting',{value:true})
        else  this.$store.commit('isAllyStarting',{value:false})
        this.$store.commit('setStepperDone',{id:'firstStep', index:'second'});
      },
      setDone(idIn){
         this.$store.commit('setStepperDone',{id:idIn});
      }
    },
  components:{
    'Team' : Team,
    'ChampSelect' : ChampSelect,
    ActiveBanArea,
    InactiveBanArea
  },
  computed:{
    loading(){
      return this.$store.state.loading;
    },
    activeStepper(){
      return this.$store.state.activeStepper
    },
    firstStep(){
      return this.$store.state.firstStep
    },
    secondStep(){
      return this.$store.state.secondStep
    },
    thirdStep(){
      return this.$store.state.thirdStep
    },
    fourthStep(){
      return this.$store.state.fourthStep
    },
    currentState(){
      return this.$store.getters.getCurrentState
    },
    bannedChampionCount(){
      return this.$store.getters.getBannedChampionCount
    }
  }
}
</script>

<style lang="scss" scoped>
.content{
  position:relative;
  width: 100%;
  display:block;
}

.blueSide{
  float:left;
  position: relative;
  width:10%;
  height:100%;
  display:block;
  margin-top:77px;
  background-color: rgb(28, 123, 179);
}

.redSide{
  float:right;
  position: relative;
  width:10%;
  height:100%;
  display:block;
  margin-top:77px;
  background-color: rgb(219, 58, 58);
}

.champAreaBan{
  position:relative;
  width:100%;
  height:100%;
  display:inline-block;
  background-color: rgb(151, 150, 150);
}

.champArea{
  position:relative;
  width:80%;
  height:100%;
  display:inline-block;
  background-color: rgb(49, 49, 49);
}
.pickOrderButton{
  width: 50%;
  height:400px;
  font-size:50px;
}
.banArea{
  width: 70%;
}

#pickOrderContainer{
  display:flex;
  flex-direction: row;
  justify-content: center;
}
</style>
