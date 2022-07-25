let map;
let marker;

const mapClickHandler = (e) => {
 
  addMarker(e.latlng);

};

const addMarker = ({ lat , lng}) => {
  if (marker) marker.remove();

  marker = L.marker([lat, lng]).addTo(map);

};

const initializeMap = (selector) => {
        map = L.map(selector).setView([-34.9187, -57.956], 13);
         
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '',
            maxZoom: 18
        }).addTo(map);
       
      

       
       // L.marker([-34.9187, -57.956], {draggable: true}).addTo(map);
      //addSearchControl(); 
      map.on('click', mapClickHandler);
};

const addSearchControl = () => {
  L.control.scale().addTo(map);
  let searchControl = new L.esri.Controls.Geosearch().addTo(map);

  let results = new L.LayerGroup().addTo(map);

  searchControl.on('results', (data) => {
    results.clearLayers();

    if (data.results.length > 0) {
      addMarker(data.results[0].latlng);
    };
  });

};



const submitHandler = (event) => {
  if (!marker) {

    event.preventDefault();
    alert('Debes seleccionar una ubicación en el mapa.');
  }
  else {
    latlng = marker.getLatLng();
    document.getElementById('lat').setAttribute('value',latlng.lat);
    document.getElementById('lng').setAttribute('value',latlng.lng);
  }


};


window.onload = () => {
  initializeMap('map');
};

