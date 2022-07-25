<template>
<div class="container" style="background-color:#aaa">
  
  <b-jumbotron>  
    <div style="height: 200px overflow: auto;">
      <h1>Encontrá tu centro habilitado más cercano </h1>

    
    </div>
   </b-jumbotron>
   <div style="height: 600px; width: 100%">
    <l-map
      v-if="showMap"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      style="height: 100%"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      
    
       <l-marker v-for="(centro,index) in centros" :lat-lng="centro.position" v-bind:key="index">
        <l-popup>
          <div>
            {{centro.nombre}}
            <p> Direccion: {{centro.direccion}} </p> 
            <p>Horario: {{centro.hora_apertura}} - {{centro.hora_cierre}} </p>
            <p>Telefono: {{centro.telefono}}  </p>
            <router-link :to="{name: 'RegisterTurn', params: {center_id: centro.pk}}">Reservar Turno</router-link>
          </div>
        </l-popup>
       </l-marker>
     
    


    </l-map>
 
  </div>
</div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";


import axios from 'axios';

export default {
  name: "CentersMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    
    
    
  },
    // Fetches posts when the component is created.
  mounted() {
    axios.get(process.env.VUE_APP_BACKEND +'/centros/all')
    .then(response => {
      // JSON responses are automatically parsed.
      this.centros = response.data.centros
    })
    .catch(e => {
      this.api_errors.push(e)
    });
  },
  
  data() {
    return {
      zoom: 6.2,
      center: latLng(-36.701, -60.200),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      withPopup: latLng(-34.9187, -57.956),
      withTooltip: latLng(-34.8187, -57.956),
      currentZoom: 11.5,
      currentCenter: latLng(-34.9187, -57.956),
      showParagraph: false,
      points: [[-34,-57,"ejemplo1"],[-33,-57,"ejemplo2"]],
      centros:[],
      mapOptions: {
        zoomSnap: 0.5
      },
      showMap: true
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },
    innerClick() {
      alert("Click!");
    }
  }
};


 
      
</script>
