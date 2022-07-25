<template>
<main class="container">
  <div>
    <b-jumbotron>

      <h2> Estadisticas </h2>
    </b-jumbotron>
    <div>
      <Estadistica1/>
      <Estadistica2/>
      
      <Estadistica4/>
    </div>
  </div>
</main>
</template>

<script>
import Estadistica1 from "./Estadistica1";
import Estadistica2 from "./Estadistica2";
// import Estadistica3 from "@/components/Estadistica3";
import Estadistica4 from "./Estadistica4";

export default {

  name: 'Estadisticas',
  components: {
    Estadistica1,
    Estadistica2,
//    Estadistica3,
    Estadistica4,
  },
  data(){
    return {
      tipo : "",
      centros:[],
      status:"",
    }
  },
}

</script>
