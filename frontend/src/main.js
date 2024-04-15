import Vue from 'vue'
import App from './App.vue'
import Fragment from 'vue-fragment'
import Axios from 'axios'
import HRNumbers from "human-readable-numbers"
import Vuex from  "vuex"
import Notifications from 'vue-notification'
 

Vue.use(Vuex) 
Vue.use(Notifications)


const store = new Vuex.Store({
  state: {
    wallet_data: [],
    sell_amount: 0,
    global_sell_percentage: 0,
    show_popup: false,
    show_login: false,
    sell_assets: [],
    buy_assets: [],
    swap_response:{}
  },
  mutations: {
    setWalletData (state, data) {
      state.wallet_data = data
      // Add "selected" property this way so that the data is reactive ss
      for(let i=0; i < state.wallet_data.length; i++){
        Vue.set(state.wallet_data[i], 'selected', false)
        Vue.set(state.wallet_data[i], 'selected_to_buy', false)
        Vue.set(state.wallet_data[i], 'amount_to_sell', 0)
        Vue.set(state.wallet_data[i], 'percentage_to_sell', 0)
        Vue.set(state.wallet_data[i], 'amount_to_buy', 0)
        Vue.set(state.wallet_data[i], 'percentage_to_buy', 0)
      }
    },
    toggleSellItem(state, index){
      if ( state.wallet_data[index].selected_to_buy == false){  
        state.wallet_data[index].selected = !state.wallet_data[index].selected;
        state.wallet_data = [...state.wallet_data]
      }
      if ( state.wallet_data[index].selected == false){  
        state.wallet_data[index].amount_to_sell = 0
        state.wallet_data[index].percentage_to_sell = 0
        console.log("toggleSellItem")
      }

    },
    forceSelectSellItem(state, index){
      state.wallet_data[index].selected = true
      state.wallet_data[index].selected_to_buy = false
      state.wallet_data = [...state.wallet_data]

    },
    toggleBuyItem(state, index){
      if ( state.wallet_data[index].selected == false){  
        state.wallet_data[index].selected_to_buy = !state.wallet_data[index].selected_to_buy;
        state.wallet_data = [...state.wallet_data]
      }
    },
    forceSelectBuyItem(state, index){
      state.wallet_data[index].selected = false
      state.wallet_data[index].selected_to_buy = true
      state.wallet_data = [...state.wallet_data]

    },
    setSellAmount(state, amount){
        state.sell_amount = amount
    },
    setGlobalSellPercentage(state, percent){
      state.global_sell_percentage = percent
     
    },
    setAmountToSellOfCoins(state){
      console.log("setAmountToSellOfCoins")
      state.wallet_data.forEach((asset) => {
        if(asset.selected == true){
          asset.amount_to_sell = asset.total * state.global_sell_percentage/100;
          asset.percentage_to_sell = state.global_sell_percentage
        }
        
      })
    },
    setAmountToBuyOfCoins(state, data){
      console.log("setAmountToBuyOfCoins", data.value, data.coins, Array.isArray(data.value))
      state.buy_assets = []
      if ((Array.isArray(data.value) && data.value.length >=2) || data.coins.length >= 2 ){
        let value = []
        if(!Array.isArray(data.value) ){

          value = [data.value]
        }else{
           value = [...data.value]
        }
       
        value.unshift(0)
        value.push(100)
        value = value.map((curr, i, array) => {
          return array[i+1] -array[i]
          })
        value.pop()
        console.log(value)
        let assets = value.map((el,i) => {
          return { asset: data.coins[i] , percentage: el}
        })
        console.log("Assets ",assets)
       
        let buy_assets = []
        for(let i =0 ; i < assets.length;i++){
          let obj = assets[i]
          let asset = state.wallet_data.find((el)=> el.asset == obj.asset.toUpperCase())
          //console.log("Indexes",index,obj.asset.toUpperCase(),state.wallet_data)
          //let asset = state.wallet[index]
          

            buy_assets.push({
              asset: obj.asset.toUpperCase(),
              asset_amount: (state.sell_amount * obj.percentage/100) / asset.coin_price ,
              asset_amount_to_usd:  state.sell_amount * obj.percentage/100,
              asset_percentage: obj.percentage
            })
        }

        state.buy_assets = [...buy_assets]
      }
      else{
        console.log("One coin to buy")
        let asset = state.wallet_data.find((el)=> el.asset == data.coins[0].toUpperCase())
        state.buy_assets = [{
          asset: asset.asset,
          asset_amount:state.sell_amount / asset.coin_price ,
          asset_amount_to_usd:  state.sell_amount ,
          asset_percentage: 100
        }]
      }

    
      console.log("buy_assets",state.buy_assets)
      

    },
    setPercentageOfSellAsset(state, data){
      console.log(data.value)
      state.wallet_data[data.index].percentage_to_sell = data.value
      state.wallet_data[data.index].amount_to_sell = state.wallet_data[data.index].total * data.value/100 
    },
    togglePopup(state){
      state.show_popup = !state.show_popup
      if( state.show_popup == true){
         document.documentElement.style.setProperty("overflow", "hidden");
      }else{
        document.documentElement.style.setProperty("overflow", "scroll");
      }
    },
    toggleLogin(state){
      state.show_login = !state.show_login
      if( state.show_login == true){
         document.documentElement.style.setProperty("overflow", "hidden");
      }else{
        document.documentElement.style.setProperty("overflow", "scroll");
      }
    },
    setSellAssetsList(state){
      state.sell_assets = state.wallet_data.filter((asset) => asset.selected == true).map((asset) => {
        return {
          asset: asset.asset,
          asset_amount: asset.total * asset.percentage_to_sell/100,
          asset_amount_to_usd:  asset.usd_value * asset.percentage_to_sell/100,
          asset_percentage: asset.percentage_to_sell
        }
      })
      state.sell_assets = [...state.sell_assets]
      // console.log(state.sell_assets)
    },
    reverseBuySell(state){
      let temp = state.sell_assets
      state.sell_assets = state.buy_assets
      state.buy_assets = temp

    },
    selectAllForSell(state){
      state.wallet_data.forEach((asset) => { 
        if(asset.selected_to_buy == false){ 
          return asset.selected = true 
        }
      })
    },
    unselectAllForSell(state){
      state.wallet_data.forEach((asset) => {
        asset.selected = false
        asset.percentage_to_sell = 0
        asset.amount_to_sell = 0
      })
    },
    selectAllForBuy(state){
      state.wallet_data.forEach((asset) => { 
        if(asset.selected == false){ 
          return asset.selected_to_buy = true 
        }
      })
      state.wallet_data = [...state.wallet_data]
    },
    unselectAllForBuy(state){
      state.wallet_data.forEach((asset) => asset.selected_to_buy = false)
    },
    setSwapResponse(state, response){
      state.swap_response = response
    }
  }
})
Vue.prototype.$store = store


Vue.prototype.$axios = Axios;
// Server URL
Vue.prototype.$server = 'http://127.0.0.1:5000'
Vue.prototype.$number = HRNumbers.toHumanString;

Vue.use(Fragment.Plugin)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
