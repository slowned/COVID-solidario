<template>
 <div>
 <b-jumbotron>
    <h2> Turnos mas concurridos </h2>
    <b-button variant="success" @click="getData">Recargar Estadistica</b-button> 
    <ve-bar :data="chartData" :settings="chartSettings"></ve-bar>
</b-jumbotron>
</div>

</template>

<script>
import axios from 'axios';

const DATA_FROM_BACKEND = {
    columns: ['hora_inicio', 'cantidad'],
    rows: []
      
  }

const EMPTY_DATA = {
    columns: ['hora_inicio', 'cantidad',],
    rows: []
      
  }



  export default {
    name:'Estadistica4',
    mounted() {
        this.getData()
    },
    created() {
      axios.get(process.env.VUE_APP_BACKEND +'/estadisticas/turnos-concurridos/')
      .then(response => {
        this.dat= response.data.turns
        DATA_FROM_BACKEND.rows= response.data.turns
    this.getData()
 
        
      })
      .catch(e => {
        this.api_errors.push(e)
      })
    },
    data () {

    
      this.chartSettings = {
        dimension: ['hora_inicio'],
        metrics: ['cantidad']
      }
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
        // ajax get data ....
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
