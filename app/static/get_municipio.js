function get_municipio() {

    // let dropdown = document.getElementById('township');
    //  dropdown.length = 0;

    //let defaultOption = document.createElement('option');
    //defaultOption.text = 'Seleccionar Municipio';

    //dropdown.add(defaultOption);
    //dropdown.selectedIndex = 0;

    let township_id = parseInt (document.getElementById('township').value);
    console.log(township_id);
    let towship = document.getElementById('township');
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
                    console.log(data.data.Town[township_id].name);
                    let option;
                    console.log(data.per_page);
                    
                // Data Binding
                    option = document.createElement('option');
                    township.value=data.data.Town[township_id].name; //actual data display
                    console.log(data.data.Town[township_id].name);
                    //township.value = data.data.Town[township_id].id;
                    dropdown.add(option);
                    
                });
            }
        )
        .catch(function (err) {
            console.error('Fetch Error -', err);
        });
}