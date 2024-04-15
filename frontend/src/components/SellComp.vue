<template>
<fragment>
  <div class="card left-card">
        <div class="card-heading">
         <h3 class="card-title">Sell</h3>
          <span>
            ( ${{$number($store.state.wallet_data.filter(asset => asset.selected == true).reduce((prev, cur) => { return prev +  cur.usd_value * cur.percentage_to_sell / 100  } ,0))}},
              {{($store.state.wallet_data.filter(asset => asset.selected == true).reduce((prev, cur) => { return prev +  cur.usd_value * cur.percentage_to_sell / 100  } ,0) / $store.state.wallet_data.reduce((prev, cur) => { return prev +  cur.usd_value } ,0) * 100).toFixed(1)}}%
           )
            </span>
         <span @click="$store.commit('selectAllForSell')" class="select-all ">Select All</span>
         <span @click="$store.commit('unselectAllForSell')" class="unselect-all ">Clear All</span>
  
  
        
        </div>  
        <div class="card-body"> 
         
           <div class="item list-item"
            @dblclick="$store.commit('forceSelectSellItem', index)"
            @click="$store.commit('toggleSellItem', index)"   
            v-for="(asset, index) in $store.state.wallet_data" 
            :key="asset.asset" 
            :class="{ 'item-selected' : asset.selected == true, 'item-to-buy' : asset.selected_to_buy == true, }"
           >
             <div class="item-column"> {{index}} </div>
            <img class="logo scale-up-center" :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">
            <div class="text " >
              <div class="coin-ticker" >{{asset.asset}}</div>
              <div class="coin-price" >${{$number(asset.coin_price)}}</div>
             </div>
            <div class="item-column"> {{$number(asset.percentage)}}%</div>
            <div class="item-column"> {{$number(asset.total)}} {{asset.asset}}</div>

            <div class="item-column "   >${{ $number(asset.usd_value)}}</div> <!-- style="filter: blur(4px);" -->
           <!-- <div class="item-column green">12%</div> -->

           <div class="item-column"> {{$number(asset.amount_to_sell)}}  </div>
           <div class="item-column"> {{$number(asset.amount_to_sell * asset.coin_price)}}  </div>

           <!-- <input v-on:keyup.enter="$store.commit('setPercentageOfSellAsset', index, values[index])" 
                    v-model="values[index]" :placeholder="$number(asset.percentage_to_sell)"
                      @click.stop="" class="item-column percent-input" type="text"  name="" id=""> -->

           <div  class="item-column"> {{$number(asset.percentage_to_sell)}}% </div>
           <!-- <div class="item-column " style="justify-item:flex-end"> &#10095; </div> -->
<!-- 
            <div v-if="index==0" class="item-column slidecontainer ">
              <input type="range" min="1" max="100" value="50" class="item-slider" id="myRange" orient="vertical">
            </div> -->

            <!-- <vue-slider class="coin-percent-slider" 
                        v-model="values"
                        :direction="'btt'"
                        :width="10"
                       
                         /> -->
 
           </div>
          </div> 
         
      </div>

      <general-slider class="general-slider"/>



 </fragment>


</template>

<script>
import GeneralSlider from './GeneralSlider.vue'
// import VueSlider from 'vue-slider-component'

export default {
  components: { GeneralSlider,    },
  props: ["assets_loaded"],
  data(){
    return{
      values: Array(20).fill(0)//[...this.$store.state.wallet_data.map(()=>0)]

    }
  },
  methods:{
    setPercentageOfSellAsset(index, value){
     this.$store.commit("setPercentageOfSellAsset", index, value)
    }
  },
  computed:{
  
  },
  watchers:{
    assets_loaded: function(oldVal, newVal) { 
      console.log("Assets Loaded", oldVal, newVal)
      this.values = Array(this.$store.state.wallet_data.length).fill(0)
    }
  }
  


}
</script>

<style scoped>
.item-to-buy{
  background-color: rgb(163, 163, 163);
  box-shadow: none;
}
.coin-percent-slider{
  position:relative;
  right: -10px;
  width: 100px;
  height: 100px;
}
.slidecontainer{
  position: absolute;
  padding-left: 2rem;
  right: -33px;
  height: 60px;
  /* background-color: red; */
}

.item-slider{
  width: 100%;
  height: 100%;
  writing-mode: bt-lr; /* IE */
  -webkit-appearance: slider-vertical; /* Chromium */
  display: none;
}
.slidecontainer:hover .item-slider{
  display: block;
}

.percent-input{
  font-size: 1rem;
   outline: none;
  width: 30px;
  height: 30px;
  background-color: none;
    background: transparent;
    border: none;
}
.card-heading{
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;;
}

</style>