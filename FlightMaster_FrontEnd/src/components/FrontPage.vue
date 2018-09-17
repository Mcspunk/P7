<template>
  <div>
    <h1>{{welcomeText}}</h1>
    <el-switch v-model="switchValue" v-on:change="welcomeTextPicker()"> </el-switch>
  </div>
</template>


<script>
export default {
  name: "FrontPage",
  data() {
    return {
      switchValue: true,
      welcomeText: "Så kører vi"
    };
  },
  methods:{
    welcomeTextPicker:function(){
      if(this.switchValue === true){
        this.welcomeText = "Så kører vi";
      }
      else{
        this.welcomeText = "Vi kører ikke mere";
      }
    }
  }
};
</script>

