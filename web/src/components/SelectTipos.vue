<template>
            <div>
              <label>Tipo:*</label>
              <select class="form-control custom-select" v-on:click="selectType" v-model="tipo" required>
                <option value="">Seleccione un tipo</option>
                <option v-for="item in tipos" v-bind:key="item.id">{{ item.nombre }}</option>
              </select>
            </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SelectTipos',
  data(){
    return {
      tipo :"",
      tipos:[],
      api_errors:[],
    }
  },
  // Fetches posts when the component is created.
  created() {
    axios.get(process.env.VUE_APP_BACKEND +'/centros/tipos')
    .then(response => {
      // JSON responses are automatically parsed.
      this.tipos = response.data.tipos
    })
    .catch(e => {
      this.api_errors.push(e)
    });
  },
  methods:{
    selectType() {
      this.$store.commit('selectTipoCentro', this.tipo);
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

