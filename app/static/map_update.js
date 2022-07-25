let map;
let marker;
let lat;
let lng;
const mapClickHandler = (e) => {
 
  addMarker(e.latlng);

};

const addMarker = ({ lat , lng}) => {
  if (marker) marker.remove();

  marker = L.marker([lat, lng]).addTo(map);

};

const initializeMap = (selector) => {
        lat = document.getElementById('lat').getAttribute('value');
        lng =document.getElementById('lng').getAttribute('value');  
  
        map = L.map(selector).setView([lat, lng], 13);
        
        
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        }).addTo(map);
        
       L.control.scale().addTo(map);
       marker =L.marker([lat, lng], {draggable: true}).addTo(map);
    
        map.on('click', mapClickHandler);
};

const addSearchControl = () => {
  L.control.scale().addTo(map);
  let searchControl = new L.esri.Controls.Geosearch().addTo(map);

  searchControl.on('results',(data) => {
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
  initializeMap('mapupdate');
};
