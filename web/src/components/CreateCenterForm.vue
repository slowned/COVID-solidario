<template>
  <main class="container">
  <b-jumbotron>
      <h3>Completá el formulario para solicitar el alta del centro </h3>
  </b-jumbotron>
  <b-jumbotron>
    <div class="row">
      <div class="container" style="background-color:#eee">       
        <form class="formFix" @submit.prevent="validateForm">
          <div class="row">
          <div class="col-md-6 col-sm-12">
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Nombre:*</label>
                  <b-form-input type="text" placeholder="Ingresá tu nombre" v-model="nombre" v-validate="'required|min:4'" name="nombre"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('nombre') }}</div>
              </div>
            </div>
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Dirección:*</label>
                  <b-form-input type="text" placeholder="Ingresá tu direccion" v-model="direccion" v-validate="'required|min:6'" name="direccion"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('direccion') }}</div>
              </div>
            </div>
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Teléfono:*</label>
                  <b-form-input type="text" placeholder="Ingresá tu telefono" v-model="telefono" v-validate="'required|numeric|min:10'" name="telefono"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('telefono') }}</div>
              </div>
            </div>
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Hora de Apertura:*</label>
                  <b-form-timepicker
                    now-button
                    reset-button
                    locale="es"
                    placeholder="08:00"
                    v-model="hora_apertura" 
                    v-validate="'required|date_format:HH:mm:ss'" 
                    name="hora_apertura">
                  </b-form-timepicker>
                  <!--b-form-input type="text" placeholder="Ingresá tu hora_apertura" v-model="hora_apertura" v-validate="'required|date_format:HH:mm'" name="hora_apertura"> </b-form-input-->
                  <div class="alert-danger" role="alert">{{ errors.first('hora_apertura') }}</div>
              </div>
            </div>
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Hora de Cierre:*</label>
                  <b-form-timepicker
                    now-button
                    reset-button
                    locale="es"
                    placeholder="20:00"
                    v-model="hora_cierre" 
                    v-validate="'required|date_format:HH:mm:ss'" 
                    name="hora_cierre">
                  </b-form-timepicker>
                  <!--b-form-input type="text" placeholder="Ingresá tu hora_cierre" v-model="hora_cierre" v-validate="'required|date_format:HH:mm'" name="hora_cierre"> </b-form-input-->
                  <div class="alert-danger" role="alert">{{ errors.first('hora_cierre') }}</div>
              </div>
            </div>
         
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Web:</label>
                  <b-form-input type="text" placeholder="Ingresá tu web" v-model="web" v-validate="'url: {require_protocol: true }|min:5'" name="web"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('web') }}</div>
              </div>
            </div>
            <div class="form-row mb-3">
              <div class="form-group">
                  <label>Email:</label>
                  <b-form-input type="text" placeholder="Ingresá tu email" v-model="email" v-validate="'email'" name="email"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('email') }}</div>
              </div>
            </div>

              <!--div class="form-row mb-3">
              <div class="form-group">
                  <label>Protocolo de Vista:*</label>
                  <b-form-input type="text" placeholder="Ingresá tu email" v-model="email" v-validate="'email'" name="email"> </b-form-input>
                  <div class="alert-danger" role="alert">{{ errors.first('email') }}</div>
              </div>
            </div-->

            <div class="form-row mb-3">
              <div class="form-group">
                <SelectTipos/>
              </div>
            </div>

          </div>
          <div class="col-md-6 col-sm-12">
            
            <div class="form-row mb-4">
              <div class="form-group">
                <SelectLocalidades/>
              </div>
            </div>
            
            <div class="form-row mb-3">
              <div class="form-group">
                <CenterCreateMap/>
              </div>
            </div>

            <div class="form-row mb-3">
              <div class="form-group">
                <div id="g-recaptcha-placeholder" class="g-recaptcha" v-bind:value="captcha" data-sitekey="6LdnLP8ZAAAAANSfvK-KnOLU9RqEhz7wbO-3YP4r"></div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                  <!--l v-if="api_errors && api_errors.length">
                    <li v-for="error of api_errors">
                      {{error.message}}
                    </li>
                  </ul-->
                <div v-if="formStatus" class="alert alert-danger alert-dismissible fade show" role="alert"> {{ formStatus }} </div>
              </div>
            </div>

            <div class="form-row mt-3">
                <button type="submit" class="btn btn-success btn-lg" style="width:100%;">Agregar Centro</button>
            </div>
          </div>
          </div>
        </form>
        </div>
      </div>
    <div>
      <modal v-if="showModal" @close="showModal = false">
        <h1 slot="header">Resultados</h1>
        <!-- BODY -->
        <div slot="body"> 
          <h2>{{ serverStatusResponseMessage }}</h2>
        </div>
        <div slot="footer">
          <div>
            <button class="btn btn-success" @click="returnHome">
              Regresar
            </button>
            <!--button class="btn btn-danger" @click="showModal = false" style="display: block; display:inline-block; float:left;">
              Cancelar
            </button-->
          </div>
        </div>
      </modal>
    </div>
  </b-jumbotron>
  </main>
</template>



<script>  
import axios from 'axios';
import SelectTipos from "./SelectTipos";
import SelectLocalidades from "./SelectLocalidades";
import CenterCreateMap from "./CenterCreateMap";
import Modal from '@/components/Modal'

export default {
  name: 'CreateCenterForm',
  components: {
  SelectTipos,
  SelectLocalidades,
  CenterCreateMap,
  Modal,
  },
  computed: {
    selectedTipo() {
      return this.$store.state.selected
    },
    selectedMunicipio() {
      return this.$store.state.selectedMunicipio
    },
    selectedLat() {
      return this.$store.state.latitude
    },
    selectedLng() {
      return this.$store.state.longitude
    },
    serverStatusReponse() {
      return this.$store.state.serverStatusReponse
    },
    serverStatusResponseMessage(){
      if(this.$store.state.serverStatusReponse == 201){return "La operación ha sido realizada con éxito";}
      if(this.$store.state.serverStatusReponse >= 400){return "La operación ha fallado";}
      return "Procesando el pedido...";
      //if(this.$store.state.serverStatusReponse == 500){return "La operación ha fallado (Error interno)";}
      //if(this.$store.state.serverStatusReponse == 400){return "La operación ha fallado (Error de validación)";}

    }
  },
  data(){
    return {
      nombre: "",
      direccion: "",
      telefono: "",
      hora_apertura: "08:00:00",
      hora_cierre: "23:59:00",
      web: "",
      email: "",
      lat: "",
      lng: "",
      captcha: document.getElementsByName('g-recaptcha-response'),
      formStatus: "",
      all_good: true,
      showModal: false,
    }
  },
  mounted() {
    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute('src', 'https://www.google.com/recaptcha/api.js')
    document.head.appendChild(recaptchaScript)
  },
  methods:{
    validateForm() {
      this.formStatus = "";
      this.all_good = true;
      this.$validator.validateAll().then((result) => {
        if(this.selectedLat == ""){
          this.formStatus="Por favor, seleccione la ubicación en el mapa";
          this.all_good = false;
        }
        if(!result) {
          this.formStatus="Por favor, revise y complete todos los campos";
          this.all_good = false;
        }
        if(this.captcha[0].value == ''){
          this.formStatus="Por favor, complete el Captcha";
          this.all_good = false;
        }
        if(this.all_good){
          this.submitForm();
          this.formStatus="Enviado";
        }
      })
    },
    submitForm() {
      var _this = this;
      axios.post(process.env.VUE_APP_BACKEND +'/centros', {
        nombre : this.nombre,
        direccion : this.direccion,
        telefono : this.telefono,
        hora_apertura : this.hora_apertura,
        hora_cierre : this.hora_cierre,
        tipo : this.selectedTipo,
        web : this.web,
        email : this.email,
        lat : this.selectedLat,
        lng : this.selectedLng,
        municipio: this.selectedMunicipio,
        g_recaptcha_response : this.captcha[0].value //this.captcha
      })
      .then(function (response) {
        console.log("respuesta" + response.status);
        if(response.status == 201){ _this.$store.commit('setServerStatusReponse', response.status); }
      })
      .catch(function (error) {
        _this.$store.commit('setServerStatusReponse', error.response.status);
        console.log("error registro: " + error.response.status);
      });
      this.showModal = true;
    },
    returnHome(){
      this.$router.push('/');
    }
  },
  beforeRouteLeave: function(to, from, next) {
    if(this.$store.state.serverStatusReponse == 201){
      next();
    }
    else{
      // Se intentó enviar el formulario, pero con errores
      if(this.formStatus == "Enviado"){
        this.formStatus = "";
        this.showModal = false;
        this.errors.add({field:'nombre', msg:'Intente con otro nombre'});
        next(false);
      }
      else{
        next();
      }
    }
    this.$store.commit('setServerStatusReponse', "");
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
@import "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";
@import "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css";

.col-6{
  margin: 0 auto;
}
.formFix{
  margin: 0 auto;
}
.form-group{
  width:100%;
}
/*.g-recaptcha{
  padding-left: 25%;
}*/
.row{
    box-sizing: border-box;    
}
.col{
    box-sizing: border-box;    
}
label {
  width:100%;
  text-align: center;
  min-height: 1em;
}
input, select {
  width:100%;
  text-align: center;
  min-height: 3em;
}
#modal-cont{
  width: 50%;
}
#g-recaptcha-placeholder{
  width: 100%;
  max-width: 330px;
  margin: auto;
}
</style>

