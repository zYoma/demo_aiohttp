var sock = new WebSocket('ws://' + window.location.host + WS_URL);
const header = document.querySelector('#header')
const main = document.querySelector('#main')

function showMessage(message) {
    /* Append message to chat area */
    
    var data = jQuery.parseJSON(message.data);
    let user = data.user
    let text = data.text
    if (text.includes('подключился')) {
        text = `<font color="blue">${text}</font>`
    }
    if (text.includes('Вышел из чата')) {
        text = `<font color="red">${text}</font>`
    }
    html = `<p><b>${user}</b>: ${text}</p>`
    let new_elem = document.createElement('div')
    new_elem.innerHTML = html
    main.appendChild(new_elem)

}

// ...

$('#send').on('submit', function (event) {

    event.preventDefault();
    var $message = $(event.target).find('input[name="text"]');
    sock.send($message.val());
    $message.val('').focus();

});

sock.onopen = function (event) {
    console.log('Connection to server started');
};

sock.onclose = function (event) {
    console.log(event);
    if(event.wasClean){
        console.log('Clean connection end');
    } else {
        console.log('Connection broken');
    }
    // window.location.assign('/');
};

sock.onerror = function (error) {
    console.log(error);
};

sock.onmessage = showMessage;