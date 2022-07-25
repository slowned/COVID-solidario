<template>
 <div>
 <b-jumbotron>
    <h2> Tipos de centro </h2> 
    <b-button variant="success" @click="getData">Recargar Estadistica</b-button> 
    <ve-pie :data="chartData"></ve-pie>
</b-jumbotron>
</div>

</template>

<script>
import axios from 'axios';

const DATA_FROM_BACKEND = {
    columns: ['nombre', 'cantidad'],
    rows: []
      
  }

const EMPTY_DATA = {
    columns: ['nombre', 'cantidad'],
    rows: []
      
  }



  export default {
    name:'Estadistica1',
    mounted() {
        this.getData()
    },
    created() {
      axios.get(process.env.VUE_APP_BACKEND +'/tiposCentro')
      .then(response => {
        this.dat= response.data.centros
        DATA_FROM_BACKEND.rows= response.data.centros
        this.getData()
      })
      .catch(e => {
        this.api_errors.push(e)
      })
    },
    data () {
      return {
        dat:null,
        array:[],
        centros:[],
        chartData: DATA_FROM_BACKEND,
        loading: false,
        dataEmpty: false
            
        
      }
    },
      methods: {
      
      getData () {
        this.loading = true
        setTimeout(() => {
          this.chartData = this.chartData.rows.length
            ? EMPTY_DATA
            : DATA_FROM_BACKEND
          this.dataEmpty = !this.chartData.rows.length
          this.loading = false
        }, 1000)
      }
    },
 



    




        
  

    // Fetches posts when the component is created.
  
  }


</script>

