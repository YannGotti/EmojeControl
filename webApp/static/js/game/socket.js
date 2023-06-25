let socket = new WebSocket("wss://"+ location.host +"/ws/");

let containers_canvas = document.getElementById("containers_canvas");

function initCanvas(canvas){
    canvas.width = 670;
    canvas.height = 380;
}

function createCanvas(id){
    var canvas = document.createElement('canvas'); 
    canvas.id = 'my_canvas_' + id;
    canvas.classList.add('custom_canvas');

    initCanvas(canvas);

    containers_canvas.appendChild(canvas);
    return canvas
}

function openSocket(data){
    socket.onopen = function(e) {
        socket.send(JSON.stringify(data));
        data.tabIndex = 1;

        let player = new Player(createCanvas(data.id), data)
        console.log(player);

        console.log('connect')
    };
}

socket.onmessage = function(event) {
    try {
        let data = JSON.parse(event.data)

        if (data.status == 'disconnectUser'){
            let id = data.id;


        }



        
    } catch (e) {
        console.log('Error:', e);
    }
};