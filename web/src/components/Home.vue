<template>

<main>
  
  <b-jumbotron> 
       <h1>{{ msg }} Centros de Ayuda Covid-19</h1>

       <p>
      Descripcion de los centros, que se hace, etc,<br>
      mas cosas.
      
    </p>
  </b-jumbotron>
  <b-jumbotron> 
<b-card-group deck >

<div class="col-sm-3">
  <b-card
    title="Nuestros centros"
    
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem;"
    class="mb-2"
  >
    <div style="font-size: 4rem;"> 
      <b-icon icon="map-fill" aria-label="Help" variant="info"></b-icon>
    </div>
    <b-card-text>

      Ingrese para ver un mapa con todos nuestros centros activos.
      
    </b-card-text>

    <b-button href="/centers_map" variant="primary">Ver mapa</b-button>
  </b-card>
</div> 

<div class="col-sm-3">
  <b-card
    title="Solicitar alta de centro"
    
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem;"
    class="mb-2"
  >
    <div style="font-size: 4rem;"> 
      <b-icon icon="card-checklist" aria-label="Help" variant="info"></b-icon>
    </div>
    <b-card-text>

      Ingrese aqui para solicitar el alta de un nuevo centro.
      
    </b-card-text>

    <b-button href="/create_center" variant="primary">Cargar centro</b-button>
  </b-card>
</div> 


<div class="col-sm-3">
  <b-card
    title="Turnos"
    
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem;"
    class="mb-2"
  >
    <div style="font-size: 4rem;">  
    <b-icon icon="alarm-fill" class="border border-info rounded p-2" variant="info"></b-icon>
    </div>
        <b-card-text>
        
      Solicite un turno en su centro mas cercano
      
    </b-card-text>

    <b-button href="/centers_map" variant="primary">Reservar turno</b-button>
  </b-card>
</div> 

<div class="col-sm-3">
  <b-card
    title="Estadisticas"
    
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem;"
    class="mb-2"
  >
    <div style="font-size: 4rem;"> 
      <b-icon icon="exclamation-circle-fill" variant="primary" aria-label="Help"></b-icon>
    </div>
    <b-card-text>

      Informese sobre el estado actual de nuestros centros
      
    </b-card-text>
    
    <b-button href="/estadisticas" variant="primary">Ver nuestras estadisticas</b-button>
  </b-card>

</div>  
</b-card-group>
    
    
  
</b-jumbotron> 
</main>
</template>

<script>
export default {
  name: 'Home',
  props: {
    msg: String
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
