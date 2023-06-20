let socket = new WebSocket("wss://"+ location.host +"/ws/");

function createSocket(data){
    socket.onopen = function(e) {
        socket.send(JSON.stringify(data));


        var square = new Square(data);
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
                Squares.push(new Square(data))
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



