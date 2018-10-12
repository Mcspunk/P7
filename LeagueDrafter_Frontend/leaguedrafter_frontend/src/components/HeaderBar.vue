<template>
  <div class="nawbar">
    <div v-bind:class="[{ noOverflow: this.showNavigation }, container]">
      <ul>
        <li id="NawAbout"> <router-link class="linkText" :to="{ name: 'About'}"> About </router-link></li>
        <li id="NawHome"> <router-link class="linkText" :to="{ name: 'FrontPage'}"> Home </router-link></li>
      </ul>

      <input type="checkbox" class="toggle-nav" id="toggle-nav" v-on:click="changeVisisbility()">
        <div class="mobile-bar" id="mobile-bar">
          <label for="toggle-nav"></label>
        </div>
      <div class="mobile-nav-panel" id="mobileNavDropDown">
              <ul>
                  <li id="NawHome"> <router-link class="linkText" :to="{ name: 'FrontPage'}"> Home </router-link></li>
                  <li id="NawAbout"> <router-link class="linkText" :to="{ name: 'About'}"> About </router-link></li>
              </ul>
      </div>   
    </div>
    
    
  </div>
</template>

<script>
export default {
  name: "NawBar",
  data() {
    return {
      showNavigation: false,
      container: "container",
      noOverflow: "noOverflow"
    };
  },
  methods: {
    changeVisisbility() {
      this.showNavigation = !this.showNavigation;
    }
  },
  components: {}
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.toggle-nav {
  display: none;
}

.mobile-bar {
  z-index: 5;
  position: relative;
  height: 60px;
}

.mobile-bar label {
  position: relative;
  margin-top: -40px;
  margin-right: 20px;
  width: 70px;
  height: 50px;
  float: right;
  text-align: center;
  cursor: pointer;
  -webkit-transition: -webkit-transform 500ms ease;
  transition: -webkit-transform 500ms ease;
  transition: transform 500ms ease;
  transition: transform 500ms ease, -webkit-transform 500ms ease;
}

.mobile-bar label:after {
  content: "\2630";
  font-size: 3em;
  color: #2d4374;
  line-height: 50px;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  -webkit-transition: 500ms ease;
  transition: 500ms ease;
}

.toggle-nav:checked ~ .mobile-nav-panel {
  /* when the checkbox is checked the container slide-down */
  -webkit-transform: translateX(-770px);
  transform: translateX(-770px);
  -webkit-transform: translate3d(-770px, 0, 0);
  transform: translate3d(-770px, 0, 0);
}

.toggle-nav:checked + .mobile-bar label {
  -webkit-transform: rotate(180deg);
  transform: rotate(180deg);
}

.toggle-nav:checked + .mobile-bar label:after {
  color: rgb(181, 132, 53);
}

.nawbar {
  padding-bottom: 12px;
  height: 60px;
  background-color:rgb(40, 40, 49);
}
.mobile-nav-toggle {
  height: 50px;
  right: 30px;
  width: 50px;
  color: #000000;
  cursor: pointer;
  z-index: 10000;
  float: center;
  position: relative;
}

.mobile-nav-icon {
  position: absolute;
  z-index: 3;
  top: 20px;
  width: 70px;
  height: 3px;
  background: #000000;
}
.mobile-nav-icon:after {
  position: absolute;
  z-index: 3;
  width: 70px;
  height: 3px;
  top: 12px;
  background: #000000;
  content: "";
}
.mobile-nav-icon:before {
  position: absolute;
  z-index: 3;
  top: -12px;
  width: 70px;
  height: 3px;
  background: #000000;
  content: "";
}
.mobile-nav-panel {
  z-index: 5;
  display: block;
  right: 0px;
  position: absolute;
  float: left;
  width: 100%;
  margin-top: -35px;
  margin-right: -770px;
  background-color: rgba(36, 49, 66, 0.8);
  box-shadow: -2px 3px 8px rgba(0, 0, 0, 0.541);

  -webkit-transition: -webkit-transform 500ms ease;
  transition: -webkit-transform 500ms ease;
  transition: transform 500ms ease;
  transition: transform 500ms ease, -webkit-transform 500ms ease;
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0px;
    overflow: hidden;
    background-color: rgba(36, 49, 66, 0.8);
    li {
      float: none;
      :hover {
        background: rgb(36, 49, 66);
      }
    }
  }
  .linkText {
    color: #ffffff;
    font-size: 22px;
  }
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.container {
  margin-right: auto;
  margin-left: auto;
  position: relative;
  height: 300px;
  overflow: hidden;
}

.noOverflow {
  overflow: visible;
}
.logo {
  float: left;
  padding-top: 10px;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0px;
  overflow: hidden;
  background-color: inherit;
  float: left;
}

li {
  float: right;
  margin-right:25px;
  margin-top:35px;
  :hover{
    background-color: black;
    border-bottom: 1px solid rgb(255, 255, 255);
  }
}
a {
  color: #ffffff;
  text-decoration: none;
}
.linkText {
  display: block;
  color: #ffffff;
  font-size: 25px;
  border: none;
}

/* Smartphones (portrait and landscape) ----------- */
@media only screen and (min-width: 0px) and (max-width: 767px) {
  .nawbar {
    min-width: 600px;
  }
  #NawAbout,
  #NawHome {
    display: none;
  }
  .logo {
    text-align: left;
    top: 5px;
    left: 35%;
    position: relative;
  }
}

/* iPads and Desktops ----------- */
@media only screen and (min-width: 768px) and (max-width: 1023px) {
  .container {
    width: 700px;
  }
  #mobileNavDropDown,
  #mobile-bar {
    display: none;
  }

  .toggle-nav:checked ~ .mobile-nav-panel {
    -webkit-transform: translateX(0);
    transform: translateX(0);
  }
}

@media only screen and (min-width: 1024px) and (max-width: 1439px) {
  .container {
    width: 970px;
  }
  #mobileNavDropDown,
  #mobile-bar {
    display: none;
  }
  .toggle-nav:checked ~ .mobile-nav-panel {
    -webkit-transform: translateY(0px);
    transform: translateY(0px);
    display: none;
  }
}

@media only screen and (min-width: 1440px) {
  .container {
    width: 1400px;
  }
  #mobileNavDropDown,
  #mobile-bar {
    display: none;
  }
  .toggle-nav:checked ~ .mobile-nav-panel {
    -webkit-transform: translateX(0px);
    transform: translateX(0px);
  }
}
</style>
