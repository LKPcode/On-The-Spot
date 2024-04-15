<template>
  <div  >
    <div class="icon-list" >
               <div v-if="this.$store.state.wallet_data.filter(asset => asset.selected == true).length >= 1 ">
                  <div :class="{'asset-selected': asset_chosen == 'Global'}" @click="chooseAsset('Global')"  class="logo scale-up-center" style="width:30px;margin-bottom:4px;" > </div>
              </div>
              <div  v-for="asset in $store.state.wallet_data.filter(asset => asset.selected == true)" :key="asset.asset">
                  <img :class="{'asset-selected': asset_chosen == asset.asset}" @click="chooseAsset(asset.asset)"  class="logo scale-up-center" :src='$server+ "/static/" +  asset.asset.toLowerCase() + ".svg"' style="width:30px;" >
              </div>
    </div>

    <div  v-if="this.$store.state.wallet_data.filter(asset => asset.selected == true).length >= 1 " class="asset-name" >{{asset_chosen}}</div>

    <vue-slider class="slider"
    
     :class='{"show-slider": this.$store.state.wallet_data.filter(asset => asset.selected == true).length >= 1 }'
               v-model="value"
               :order="true"
               :process="process"
               :tooltip-formatter="formatter"
               :enable-cross="true"
               :tooltip="'always'"    
               :direction="'btt'"
               :height="'90%'"
               :width="10"
               :interval="0.1"
               :change="onChange(value)"
              
    >
    <template v-slot:process="{ style, index}">
          <div class="vue-slider-process" :style="style">
            <div :class="[
              'merge-tooltip',
            ]"
            v-if="index == 0"
            >
              <!-- <div  v-for="asset in $store.state.wallet_data.filter(asset => asset.selected == true)" :key="asset.asset">
                  <img class="logo scale-up-center" :src='$server+ "/static/" +  asset.asset.toLowerCase() + ".svg"' style="width:30px;" >
              </div> -->
            </div>
          </div>

        

        </template>
    <template #tooltip="{ value }">
        <div class="tooltip-left">
            {{value.toFixed(1)}}%
          <!-- <img src="../../public/aave.svg" style="width:30px;" > -->
          </div>
           <div v-if="asset_chosen=='Global'" class="tooltip-right">
               ${{$number($store.state.wallet_data.filter(asset => asset.selected == true).reduce((prev, cur) => { return prev +  cur.usd_value * value / 100  } ,0))}}
           </div>
            <div v-else class="tooltip-right">
               ${{$number($store.state.wallet_data.filter(asset => asset.asset == asset_chosen)[0].usd_value * value/100)}}
           </div>
       
      </template>
    
    </vue-slider>

  </div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import { debounce } from "debounce";


export default {
  name: 'GeneralSlider',
  components: {
    VueSlider
  },
   data: function () {
      return {
        value: 25,
        formatter: '{value}%',
         process: dotsPos => [
          [ dotsPos[0],0, { backgroundColor: 'var(--main-color)' }],
          [dotsPos[0],100, { backgroundColor: 'gray' }]
        
        ],
        coins: ["aave","dot"],
        asset_chosen: "Global",
        asset_chosen_index: NaN,
      }
   },
   methods:{
     setSellAmount(value){
       let amount = this.$store.state.wallet_data.filter(asset => asset.selected == true)
                                            .reduce((prev, cur) => { return prev +  cur.usd_value * value / 100  } ,0)
       this.$store.commit("setSellAmount" ,amount)
     },
     setGlobalSellPercentage(percent){
       this.$store.commit("setGlobalSellPercentage" ,percent)
     },
     onChange: debounce(function (value) {
       console.log(value)
       if(this.asset_chosen == "Global"){
        this.setSellAmount(value)
        this.setGlobalSellPercentage(value)
        this.$store.commit("setAmountToSellOfCoins") 
       }
       else{
         this.$store.commit("setPercentageOfSellAsset", {index: this.asset_chosen_index, value: this.value}) 
       }
     }, 20),
     chooseAsset(asset){
       this.asset_chosen = asset
       if( this.asset_chosen == "Global"){
        //  this.value = this.$store.state.global_sell_percentage
       }else{
        let index = this.$store.state.wallet_data.findIndex(assett => assett.asset == asset)
        this.value = this.$store.state.wallet_data[index].percentage_to_sell
        this.asset_chosen_index = index
       }
       console.log(asset)
       
     }
   },
  //  watch:{
  //    "$store.state.global_sell_percentage": function(){
  //      console.log("Watcher: $store.state.global_sell_percentage")
  //      this.value = this.$store.state.global_sell_percentage
  //    }
  //  }
 
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.merge-tooltip {
      position: absolute;
      right: 30px;
      top: 50%;
      transform: translate(75px, -50%);
    }

.merge-tooltip-percentage {
      position: absolute;
      left: -25px;
      top: 50%;
      transform: translate(-105px, 50%);
}
.tooltip-left{
  text-align: center;
  width: 35px;
  font-size: 12px;
  position: absolute;
  right: -6px;
  top: -10px;
  padding: 0.2rem;
  border-radius: 1rem;
  background: var(--main-color);
  color: black;
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
}

.tooltip-right{
  text-align: center;
  width: 35px;
  font-size: 12px;
  position: absolute;
  left: 28px;
  top: -10px;
  padding: 0.2rem;
  border-radius: 1rem;
  background: var(--main-color);
  color: black;
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
}

.icon-list{
  position: absolute;;
  /* background-color: blueviolet; */
  height: 100%;
  top:0px;
  right: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* align-content: center; */
  overflow:scroll; 
  overflow-x: hidden;

}
.icon-list::-webkit-scrollbar {
  display: none;
}
/* Hide scrollbar for IE, Edge and Firefox */
.icon-list{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
   
}

.asset-selected{
   box-sizing: border-box;
    -moz-box-sizing: border-box;
    -webkit-box-sizing: border-box;
  /* position:relative;
  left:-60px; */
  border:3px solid var(--main-color);
  /*
 margin: 0px;
 width: 100px; */
}
/* 
.asset-unselected{
  position:relative;
  left: 0px;
} */

.asset-name{
  font-weight: bold;
  left:0px;
  width:100%;
  margin: 0px;
  position: absolute;
  text-align: center;
}

.logo{ 
  /* */
}
/* 
.icon-list > div{
  margin:auto;
}
   */
</style>
