import Vue from 'vue'
import Router from 'vue-router'
//import  HelloWorld from './components/HelloWorld.vue'
import  CentersMap from '../components/CentersMap.vue'
import  CreateCenterForm from '../components/CreateCenterForm.vue'
import  Home from '../components/Home.vue'
import  Centers from '../components/Centers.vue'
import  CenterCreateMap from '../components/CenterCreateMap.vue'
import  Estadistica1 from '../components/Estadistica1.vue'
import RegisterTurn from '../views/RegisterTurn.vue'
import  Estadistica2 from '../components/Estadistica2.vue'
import Estadisticas from '../components/Estadisticas.vue'
import  Estadistica4 from '../components/Estadistica4.vue'

Vue.use(Router)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
      },
      {
        path: '/centers_map',
        name: 'centers_map',
        component: CentersMap
      },
      {
        path: '/create_center',
        name: 'create_center',
        component: CreateCenterForm
      },
      {
        path: '/centers',
        name: 'centers',
        component: Centers
      },
      {
        path: '/createMap',
        name: 'createMap',
        component: CenterCreateMap
      },
      {
        path: '/estadistica1',
        name: 'estadistica1',
        component: Estadistica1
      },
      {
        path: '/estadistica2',
        name: 'estadistica2',
        component: Estadistica2
      },
      {
        path: '/estadisticas',
        name: 'estadisticas',
        component: Estadisticas
      },
      {
        path: '/estadistica4',
        name: 'estadistica4',
        component: Estadistica4
      },
 
      
      {
        path: '/register_turn/:center_id',
        name: 'RegisterTurn',
        component: RegisterTurn
      },
]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
