<template>
<div class="container mt-4" style="background-color:#aaa">
  <div style="height: 500px; width: 100%">
    
    <div style="height: 200px overflow: auto;">
      <p>Seleccione la ubicacion del centro</p>

    
    </div>
    <l-map
      v-if="showMap"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      style="height: 80%"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
      @click="addPoint"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      
    
       <l-marker v-for="(point,index) in points" :lat-lng="point" v-bind:key="index">
       
       
       </l-marker>
        

    </l-map>
  </div>
</div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";



export default {
  name: "CenterCreateMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    
    
    
    
    
  },
   
  
  data() {
    return {
      zoom: 6,
      center: latLng(-36.701, -60.200),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 11.5,
      currentCenter: latLng(-36.701, -60.200),
      showParagraph: false,
      points: [[-36.701, -60.200]],
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
    },
    removePoint(point) {
       const index = this.points.indexOf(point);
       this.points.splice(index, 1);

    },
    addPoint(point) {
        this.points.splice(0, 1);
        this.points.push(point.latlng);
        this.$store.commit('selectCoordinates', point.latlng);
    },
  }
};


 
      
</script>