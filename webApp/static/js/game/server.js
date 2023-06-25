

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
  
LOCAL_ID = getRandomInt(1, 100)

let data = {
    'id' : LOCAL_ID,
    'username': 'Nigga_' + LOCAL_ID,
    'first_name' : 'tg.initDataUnsafe.user.first_name',
    'auth': true
}


console.log(loadAnimations());
openSocket(data)