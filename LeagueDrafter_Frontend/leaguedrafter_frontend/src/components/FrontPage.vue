<template>
  <div class="content" v-loading.fullscreen.lock="this.loading"
    element-loading-text="Loading..."
    element-loading-background="rgba(0, 0, 0, 0.8)">
    <md-steppers :md-active-step.sync="this.activeStepper" md-horizontal md-linear>
      <md-step id="first" md-label="Picking order" :md-editable="false" :md-done.sync="this.firstStep">
          <div id="pickOrderContainer">
            <md-button @click="sidePicked('firstPick')" class="md-raised md-primary pickOrderButton">We have first pick</md-button>
            <md-button @click="sidePicked('secondPick')" class="md-raised md-primary pickOrderButton">They have first pick</md-button>
            <md-button @click="postData" class="md-raised md-primary">Send data</md-button>
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
          <team></team>
        </div>
        <div class="champArea">
          <InactiveBanArea> </InactiveBanArea>
          <ChampSelect> </ChampSelect>
        </div>
        <div class="redSide">
          <team></team>
        </div>
        
        <md-button class="md-raised md-primary" @click="setDone('thirdStep')">Done</md-button>
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
      firstPick:null,
      currentState:{
        ally_starting:true,
        ally_team:[108,103],
        enemy_team:[130,85],
        banned_champs:[0,1,2,3,4,5,6,7,8,9]
      }
    }
  },
  methods: {
      sidePicked(input){
        if(input==="firstPick") this.firstPick = true;
        else this.firstPick = false;
        this.$store.commit('setStepperDone',{id:'firstStep', index:'second'});
      },
      postData(){
        this.$http.post(this.$api.MCTS.postCurrentState, this.currentState)
        .then(response =>{
          console.log(response)
        })
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
  width:15%;
  height:100%;
  display:block;
  background-color: rgb(28, 123, 179);
}

.redSide{
  float:right;
  position: relative;
  width:15%;
  height:100%;
  display:block;
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
  width:70%;
  height:100%;
  display:inline-block;
  background-color: rgb(151, 150, 150);
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
