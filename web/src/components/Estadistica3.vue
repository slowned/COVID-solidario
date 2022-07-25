<template>
 <div>
 <b-jumbotron>
    <h2> Turnos mas concurridos </h2> 
    <ve-bar :data="chartData" :settings="chartSettings"></ve-bar>
</b-jumbotron>
</div>

</template>

<script>
import axios from 'axios';

  export default {
    name:'Estadistica3',
    data () {
      this.chartSettings = {
        dimension: ['hora_inicio'],
        metrics: ['cantidad']
      }
      return {
        chartData: {
          columns: ['hora_inicio', 'cantidad',],
          rows: [],
        },
      }
    },
    created: function () {
      this.fetchRecurrentTurns();
    },
    methods: {
      fetchRecurrentTurns: function () {
        let BACK_URL = process.env.VUE_APP_BACKEND;
        let url = `${BACK_URL}/estadisticas/turnos-concurridos/`;
        axios
          .get(url)
          .then(response => {
            this.chartData.rows = response.data.turns;
          })
          .catch(e => {
            console.log(e);
          });
      },
    },
  }
</script>

