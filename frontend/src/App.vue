<template>
  <div id="app" >
    
  <!-- <div id="app" class="blur" :style="{ 'background-image': 'url(' + require('../public/big_plants.jpeg') + ')' }"> -->
   <popup v-if="$store.state.show_popup" />
    <login v-if="$store.state.show_login"/>

  
 <notifications width="40%" 
                position="top center" 
               
                :duration='5000'>

                   <template slot="body" slot-scope="props">
                      <div @click="props.close" class="my-notification">
                          <div class="title">
                            {{props.item.title}}
                          </div>
                          <!-- <div v-html="props.item.text">
                            {{props.item.text}}
                          </div> -->
                          <ul>
                            <li v-for="error in props.item.text" :key="error" >  {{error.message}} </li>
                          </ul>

                      </div>
                    </template>
  
 </notifications>



   <div  class="navbar"> 
    
      <!-- <div class="notification"> This is a Notification. </div> -->
        <div @click=" get_spot_wallet_balances()" class="website-name" > On The Spot </div>
        
        <button @click="$store.commit('toggleLogin')" class="nav-button"> Manage Keys </button>


        <label class="switch">
          <input @click.stop="toggleDarkMode()"   type="checkbox">
          <span class="slider-switch round"></span>
        </label>


  </div>

    <div class="container" >




      
     
 <div class="trading">

   <sell-comp :assets_loaded="assets_loaded" />

   <buy-comp />


</div >

<div class="history" >
  <div class="card history-card ">
        <div class="card-heading">
         <h3 class="card-title">Swap Info</h3>
        </div>
        <div class="card-body"> 
          
           <div class="item" >
            
            <div class="history-assets item-column"  >
              
              <div class="swap-asset" v-for="asset in $store.state.wallet_data.filter(asset => asset.selected == true)" :key="asset.asset" >
                  <img class="logo scale-up-center" :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">          
              </div>

            </div>
            <div class="arrow item-column">&rarr;</div>
           <div class="history-assets item-column">
                 
              
              
             <div class="swap-asset" v-for="asset in $store.state.wallet_data.filter(asset => asset.selected_to_buy == true && asset.selected != true)" :key="asset.asset" >
                  <img class="logo scale-up-center" :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">          
              </div>
            </div>
           
            <div class="item-column"> {{($store.state.wallet_data.filter(asset => asset.selected == true).reduce((prev, cur) => { return prev +  cur.usd_value * cur.percentage_to_sell / 100  } ,0) / $store.state.wallet_data.reduce((prev, cur) => { return prev +  cur.usd_value } ,0) * 100).toFixed(1)  }}%</div>
            <div class="item-column"> ${{ $number( $store.state.sell_amount )}}</div>

            <button @click="swapButtonClicked()" class="item-column swap-button list-item" role="button">Swap</button>
           

           </div>
          </div> 
         
        
           
      </div>
</div> 


 <!-- <trade-history/>  -->


    </div>
   
  
   
  </div>
</template>

<script>
import BuyComp from './components/BuyComp.vue'
// import TradeHistory from "./components/TradeHistory.vue"
import Popup from './components/Popup.vue'
import SellComp from './components/SellComp.vue'
import Login from './components/Login.vue'

import {
    enable as enableDarkMode,
    disable as disableDarkMode
} from 'darkreader';

export default {
  name: 'App',
  components:{
    Login,
    Popup,
    SellComp,
    BuyComp,
    // TradeHistory
  },
  data(){
    return{
      show_popup:false,
      assets_loaded: false,
      darkMode: true,
    }
  },
  methods:{
    get_spot_wallet_balances(){
      this.$axios
        .get(this.$server + "/api/spot-wallet-balances")
        .then( response => {
            this.$store.commit("setWalletData", response.data)
            this.assets_loaded = true
            }
        );
    },
    swapButtonClicked(){
      this.$store.commit('togglePopup')
      this.$store.commit('setSellAssetsList')
      console.log("what") 
      this.$root.$emit('swapButtonClicked')
     
    },
    toggleDarkMode(){
      console.log("Toggle Dark Mode")
      if(this.darkMode == true){
        disableDarkMode()
      }
      else{
        enableDarkMode({
            brightness: 100,
            contrast: 90,
            sepia: 10,
         });
      }
     
      this.darkMode = !this.darkMode;
    }
  },
  created(){
    this.get_spot_wallet_balances()

    enableDarkMode({
        brightness: 100,
        contrast: 90,
        sepia: 10,
    });


   
    // var array = ['#f5de139a', '#8062da'];
    // var interval = 5000; // how much time should the delay between two iterations be (in milliseconds)?
    // array.forEach(function (el, index) {
    //   setTimeout(function () {
    //    document.documentElement.style.setProperty("--main-color", el);
    //   }, index * interval);
    // });
    //document.documentElement.style.setProperty("--main-color", "red");
  }
 
}
</script>

<style> 
/* html{
  height: 100%;
} */
:root {
  --main-color: #ad5dc5d0;
  --secondary-color: rgba(240, 240, 240, 0.623);
  /* --main-color-without-opacity: #8062da; */
}


body {
  
  margin: 0;
  background: #edc0bf;
  /* background-color: var(--main-color); */
  background-color: var(--main-color); 
  /* background: linear-gradient(0deg, #0c69c0 0,#d327c5 80%); */
  font-family: 'Inter', sans-serif;


/*  */
/* background-color: #fff; */
  /* background-image: 
    radial-gradient(at top left, #7be75a, transparent),
    radial-gradient(at top right, #f3ad45, transparent),
    radial-gradient(at bottom left, #f11c98, transparent);
  background-size: 100% 100%;
  background-repeat: no-repeat; */
}

#app{
  /* filter: blur(50px); */
 background-size: 100% auto;
 height: 100%;
 background-repeat: no-repeat;
background-attachment: fixed;
}

.navbar{
  padding: 0.5rem 3rem;
  
  display: flex;
  position: sticky;
  top:0;
  z-index:100;

  align-content: center;
  background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  border: 1px solid rgba(255,255,255,0.2);
}

.website-name{
   font-family: "Impact";
   align-self: center;
   font-size: 2rem;
  font-weight: bolder;
  cursor: pointer;
   
}

.notification{
  text-align: center;
  font-weight: bolder;
  position:absolute;
  background-color: var(--main-color);
  padding:0.5rem 2rem;
  border-radius: 0.5rem;
  width: 300px;
  height: 20px;
  z-index: 1000;
  top: 10px;
  left: 50%;
  transform: translate(-50%, 0);
}

.back-img{
  width:100%;
  position: absolute;
  -webkit-backdrop-filter: blur(60px);
	backdrop-filter: blur(60px);

}


.container{
  padding: 1rem 5rem;
  /* height:700px; */
 /* display:none; */
}

.trading{
  display: flex;
  gap: 1;
  /* justify-content: space-between; */
  flex-wrap: wrap;
  /* height: 600px; */
}


.card {
  margin: 2rem;
  padding: 2rem 0.5rem;
  border-radius: 1rem;
  padding-bottom: 1rem;

}

.left-card{
  flex-grow:1;
  margin-left: 0px;
  height: 600px;
  /* width: 50%; */
   display:flex;
  flex-direction: column;
}


.right-card{
  flex-grow:1;
  /* margin-right: 0px; */
  height: 600px;
  /* width: 25%; */
  display:flex;
  flex-direction: column;
}

.history-card{
  margin: 2rem 0rem;
}

.card-body{
  height: 90%;
  overflow:scroll; 
  overflow-x: hidden;
  flex-grow: 4;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.card-body::-webkit-scrollbar {
  display: none;
}
/* Hide scrollbar for IE, Edge and Firefox */
.card-body{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
   
}


.card-title {
  margin-top: 0;
  margin-bottom: .5rem;
  font-size: 1.2rem;
  text-align: center;
}

p, a {
  font-size: 1rem;
}

a {
  color: #4d4ae8;
  text-decoration: none;
}
.card {
	/* other styles */
	background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  border: 1px solid rgba(255,255,255,0.2);
}
.shape {
  position: relative;
  width: 100%;
}

.item{
  cursor:pointer;
  border: 2px solid var(--main-color);
  border-radius: 1rem;
  padding: 1rem 1rem;
  margin: 1rem;
  background: rgba(255, 255, 255, .3);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(1px);
  /* border: 1px solid rgba(255,255,255,0.2); */
  /* box-shadow: rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset; */
  box-shadow: rgba(0, 0, 0, 0.45) 0px 15px 10px -10px;

  display:flex;
  gap:1rem;
  list-style: none;
  
  justify-content: space-evenly;
  align-content: center;

  }


 
.item {
  position: relative;

  transition: left ease 5s;
}

.item:first-child{
  margin-top: 0px;
}
.item-selected {
  left: -0px;
/* box-shadow: rgb(204, 219, 232) 3px 3px 6px 0px inset, rgba(255, 255, 255, 0.5) -3px -3px 6px 1px inset; */
box-shadow: none;
background-color:var(--main-color);/*  #cfceffca; */
} 


.logo{
 height: 30px;
 width: 30px;
 padding: 0px;
 
border-radius: 50%;
background: rgba(255, 255, 255, 0.7) ;
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(1px);
z-index: 100000;
 
}


.logo:hover{
  
} 

.text{
  align-self: center;
  margin-left: 1rem;
}

.coin-ticker{
  font-weight: bold;
}

.coin-price{
  font-size: 12px;
}

.item-column{
   width: 80px;
   align-self: center;
   flex-grow: 1;
   text-align: center;

   

}



.red{
  color: red;
}

.green{
  color: green;
}




.column-names{
  display: flex;
  align-content: center;
}

.arrow{
  font-size: 1.3rem;
  width: 20px;
}

.coin-add{
  display: block;
  border-radius: 1rem;
  padding: 1rem 1rem;
  margin: auto;
  background: rgba(255, 255, 255, .3);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(1px);
  /* border: 1px solid rgba(255,255,255,0.2); */
  /* box-shadow: rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset; */
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  border: 0px;
  width:70%;
 outline: none;
 text-transform: uppercase;


  
}

.multi-slider{
  width: 25px;
  border-radius: 1rem;
  padding: 1rem 3rem;
  margin: 2rem;
  margin-right: 0px;
  background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  /* border: 1px solid rgba(255,255,255,0.2); */
  /* box-shadow: rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset; */
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  margin-left: 0rem;

}
.general-slider{
  width: 25px;
  border-radius: 1rem;
  padding: 1rem 3rem;
  margin: 2rem 0rem;
  padding-top: 2rem;
  background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  /* border: 1px solid rgba(255,255,255,0.2); */
  /* box-shadow: rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset; */
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  /* margin-right: 2rem; */
}

.slider{
   /* visibility: hidden; */
   position:relative;
   top:50px;
   opacity:0;
   transition: opacity 1s ease;
}

.show-slider{
  
  opacity: 1;
}


.swap-data{
  border-radius: 1rem;
  padding: 1rem 1rem;
  
  background: rgba(255, 255, 255, .3);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(1px);
  /* border: 1px solid rgba(255,255,255,0.2); */
  /* box-shadow: rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset; */
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;

  display:flex;
  
  align-content: center;
  justify-content: space-around;
}
.history-assets{
  display:flex;
  overflow-x: auto;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.history-assets::-webkit-scrollbar {
  display: none;
}
/* Hide scrollbar for IE, Edge and Firefox */
.history-assets{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
   
}
.swap-percentage{
  text-align: center;
}
.swap-asset{
  margin: 0px 8px;
  
}

.swap-button{
  cursor:pointer;
  color: white;
  padding: 1rem 5rem;
  border-radius: 1rem;
  font-size: 1.3rem;
  background-color: var(--main-color);
  border: 0px solid black;
  font-weight: bolder;
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
}



/* Coin Logo Animation */

@-webkit-keyframes scale-up-center {
  0% {
    -webkit-transform: scale(0.5);
        transform: scale(0.5);
  }
  100% {
    -webkit-transform: scale(1);
        transform: scale(1);
  }
}
@keyframes scale-up-center {
  0% {
    -webkit-transform: scale(0.5);
          transform: scale(0.5);
  }
  100% {
    -webkit-transform: scale(1);
        transform: scale(1);
  }
}

.scale-up-center {
	-webkit-animation: scale-up-center 0.4s cubic-bezier(0.445, 0.050, 0.550, 0.950) both;
      animation: scale-up-center 0.4s cubic-bezier(0.445, 0.050, 0.550, 0.950) both;
}


/* Notification */
.my-notification {

  /* top: 60px; */
  margin: 0 5px 5px;
  margin-top: 5px;
  padding: 10px;
  font-size: 16px;
  color: #ffffff;
  border-radius: 1rem;
  -webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  /* filter: blur(10px); */
  text-align: center !important;
  background-color: var(--main-color) !important;

 
  
  /* .notification-title {
    
  } */

 
  /* .notification-content {
   
  } */

}


.select-all{
  position: absolute;
  right: 2rem;
  top: 3rem;
  cursor:pointer;
  color:var(--main-color); /*
  margin-left: auto;
  float:right; */
  /* margin-left:auto; */
}
.select-all:hover{
  text-decoration: underline;
}

.unselect-all{
  position: absolute;
  left: 2rem;
  top: 3rem;
  cursor:pointer;
  color:var(--main-color); 
}
.unselect-all:hover{
  text-decoration: underline;
}

.nav-button{
  background-color: var(--main-color);
  border: 2px solid var(--secondary-color);
  border-radius: 1rem;
  padding: 0rem 1rem;
  margin-left: auto;
  font-size: 1rem;
}
.nav-button:hover{
  cursor: pointer;
  -webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
}

/* Dark Reader Switch  */
/* Rounded sliders */
.slider-switch.round {
  border-radius: 34px;
}

.slider-switch.round:before {
  border-radius: 50%;
}

.switch {
  align-self: center;
  margin-left: 2rem;
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;

}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider-switch {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider-switch:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: var(--main-color);;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider-switch {
  background-color: white;
}

input:focus + .slider-switch {
  box-shadow: 0 0 1px white;
}

input:checked + .slider-switch:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

</style>
