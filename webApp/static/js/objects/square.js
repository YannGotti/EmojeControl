let Squares = []

class Square {
    constructor(data, client_canvas) {
        this.id = data.id;
        this.username = data.username;
        this.x = 50;
        this.y = 50;
        this.size = 20;
        this.color = 'red';

        this.maxSpeed = 5;
        this.minSpeed = 1;

        this.speed = 1;
        this.acceleration = 0.1;
        this.keysPressed = {};

        this.moved = false;

        this.fontSize = 12;
        this.textWidth = 0;

        this.startTouchX = 0;
        this.startTouchY = 0;

        this.isSwiping = false;

        this.tabIndex = data.tabIndex;

        this.hitbox = {}
        
        this.canvas = client_canvas;

        this.canvas.addEventListener('keydown', this.handleKeyDown.bind(this));

        this.canvas.addEventListener('keyup', this.handleKeyUp.bind(this));


        this.canvas.addEventListener('touchmove', function(event) {
            event.preventDefault();
        }, { passive: false });


        window.addEventListener('touchstart', this.handleTouchStart.bind(this));
        window.addEventListener('touchmove', this.handleTouchMove.bind(this));
        window.addEventListener('touchend', this.handleTouchEnd.bind(this));


        this.canvas.setAttribute('tabindex', this.tabIndex);
        this.canvas.focus();

        this.ctx = this.canvas.getContext('2d');
        this.draw()
        this.drawName()

        this.connected()

        this.update();
    }

    connected(){

        for (let square of Squares) {
                
            if (LOCAL_ID == square.id){
                containers_canvas.appendChild(square.canvas);
            }
        }

        console.log(this.username + " connected")
    }

    borderChecker(){
        const canvasWidth = this.canvas.width;
        const canvasHeight = this.canvas.height;
        const squareSize = this.size;


        if (this.x < 0) {
            this.clearSquare()
            this.x = 0;
        } else if (this.x > canvasWidth - squareSize) {
            this.clearSquare()
            this.x = canvasWidth - squareSize;
        }

        if (this.y < 10) {
            this.clearSquare()
            this.y = 0;
        } else if (this.y > canvasHeight - squareSize) {
            this.clearSquare()
            this.y = canvasHeight - squareSize;
        }
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

    handleTouchStart(event){
        if (LOCAL_ID != this.id){
            return
        }

        
        this.isSwiping = true;

        this.startTouchX = event.touches[0].clientX;
        this.startTouchY = event.touches[0].clientY;
    }

    handleTouchMove(event){
        if (!this.isSwiping) return;

        this.moved = true;

        this.clearSquare()
        
        this.startForce = event.touches[0].force;

        this.touchMoveSquare(event);

    }

    touchMoveSquare(event){
        const touchX = event.touches[0].clientX;
        const touchY = event.touches[0].clientY;
        const deltaX = touchX - this.startTouchX;
        const deltaY = touchY - this.startTouchY;

        this.x += (deltaX * this.speed / 10);
        this.y += (deltaY * this.speed / 10);

        this.startTouchX = touchX;
        this.startTouchY = touchY;
    }

    handleTouchEnd(event){
        this.isSwiping = false;
        this.moved = false;
    }


    moveSquare(){
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
    }



    update() {

        this.borderChecker()

        if (LOCAL_ID != this.id){
            return
        }

        this.clearSquare();

        this.moveSquare();

        this.hitbox = this.getHitbox()

        this.checkCollisions();

        this.drawSquare();

        updateData(this.toJson())

        requestAnimationFrame(this.update.bind(this));
    }



    getHitbox(){
        let hitbox = {
            'topLeft' :{
                'x' : this.x,
                'y' : this.y
            },
            'topRight' : {
                'x' : this.x + this.size,
                'y': this.y
            },
            'botLeft': {
                'x': this.x,
                'y' : this.y + this.size
            },
            'botRight' : {
                'x': this.x + this.size,
                'y' : this.y + this.size 
            }
        }

        return hitbox
    }
    
    clear() {
        this.ctx.clearRect(this.x -0.6, this.y - 0.6, this.size + 1.2, this.size + 1.2);
    }

    clearName(){
        this.ctx.clearRect(this.x + (this.size / 2) - (this.textWidth / 2) - 5, this.y - 20, this.textWidth + 10, this.fontSize);
    }

    checkCollisions(){
        for (const square of Squares) {
            if (this.id === square.id) continue;

            if (
                this.hitbox.topLeft.x < square.hitbox.botRight.x &&
                this.hitbox.topRight.x > square.hitbox.botLeft.x &&
                this.hitbox.topLeft.y < square.hitbox.botRight.y &&
                this.hitbox.botLeft.y > square.hitbox.topRight.y
            ) {
                if (this.hitbox.botLeft.y > square.hitbox.topLeft.y && this.hitbox.botLeft.y < square.hitbox.topLeft.y + 10) {
                    this.y = square.hitbox.topLeft.y - this.size - 1;
                } 

                if (this.hitbox.topRight.x > square.hitbox.topLeft.x && this.hitbox.topRight.x < square.hitbox.topLeft.x + 10){
                    this.x = square.hitbox.topLeft.x - this.size - 1;
                }

                if (this.hitbox.topRight.y < square.hitbox.botLeft.y && this.hitbox.topRight.y > square.hitbox.botLeft.y - 10){
                    this.y = square.hitbox.topLeft.y + this.size + 1;
                }

                if (this.hitbox.topLeft.x < square.hitbox.topRight.x && this.hitbox.topLeft.x > square.hitbox.topRight.x - 10){
                    this.x = square.hitbox.topLeft.x + this.size + 1;
                }

            }

        }
    }

    updateData(data){

        if (data.id != this.id){
            return
        }

        this.clearSquare();

        this.x = data.x;
        this.y = data.y;
        this.speed = data.speed;
        this.keysPressed = data.keysPressed;
        this.moved = data.moved;
        this.hitbox = data.hitbox

        this.drawSquare();
    }


    clearSquare(){
        //this.clear();
        //this.clearName();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    }

    drawSquare(){
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
            'hitbox' : this.hitbox,
        };

        return data;
    }

    disconnect(){
        this.clearSquare();
        this.canvas.remove();
        Squares = Squares.filter(square => square.id !== this.id);
        delete this;
    }
}


  

