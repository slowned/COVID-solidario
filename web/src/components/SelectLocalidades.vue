<template>
            <div>
              <label>Municipio:*</label>
              <select class="form-control custom-select" v-on:click="selectMunicipio" v-model="municipio" required>
                <option value="">Seleccione un Municipio</option>
                <option v-for="item in apiMunicipiosPayload" v-bind:key="item.id">{{ item.name }}</option>
              </select>
            </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'SelectLocalidades',
    computed: {
        apiMunicipiosPayload() {
            return this.$store.state.apiMunicipiosPayload;
        },
    },
    data(){
    return {
        municipio:"",
        //localidades:[],
        api_errors:[],
        required:true,
    }
    },
    // Fetches posts when the component is created.
    created() {
      axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135')
      .then(response => {
          // JSON responses are automatically parsed.
          this.$store.commit('setApiMunicipiosPayload', response.data.data.Town);
      })
      .catch(e => {
          this.api_errors.push(e)
      });
    },
    methods:{
      selectMunicipio() {
          this.$store.commit('selectMunicipio', this.municipio);
      },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
  width:100%;
  text-align: center;
  min-height: 1em;
}
input, select {
  width:100%;
  text-align: center;
  min-height: 3em;
}
</style>

