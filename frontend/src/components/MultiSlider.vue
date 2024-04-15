<template>
  <div  >
    <vue-slider
               class="slider" 
               :class='{"show-slider": this.$store.state.wallet_data.filter(asset => asset.selected_to_buy == true).length >= 2 }'
               ref="slider"
               v-model="value"
               :order="true"
               :process="processes"
               :tooltip-formatter="formatter"
               :enable-cross="true"
               :tooltip="'always'"    
               :direction="'ttb'"
               :height="'90%'"
               :width="10"
               :contained="false"
              
              
               
              
              
    >
    <template v-slot:process="{ style, index }">
          <div class="vue-slider-process" :style="style">
            <div :class="[
              'merge-tooltip',
            ]">
              <!-- {{ value[index] }} - {{ value[index + 1] }} -->
              <img class="logo scale-up-center" :src="$server + '/static/'+ coins[index]  +  '.svg'" style="width:30px;" >
            </div>
          </div>

         <div class="vue-slider-process" :style="style">
           
            <div :class="[
              'merge-tooltip-percentage',
            ]" >
            
            <div class="tooltips">
            <!-- Percentage -->
            <div v-if="!Array.isArray(value)">
                 
                 
                  <div v-if="index==0">{{100 -value}}%</div>
                   <div v-else>  {{ value}}%</div>
               
            </div>
            <div v-else-if="isNaN(value[index - 1])" >
              {{ value[index] }}%
            </div>
            <div v-else-if="isNaN(value[index ])">
               {{ 100 - value[index -1] }}%
            </div>
            
            <div v-else>
               {{ value[index] -  value[index - 1] }}%
            </div>
             </div>  
          
            
            <!-- Amount -->
             <div class="tooltips">
            <div v-if="!Array.isArray(value)">
                
                  <div v-if="index==0">  ${{ $number($store.state.sell_amount - $store.state.sell_amount * value / 100) }} </div>
                   <div v-else>  ${{ $number($store.state.sell_amount * value / 100 )}} </div>
               
            </div>
            <div v-else-if="isNaN(value[index - 1])" >
              ${{ $number( value[index] /100  * $store.state.sell_amount) }}
              <!-- {{$store.state.sell_amount * value[index] /100}} -->
            </div>
            <div v-else-if="isNaN(value[index ])">
               ${{ $number( $store.state.sell_amount  - value[index-1] /100  * $store.state.sell_amount ) }}
            </div>
            
            <div v-else>
               ${{ $number( value[index] /100  * $store.state.sell_amount -  value[index-1] /100  * $store.state.sell_amount ) }}
            </div>
            <!-- <div class="tooltip-right">
              {{$number($store.state.sell_amount * value / 100)}}
            </div> -->
             </div>
              </div>
          </div>

        </template>
     <template #tooltip="{ index }">
        <div v-if="index === 1">
          <!-- <img src="../../public/aave.svg" style="width:30px;" > -->
          </div>
        <div v-else></div>
      </template>
    
    </vue-slider>
  
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import { debounce } from "debounce";



export default {
  name: 'MultiSlider',
  components: {
    VueSlider
  },
   data: function () {
      return {
        toggle: true,
        toggle_amount: true,
        value: [50],
        formatter: '{value}%',
        
        coins: []
      }
     

      }, 
      created(){
        this.$root.$on('swapButtonClicked', () => {
            this.$store.commit("setAmountToBuyOfCoins", { value: this.value, coins: this.coins })
        })
      },
      methods: {
        processes: function(dotsPos){
          let processes = []
          
          if (Array.isArray(this.value) && this.value.length >= 2){
              processes.push([0, dotsPos[0], { backgroundColor: 'gray' }])
              for(let i=0; i < this.value.length - 1; i++){  
                processes.push([dotsPos[i], dotsPos[i+1], { backgroundColor: i%2==0? 'var(--main-color)' : "gray" }])
              }
              processes.push([dotsPos[this.value.length - 1], 100, { backgroundColor: this.value.length%2!=0? 'var(--main-color)' : "gray" }]) 
          }
          else{
            
             processes.push([0, dotsPos[0], { backgroundColor: 'gray' }])
             processes.push([dotsPos[0],100, { backgroundColor: 'var(--main-color)'}])
             
          }
          return processes
        },
        
       
       
      },
      //   computed:{
      //     sell_amount: function(){
      //       return this.$store.state.wallet_data.filter(asset => asset.selected == true).reduce((prev, cur) => { return prev +  cur.usd_value * value / 100  } ,0)
          
      //     }
      //   },
        watch:{
         
          "$store.state.wallet_data": debounce(function () {
              let selected_assets = this.$store.state.wallet_data.filter(asset => asset.selected_to_buy == true && asset.selected != true )

              //console.log(this.$store.state.wallet_data.filter(asset => asset.selected_to_buy == true).map((asset, index)=> 20 * index))
              let value = selected_assets.map((asset ,index) => ((100 / (selected_assets.length)) * (index +1)).toFixed(0))
              value.pop()
              this.coins = selected_assets.map((asset) => asset.asset.toLowerCase())
              //this.onChange(value, this.coins)
              this.$refs.slider.setValue(value)
              console.log(value)

                // if (Array.isArray(value) && ( value.length == 1) ){
                //   this.$refs.slider.setValue([50])
                // }
                // else{
                //   this.$refs.slider.setValue(value)
                // }

          }, 20)
        }
  
 
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.merge-tooltip {
      position: absolute;
      right: 30px;
      top: 50%;
      transform: translate(15px, -50%);
    }

.merge-tooltip-percentage {
      position: absolute;
      right: -25px;
      top: 50%;
      transform: translate(15px, -50%);
}
.tooltips{
  margin-top:0.2rem;
  background-color: aquamarine;
  position:relative;
  left: 10px;
  text-align: center;
  width: 35px;
  font-size: 12px;
  padding: 0.2rem;
  border-radius: 1rem;
  background: var(--main-color);
  color: black;
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
}



</style>
