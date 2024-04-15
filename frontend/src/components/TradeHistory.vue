<template>
      
<div class="history" >
  <div class="card history-card ">
        <div class="card-heading">
         <h3 class="card-title">Trade History</h3>
        </div>
        <div class="card-body"> 
          
           <div class="item  list-item" v-for="i in [1,2,3,4]" :key="i">
            <div class="history-date item-column"> 15/02/1999 </div>
            <div class=" ">
                <img class="logo swap-asset scale-up-center" src="../../public/dot.svg" alt="">
                <img class="logo swap-asset scale-up-center" src="../../public/btc.svg" alt="">
                <img class="logo swap-asset scale-up-center" src="../../public/eth.svg" alt="">
            </div>
            <div class="arrow item-column">&rarr;</div>
           <div class="history-assets">
                <img class="logo swap-asset scale-up-center" src="../../public/matic.svg" alt="">
                <img class="logo swap-asset scale-up-center" src="../../public/ada.svg" alt="">
               
            </div>
           
            <div class="item-column">30%</div>
            <div class="item-column">$250</div>
           

           </div>
          </div> 
         
        
           
      </div>
</div>
</template>