
var cubeX = 0;
var cubeY = 0;

function showButton(){
    tg.expand(); 
    
    let button_username = document.getElementById('button_username')
    button_username.textContent = tg.initDataUnsafe.user.first_name;

    tg.MainButton.setText("ИГРАТЬ")

    tg.MainButton.show()
}

Telegram.WebApp.onEvent('mainButtonClicked', function(){
    tg.close()
});

let canvas = document.getElementById('canvas');

function createCube(id, connect = false){
    canvas.innerHTML += `<div id="cube_`+ id +`"></div>`

    // Получение элемента квадрата
    var square = document.getElementById("cube_" + id);

    // Настройка стилей и других свойств квадрата
    square.style.width = "40px";
    square.style.height = "40px";
    square.style.backgroundColor = "red";
    square.style.position = "relative";
    if (connect){
        //setTimeout(() => userConnect(id), 1000);
        setTimeout(() => CONNECT = true, 1000);
    }
}


function UpdateUser(data){

    if (data.action){
        DeleteUser(data.id)
        return
    }
        

    var square = document.getElementById('cube_' + data.id);

    if (!square) {
        square = document.createElement('div');
        square.id = 'cube_' + data.id; 
        square.style.position = "relative";
        canvas.appendChild(square); 
    }

    // Настройка стилей и других свойств квадрата
    square.style.width = data.width;
    square.style.height = data.height;
    square.style.backgroundColor = data.backgroundColor;
    square.style.top = data.top;
    square.style.left = data.left;
}

function DeleteUser(id){
    var square = document.getElementById('cube_' + id);
    canvas.removeChild(square);
}


function handleKeyPress(key, id, client = false) {

    var square = document.getElementById("cube_" + id);

    // Проверка нажатой клавиши
    if (key === "w") {
        cubeY -= 10; // Движение вверх
    } else if (key === "a") {
        cubeX -= 10; // Движение влево
    } else if (key === "s") {
        cubeY += 10; // Движение вниз
    } else if (key === "d") {
        cubeX += 10; // Движение вправо
    }

    // Обновление позиции куба
    square.style.top = cubeY + "px";
    square.style.left = cubeX + "px";
}

