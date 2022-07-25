<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Descripcion de los centros, que se hace, etc,<br>
      mas cosas.
      
    </p>
    <div id="app">
    <div id="nav">
      <router-link to="/home">Home</router-link> |
      <router-link to="/centers_map">Mapa centros</router-link> |
      <router-link to="/create_center">Create Center</router-link> |
      <router-link to="/select_tipos">Select Tipos</router-link> |
      <router-link to="/turnos">Turnos</router-link> |
      <router-link to="/estadisticas">Estadisticas </router-link> 
      <router-link to="/register_turn">sacar turno</router-link> |
    </div>
      <router-view>
      </router-view>
    </div>
  
   </div>
</template>

<script>
export default {
  name: 'HelloWorld',
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
