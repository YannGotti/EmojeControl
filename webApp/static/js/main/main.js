

let tg = window.Telegram.WebApp;
tg.expand();


LOCAL_ID = tg.initDataUnsafe.user.id

var canvas = document.getElementById('my_canvas');

var ctx = canvas.getContext('2d');

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
  
//LOCAL_ID = getRandomInt(1, 100)

let data = {
    'id' : LOCAL_ID,
    'username': tg.initDataUnsafe.user.username,
    'first_name' : tg.initDataUnsafe.user.first_name,
    'auth': true
}


function initCanvas(){
    canvas.width = 380;
    canvas.height = 670;
}

initCanvas();

createSocket(data)


