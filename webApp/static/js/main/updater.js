CONNECT = false

var intervalId = setInterval(Update, 10);


function Update(){
    if (CONNECT){
        var square = document.getElementById("cube_" + DATA_PLAYER['id']);
        
        DATA_PLAYER.width = square.style.width;
        DATA_PLAYER.height = square.style.height;
        DATA_PLAYER.backgroundColor = square.style.backgroundColor;
        DATA_PLAYER.top = square.style.top;
        DATA_PLAYER.left = square.style.left;

        userUpdate(DATA_PLAYER)
    }
}


