let Squares = []

class Square {
    constructor(data) {
        this.id = data.id;
        this.username = data.username;
        this.x = 50;
        this.y = 50;
        this.size = 20;
        this.color = 'red';

        this.maxSpeed = 15;
        this.minSpeed = 1;

        this.speed = 1;
        this.acceleration = 0.1;
        this.keysPressed = {};

        this.moved = false

        this.fontSize = 12;
        this.textWidth = 0;
        
        this.canvas = canvas;

        this.handleKeyDown = this.handleKeyDown.bind(this);
        this.handleKeyUp = this.handleKeyUp.bind(this);
        this.canvas.addEventListener('keydown', this.handleKeyDown);
        this.canvas.addEventListener('keyup', this.handleKeyUp);

        this.canvas.setAttribute('tabindex', '0');
        this.canvas.focus();

        this.ctx = ctx;
        this.draw()
        this.drawName()

        this.update();
    }

    draw() {
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(this.x, this.y, this.size, this.size);
    }

    drawName(){
        this.ctx.fillStyle = 'black';
        this.ctx.font = this.fontSize + "px serif";
        this.ctx.fillText(this.username, this.x + (this.size / 2) - (this.textWidth / 2), this.y - 10);
        this.textWidth = this.ctx.measureText(this.username).width;
    }

    handleKeyDown(event) {
        this.keysPressed[event.key] = true;
    }

    handleKeyUp(event) {
        delete this.keysPressed[event.key];
    }

    update() {

        if (LOCAL_ID != this.id){return}

        this.clear();
        this.clearName();

        if (this.moved){
            this.speed += this.acceleration;
        }
        else{
            this.speed -= this.acceleration;
        }

        if (this.speed > this.maxSpeed) {
            this.speed = this.maxSpeed;
        }

        if (this.speed < this.minSpeed){
            this.speed = this.minSpeed;
        }

        if (this.keysPressed['a']) {
            this.x -= this.speed;   
            this.moved = true;
        }
        if (this.keysPressed['d']) {
            this.x += this.speed;
            this.moved = true;
        }
        if (this.keysPressed['w']) {
            this.y -= this.speed;
            this.moved = true;
        }
        if (this.keysPressed['s']) {
            this.y += this.speed;
            this.moved = true;
        }

        if (JSON.stringify(this.keysPressed) == '{}'){
            this.moved = false;
        }

        this.draw();
        this.drawName();

        updateData(this.toJson())

        requestAnimationFrame(this.update.bind(this));
    }
    
    clear() {
        this.ctx.clearRect(this.x -0.6, this.y - 0.6, this.size + 1.2, this.size + 1.2);
    }

    clearName(){
        this.ctx.clearRect(this.x + (this.size / 2) - (this.textWidth / 2), this.y - 20, this.textWidth + 5, this.fontSize);
    }

    updateData(data){
        if (data.id != this.id){
            return
        }

        this.clear();
        this.clearName();

        this.x = data.x;
        this.y = data.y;
        this.speed = data.speed;
        this.keysPressed = data.keysPressed;
        this.moved = data.moved;

        this.draw();
        this.drawName();
    }

    toJson(){
        let data = {
            'id' : this.id,
            'username' : this.username,
            'x' : this.x,
            'y': this.y,
            'speed': this.speed,
            'keysPressed' : this.keysPressed,
            'moved' : this.moved,
        };

        return data;
    }
}


  

