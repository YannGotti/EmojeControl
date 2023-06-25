let socket = new WebSocket("wss://"+ location.host +"/ws/");
let containers_canvas = document.getElementById("containers_canvas");

PLAYERS = []

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
        PLAYERS.push(player);

        console.log('connect')
    };
}

socket.onmessage = function(event) {
    try {
        let data = JSON.parse(event.data)


        if (data.status == 'updateData'){
            data = data.data;

            let hasPlayer = PLAYERS.some(item => item.id === data.id);

            if (!hasPlayer){
                data.tabIndex = PLAYERS.length + 1;
                PLAYERS.push(new Player(createCanvas(data.id), data))
            }

            for (let player of PLAYERS) {
                
                if (player.id == player.id){
                    player.dataUpdate(data);
                }

            }
    
            return
        }

        if (data.status == 'disconnectUser'){
            let id = data.id;

            for (let player of PLAYERS) {
                
                if (player.id == id){
                    player.remove();
                }

            }
        }



        
    } catch (e) {
        console.log('Error:', e);
    }
};


function sendData(data){
    socket.send(JSON.stringify(data));
}