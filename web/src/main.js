import Vue from 'vue'
import App from './App.vue'
import router from './router/index' // Router being imported
import store from './store/index'
import { Icon } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import VeeValidate from 'vee-validate'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VCharts from 'v-charts'




// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(VeeValidate);
Vue.config.productionTip = false
Vue.use(VCharts);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')


delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});
