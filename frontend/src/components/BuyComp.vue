<template>
<fragment>
  

   <div class="card right-card">
     
      
      <div class="card-heading">
         <h3 class="card-title ">Buy</h3>
          <span @click="$store.commit('selectAllForBuy')" class="select-all ">Select All</span>
         <span @click="$store.commit('unselectAllForBuy')" class="unselect-all ">Clear All</span>
  
  
        </div>
        <div class="card-body"> 
          
           <div class="item  list-item" @dblclick="$store.commit('forceSelectBuyItem', index)"
                                        @click="$store.commit('toggleBuyItem', index)"   
                                        v-for="(asset, index) in $store.state.wallet_data" :key="asset.asset" 
                                        :class="{ 'item-for-sale' : asset.selected == true,  'item-selected' : asset.selected_to_buy == true  }"
                                        >
            <!-- <div v-if=" asset.selected == true" class="blur-item"></div> -->
             <!-- <div class="item-column"> {{index}}  </div> -->
            <img class="logo scale-up-center" :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">
            <div class="text" >
              <div class="coin-ticker" >{{asset.asset}}</div>
              <div class="coin-price" >${{$number(asset.coin_price)}}</div>

             </div>
             <!-- <div class="item-column"> 0 </div>  -->
           
            
           </div>

          <div class="" >
            <input class="coin-add" type="text" placeholder="Add Coin" name="" id="">
           </div>
          
          </div> 

        
           
      </div>

       <multi-slider class="multi-slider" />

 </fragment>


</template>

<script>
import MultiSlider from "./MultiSlider.vue"

export default {
  components: {  MultiSlider },

}
</script>

<style scoped>
.item-for-sale{
  background-color: rgb(160, 160, 160);
  box-shadow: none;
 
}
.card-heading{
  margin-bottom: 1rem;;
}
/* .blur-item{
  position: absolute;
  top: 0rem;
  width: 100%;
  height: 100%;
  background-color: rgb(255, 253, 253, 0.1);;
  backdrop-filter: blur(4px);
  z-index: 1000;

} */
</style>