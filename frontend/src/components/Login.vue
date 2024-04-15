<template>
  <div class="blur"  @click.self.prevent="$store.commit('toggleLogin')" >
      <div class=" content" >
       
          <div class="headings">
              <h1 class="title">Insert API Keys </h1>
          </div>
         
         <div class="body">
              <div class="inputs">
                
                <input v-model="keys.api_key" type="text" name="api-key" id="api-key" placeholder="API KEY">
                <input v-model="keys.api_secret" type="text" name="api-secret" id="api-secret"  placeholder="API SECRET">
            </div>
         </div>
        
         
            <button @click="saveAPIKeys()" class="swap-button confirm-button" role="button">
                    <div v-if="loading == false">
                        Save API Keys
                    </div>
                    <div v-else> Saving Keys </div>

                    
                    </button>
         
        </div>

         
      </div>

 
</template>

<script>
export default {
  data(){
    return{
      loading: false,
      keys:{
          api_key: "",
          api_secret: ""
      }
    }
  },
  created(){
      this.getAPIKeys()
  },
  methods:{
   saveAPIKeys(){
      this.loading = true
      this.$axios
        .post(this.$server + "/api/save-keys", {api_key: this.keys.api_key, api_secret: this.keys.api_secret} )
        .then( response => {
            console.log(response)
            this.loading = false
             this.$notify({
                          title: response.data.message,
                          text: response.data.data
                        });
           
            this.$store.commit('toggleLogin')
           
            }
        ).catch(()=>{
             this.$notify({
                          title: "There was an error while saving keys",
                          text: ""
                        });
        });
   },
   getAPIKeys(){
      this.$axios
        .get(this.$server + "/api/get-keys" )
        .then( response => {
            console.log(response)
            this.keys = response.data.keys
            
            }
        ).catch(()=>{
             this.$notify({
                          title: "There was an error while getting keys",
                          text: ""
                        });
        });
   }
    
  }

}
</script>

<style>


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
  /* height:700px; */
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
  /* margin-top: auto; */
  
}

.trade-data{
  display: flex;
  justify-content: space-around;
  flex-wrap:wrap
}

.headings{
  width: 100%;
  display: flex;
  margin: 1rem;
  /* justify-content: center; */
}
.headings h1{
  display:inline;
  margin:auto;

}

.body{
    flex-grow: 1;
}

.inputs{
   

}

.inputs > input{
    display: block;
    padding: 1rem 2rem;
    margin: 2rem auto;
    box-sizing: border-box;
    width: 100%; 
    border: 2px solid var(--main-color);
    border-radius: 1rem;
    outline: none;
    font-size: 1.2rem;

    background: var(--secondary-color);
	-webkit-backdrop-filter: blur(5px);
	backdrop-filter: blur(5px);
  box-shadow: rgba(0, 0, 0, 0.45) 0px 25px 20px -20px;
  
}

#api-secret{
   
}


</style>