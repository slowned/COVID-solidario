<template>
<div id="app">
  <header>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <div class="container">
          <b-navbar-nav :class="'container-fluid'">
            <b-nav-item href="/"><img alt="Vue logo" src="./assets/logo.svg"></b-nav-item>
            <b-nav-item href="/centers_map">Mapa de Centros</b-nav-item>
            <b-nav-item href="/create_center">Alta de nuevo Centro</b-nav-item>
            <b-nav-item href="/centers_map">Turno</b-nav-item>
            <b-nav-item href="/estadisticas">Estadisticas</b-nav-item>
          </b-navbar-nav>
        </div>     
      </b-collapse>
    </b-navbar>
    <router-view></router-view>
  </header>

<footer id="main-footer" class="mt-3">
    <div class="fluid-container">
    <p class="text-center">
      Página realizada por Grupo 19 - Contacto: covid19@covid.com.ar - 
      <a href="https://www.imdb.com/video/vi2776934681">Términos del Servicio</a>
    </p>
    <div id="myPlaceHolder"></div>
    </div>
</footer>
</div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  
}



#nav a {
  font-weight: bold;
  
}

#nav a.router-link-exact-active {
  color: black;
  background: #f8f9fa;
}
.navbar-nav{
  max-width: 960px;
}
.navbar-dark .navbar-nav .nav-link {
    color: rgb(255, 255, 255)!important;
    font-size: 1.2em;
}

#myPlaceHolder{
  min-height: 300px;
}
#main-footer{            
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    height: fit-content;
    width: 100%;
       color: black;
       background:#f0f0f0 ;
    background-image: url('~@/assets/footer.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;

}
</style>
