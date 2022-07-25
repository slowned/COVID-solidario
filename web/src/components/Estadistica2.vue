<template>
  <div>
    <b-jumbotron>
      <h2> Centros por Localidad </h2> 
      <b-button variant="success" @click="getData">Recargar Estadistica</b-button> 
      <ve-bar
        :data="chartData">
      </ve-bar>
    </b-jumbotron>
  </div>
</template>

<script>
import axios from 'axios';

const DATA_FROM_BACKEND = {
    columns: ['localidad', 'cantidad_centros'],
    rows: [] 
  }

const EMPTY_DATA = {
    columns: ['localidad', 'cantidad_centros'],
    rows: []
  }


  export default {
    name:'Estadistica2',
    mounted() {
        this.getData()
    },
    created() {
        axios.get('https://admin-covid-solidario.com.ar/estadisticas/centros/por/localidad')
  //    axios.get(process.env.VUE_APP_BACKEND +'/centros/all')
       // axios.get('http://:5000/tiposCentro')
      .then(response => {
        // JSON responses are automatically parsed.
       
        //this.chartData.rows = response.data.centros
        this.dat= response.data.stats
        DATA_FROM_BACKEND.rows= response.data.stats
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
  }
</script>
