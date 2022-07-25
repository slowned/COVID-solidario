function get_municipios_edit() {

    let dropdown = document.getElementById('township');
      dropdown.length = 0;

    let defaultOption = document.createElement('option');
    defaultOption.text = 'Seleccionar Municipio';

    dropdown.add(defaultOption);
    dropdown.selectedIndex = 0;

    let township_id = parseInt (document.getElementById('township_id').value); // ahora el contenido es name, no ID
    console.log(township_id);
    
    const url = 'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135';

    fetch(url)
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.warn('Hubo un problema. Status Code: ' +
                        response.status);
                    return;
                }
                
                // Console Trace
                response.json().then(function (data) {
                    console.log(data);
                    console.log(data.data.Town[2].name);
                    let option;
                    console.log(data.per_page);
                    
                // Data Binding    
                    for (let i = 1; i < data.per_page; i++) {
                        
                        option = document.createElement('option');
                        option.text=data.data.Town[i].name;
                        console.log(data.data.Town[i].name);
                        option.value = data.data.Town[i].name;  //actual POST payload
                        if (township_id == data.data.Town[i].name){
                            option.selected="selected"
                        }
                        dropdown.add(option);
                    }

                });
            }
        )
        .catch(function (err) {
            console.error('Fetch Error -', err);
        });
}