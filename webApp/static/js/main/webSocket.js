let socket = new WebSocket("wss://"+ location.host +"/ws/");

let containers_canvas = document.getElementById("containers_canvas");

function initCanvas(canvas){
    canvas.width = 380;
    canvas.height = 670;
}

function createCanvas(id){
    var canvas = document.createElement('canvas'); 
    canvas.id = 'my_canvas_' + id;
    canvas.classList.add('custom_canvas');

    initCanvas(canvas);

    containers_canvas.appendChild(canvas);
    return canvas
}

function createSocket(data){
    socket.onopen = function(e) {
        socket.send(JSON.stringify(data));

        
        data.tabIndex = 1;
        var square = new Square(data, createCanvas(data.id));
        Squares.push(square)

        console.log('connect')
    };
}

socket.onmessage = function(event) {
    try {
        let data = JSON.parse(event.data)

        if (data.status == 'disconnectUser'){
            let id = data.id;

            for (let square of Squares) {
                
                if (square.id == id){
                    square.disconnect();
                }

            }
        }

        if (data.status == 'updateData'){

            data = data.data;

            let hasSquare = Squares.some(item => item.id === data.id);

            if (!hasSquare){

                data.tabIndex = Squares.length + 1;

                Squares.push(new Square(data, createCanvas(data.id)))
            }

            for (let square of Squares) {
                
                if (square.id == data.id){
                    square.updateData(data);
                }

            }
    
            return
        }

        
    } catch (e) {
        console.log('Error:', e);
    }
};

function updateData(data){
    socket.send(JSON.stringify(data));
}



