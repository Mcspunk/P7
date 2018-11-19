<template>
  <div class="content">
    <md-steppers :md-active-step.sync="active" md-horizontal md-linear>
      <md-step id="first" md-label="Picking order" :md-editable="false" :md-done.sync="first">
          <div id="pickOrderContainer">
            <md-button @click="sidePicked('firstPick')" class="md-raised md-primary pickOrderButton">We have first pick</md-button>
            <md-button @click="sidePicked('secondPick')" class="md-raised md-primary pickOrderButton">They have first pick</md-button>
            <md-button @click="postData" class="md-raised md-primary">Send data</md-button>
          </div>
      </md-step>
      <md-step id="second" md-label="Ban phase" :md-editable="false" :md-done.sync="second">
        <div class="champArea">
          <ChampSelect> </ChampSelect>
        </div>
      </md-step>

      <md-step id="third" md-label="Third Step" :md-editable="false" :md-done.sync="third">
        
        <md-button class="md-raised md-primary" @click="setDone('third')">Done</md-button>
      </md-step>
    </md-steppers>
  </div>
</template>


<script>
import Team from './Team.vue'
import ChampSelect from './ChampSelect.vue'
export default {
  name:"FrontPage",
  data(){
    return{
      active: 'first',
      first: false,
      second: false,
      third: false,
      secondStepError: null,
      firstPick:null

    }
  },
  methods: {
      sidePicked(input){
        if(input==="firstPick") this.firstPick = true;
        else this.firstPick = false;
        this.setDone('first', 'second');
        console.log(this.firstPick);
      },
      setDone (id, index) {
        this[id] = true

        this.secondStepError = null

        if (index) {
          this.active = index
        }
      },
      setError () {
        this.secondStepError = 'This is an error!'
      },
      postData(){
        this.$http.post(this.$api.MCTS.postChampChoice, this.SelectedChamps)
        .then(response =>{
          this.continue = true;
        })
      }
    },
  components:{
    'Team' : Team,
    'ChampSelect' : ChampSelect
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

.champArea{
  position:relative;
  width:100%;
  height:100%;
  display:inline-block;
  background-color: rgb(151, 150, 150);
}

.pickOrderButton{
  width: 50%;
  height:400px;
  font-size:50px;
}

#pickOrderContainer{
  display:flex;
  flex-direction: row;
  justify-content: center;
}
</style>
