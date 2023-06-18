let tg = window.Telegram.WebApp;

function showButton(){
    tg.expand(); 
    
    let button_username = document.getElementById('button_username')
    button_username.textContent = tg.initDataUnsafe.user.first_name;

    tg.MainButton.setText("ИГРАТЬ")

    tg.MainButton.show()
}

Telegram.WebApp.onEvent('mainButtonClicked', function(){
    alert(tg.initDataUnsafe.user)
	tg.sendData("some string that we need to send"); 
});

