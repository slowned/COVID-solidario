<template>
<div>
  <modal v-if="showModal" @close="showModal = false">
    <h3 slot="header">Reservar turno:</h3>
    <!-- BODY -->
    <div slot="body"> 
      <div>
        <label for="name">Nombre: </label>
        <input type="text" v-model="name" name="name"> 
      </div>
      <div>
        <label for="surname">Apellido: </label>
        <input type="text" v-model="surname" name="surname"> 
      </div>
      <div>
        <label for="email">Email: </label>
        <input type="email" v-model="email" name="email"> 
      </div>
      <div>
        <label for="phone">Telefono: </label>
        <input type="text" v-model="phone" name="phone"> 
      </div>
    </div>
    <div slot="footer">
      <div>
        <button class="btn btn-success" @click="registerTurn">
          Aceptar
        </button>
        <button class="btn btn-danger" @click="showModal = false" style="display: block; display:inline-block; float:left;">
          Cancelar
        </button>
      </div>
    </div>
  </modal>

  <br>
  <br>

  <div>
    <h4>Buscar Turno</h4>
    <b-form-datepicker id="turn-date" v-model="searchQuery" class="mb-2"></b-form-datepicker>
    <b-button variant="primary" type="submit" @click.prevent="fetchTurns" class="mb-2">Buscar</b-button>
  </div>
  <br>
  <br>
  <div>
    <h4>Listado de Turno disponibles</h4>
    <table class="table">
      <thead class="thead-dark">
        <tr>
          <th>ID</th>
          <th>Dia</th>
          <th>Hora Inicio</th>
          <th>Hora Fin</th>
          <th>Reservar</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="turn in turns" v-bind:key="turn.id">
          <td>{{ turn.pk }}</td>
          <td>{{ turn.fecha }}</td>
          <td>{{ turn.hora_inicio }}</td>
          <td>{{ turn.hora_fin }}</td>
          <td>
            <button id="show-modal" @click="showModal = true; lastSelectedTurn=turn">Registrar turno</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Modal from '@/components/Modal'


export default {
  name: 'RegisterTurn',
  props: {
  },
  components: {
    Modal,
  },
  data () {
    return {
      name: '',
      surname: '',
      email: '',
      phone: '',
      turns: [],
      searchQuery: '',
      showModal: false,
      lastSelectedTurn: null,
      centerId: '',
    };
  },
  mounted: function () {
    this.fetchTurns();
  },
  created: function () {
    this.centerId = this.$route.params['center_id'];
  },
  methods: {
    fetchTurns: function () {
      let data = {};
      let BACK_URL = process.env.VUE_APP_BACKEND;
      let url = `${BACK_URL}/centros/` + this.centerId + `/turnos_disponibles/`;

      if(this.searchQuery) {
        data = {fecha: this.searchQuery}
      }

      axios
        .get(url, {params : data})
        .then(response => {
          this.turns = response.data.turnos;
        })
        .catch(error => {
          console.log("error fetch: " + error);
        });
    },
    registerTurn: function () {
      console.log('registrando turno');
      let BACK_URL = process.env.VUE_APP_BACKEND;
      let center_id = this.centerId;
      axios
        .post(`${BACK_URL}/centros/${center_id}/reserva/`, {
          "centro_id": 5,
          "email_donante": this.email,
          "fecha": this.lastSelectedTurn.fecha,
          "hora_inicio": this.lastSelectedTurn.hora_inicio,
          "hora_fin": this.lastSelectedTurn.hora_fin,
          "telefono_donante": this.phone,
        })
        .then(response => {
          console.log(response);
          this.showModal = false;
          this.turns = this.turns.filter(turn => turn.pk != this.lastSelectedTurn.pk)
        })
        .catch(error => {
          console.log("error registro: " + error);
        });
      
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
@import "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css";
@import "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css";
</style>
