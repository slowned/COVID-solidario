<template>
<div>

<p> Centros</p>

</div>

</template>



<script>
import axios from 'axios';

export default {
  name: 'Centers',
  data(){
    return {
      tipo : "",
      centros:[],
      status:"",
    }
  },
  // Fetches posts when the component is created.
  mounted() {
    axios.get(process.env.VUE_APP_BACKEND +'/centros')
    .then(response => {
      // JSON responses are automatically parsed.
      this.centros = response.data.centros
    })
    .catch(e => {
      this.api_errors.push(e)
    });
  },
  methods:{
    selectType() {
      this.tipo="algo";
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
@import "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";
@import "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css";

.col-6{
  margin: 0 auto;
}
.formFix{
  margin: 0 auto;
}
.form-group{
  width:100%;
}

.row{
    box-sizing: border-box;    
}
.col{
    box-sizing: border-box;    
}

label {
  width:30%;
  text-align: left;
}
input, select {
  width:70%;
}

</style>



