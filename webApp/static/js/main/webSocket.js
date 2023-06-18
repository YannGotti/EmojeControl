let socket = new WebSocket("wss://"+ location.host +"/ws/");

function createSocket(data){
    socket.onopen = function(e) {
        socket.send(JSON.stringify(data));
        console.log('connect')
    };
}

socket.onmessage = function(event) {
    try {
        let data = JSON.parse(event.data)
        if (data.status == 'connect'){
            createCube(data.id)
            return
        }

        if (data.status == 'move'){
            handleKeyPress(data.key, data.id)
            return
        }

        let textarea_one = document.getElementById('textarea_one')

        textarea_one.textContent += " " + data.username + ' : ' + data.text + ' ';
    } catch (e) {
        alert('Error:', e.message);
    }
};

function userConnect(id){
    data = {
        'id' : id,
        'status' : 'connect'
    }
    data = JSON.stringify(data)

    socket.send(data);
    
}

function userMove(key, id){
    data = {
        'id' : id,
        'key': key,
        'status' : 'move'
    }
    data = JSON.stringify(data)

    socket.send(data);
}


function sendMessage(){
    let input_message = document.getElementById('input_message')
    data = {
        'username' : tg.initDataUnsafe.user.username,
        'text': input_message.value
    }
    socket.send(JSON.stringify(data));
}

