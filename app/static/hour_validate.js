
function hour_validate (event) {
    

    let open_hour  =(document.getElementById('open_hour').value);
    


    let close_hour =  (document.getElementById('close_hour').value);
    
    const getTime = time => new Date(2019, 9, 2, time.substring(0, 2), time.substring(3, 5), 0, 0);


    if (getTime(close_hour) <= getTime(open_hour)) {
        event.preventDefault();
        alert('La hora de cierre debe ser mayor a la hora de apertura');
    }




}