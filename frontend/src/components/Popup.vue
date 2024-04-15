<template>
  <div class="blur" @click.self.prevent="$store.commit('togglePopup')" >
      <div class=" content" >
        <div class="trade-data">
          <div class="headings">
              <h3 class="title">Sell ({{$store.state.sell_assets.length}})</h3>
              <h3 @click="reverseBuySell()" class=" reverse-arrows">&#8651;</h3>
            <h3 class="title">Buy ({{$store.state.buy_assets.length}})  </h3>
          </div>
         
          <div class="sell"> 
           
            <div class="asset" v-for=" asset in $store.state.sell_assets" :key="asset.asset">
              <div class="asset-name">

                  <img  :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">
              <div class="asset-name"> {{asset.asset}} </div>
              </div>
            
              <div class="info">
                <p> {{$number( asset.asset_amount) }}  {{asset.asset}} </p>
                <p> {{$number(asset.asset_amount_to_usd)}} USD </p>
                <p> {{$number(asset.asset_percentage)}} % </p>
              </div>
            </div>
          </div>

          <div class="buy">
           <div class="asset" v-for=" asset in $store.state.buy_assets" :key="asset.asset">
              <div class="asset-name">

                  <img  :src="$server + '/static/'+ asset.asset.toLowerCase()  +  '.svg'" alt="">
              <div class="asset-name"> {{asset.asset}} </div>
              </div>
            
              <div class="info">
                <p> {{$number( asset.asset_amount) }}  {{asset.asset}} </p>
                <p> {{$number(asset.asset_amount_to_usd)}} USD </p>
                <p> {{$number(asset.asset_percentage)}} % </p>
              </div>
            </div>
          </div>
        </div>

         <button @click="confirmSwap()" class="swap-button confirm-button" role="button">
           <div v-if="loading == false">
             Confirm Swap (${{$number($store.state.sell_amount)}})
           </div>
           <div v-else> Contacting Binance... </div>

          
         </button>
      </div>

  </div>
</template>

<script>
export default {
  data(){
    return{
      loading: false
    }
  },
  methods:{
    confirmSwap(){
      if(this.loading == false){
        this.$axios
        .post(this.$server + "/api/swap", {sell: this.$store.state.sell_assets,
                                            buy: this.$store.state.buy_assets} )
        .then( response => {
            console.log(response)
            this.loading = false
             this.$notify({
                          title: response.data.message,
                          text: response.data.errors,
                          errors: response.data.errors
                        });
            this.$store.commit("setSwapResponse", response.data)
            this.$store.commit('togglePopup')
            //this.$store.commit("setWalletData", response.data)
            }
        ).catch((error) => {
           this.$notify({
                          title: error.data.message,
                          text: error.data.errors,
                          errors: error.data.errors
                        });
            this.$store.commit("setSwapResponse", error.data)
            this.$store.commit('togglePopup')
        });

        this.loading = true

      }
      
    },
    reverseBuySell(){
        // this.$store.commit("reverseBuySell")
    }
  }

}
</script>

<style scoped>


.blur{
    position: fixed;
    top:0;
    width:100%;
    height:100%;
    transition: 1s backdrop-filter linear;
    /* filter: blur(60px); */
   backdrop-filter: blur(30px);
    z-index: 100;
}
.content{
  width: 700px;
  height:700px;
  background-color: black;
  position: absolute;
  top: 50%;
  right: 50%;
  transform: translate(50%, -50%);
  margin: 0px;
 
  border-radius: 1rem;
  padding: 1rem;
  background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  /*   box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px; */
  border: 1px solid rgba(255,255,255,0.2);
  display: flex;
  flex-direction: column;

  text-align: center;
}

.confirm-button{
  display: block;
  margin: 1rem;
  margin-top: auto;
  
}

.trade-data{
  display: flex;
  justify-content: space-around;
  flex-wrap:wrap
}
.title{
  font-weight: bold;
  margin-top:0px;
  position: sticky;
  top: 0;

}
img{
  width: 60px;
}

.asset{
  display: flex;
  gap:1;
  justify-content: space-around;
  border-bottom: 2px solid gray;
}
.asset-name{
  font-weight: bold;
  align-self: center;
  margin:1rem;

}
.info{
  margin: 1rem 0rem;
  
}

.buy{
  border-left: 2px solid gray;
  flex: 1;
  padding: 1rem;
   height: 500px;
  flex: 1;
  padding: 1rem;
  padding-left: 0px;
  overflow: scroll ;
}
.sell{
  height: 500px;
  flex: 1;
  padding: 1rem;
  padding-right: 0px;
  overflow: scroll ;
  

}
/* Hide scrollbar for Chrome, Safari and Opera */
.sell::-webkit-scrollbar {
  display: none;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.buy::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.sell, .buy {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.headings{
  width: 100%;
  display: flex;
  margin: 1rem;
  /* justify-content: center; */
}
.headings h3{
  display:inline;
  margin:auto;

}
.reverse-arrows{
  font-size: 30px;
  font-weight: bolder;
  cursor: pointer;
}





</style>