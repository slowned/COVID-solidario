import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		selected:"",
		latitude:"",
		longitude:"",
		serverStatusReponse:"",
		apiMunicipiosPayload:"",
		apiStatsPayload:"",
	},
	mutations: {
		// share a message between components
		setServerStatusReponse(state, msg){
			state.serverStatusReponse = msg
		},
		selectTipoCentro(state, option){
			state.selected = option
		},
		selectMunicipio(state, option){
			state.selectedMunicipio = option
		},
		selectCoordinates(state, obj){
			state.latitude = obj.lat
			state.longitude = obj.lng
		},
		setApiMunicipiosPayload(state, json){
			state.apiMunicipiosPayload = json
		},
		setApiStatsPayload(state, json){
			state.apiStatsPayload = json
		},
	},
	actions: {},
	modules: {}
})