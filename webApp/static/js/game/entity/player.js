class Player extends CustomObject {
    constructor(canvas, data) {
        super(canvas);
        this.id = data.id;
        this.username = data.username;

        this.posY = 310;


        this.maxSpeed = 7;
        this.minSpeed = 1;

        this.speed = 1;
        this.acceleration = 0.3;
        this.keysPressed = {};

        this.moved = false;

        this.canvas.addEventListener('keydown', this.handleKeyDown.bind(this));
        this.canvas.addEventListener('keyup', this.handleKeyUp.bind(this));

        this.tabIndex = data.tabIndex;
        this.canvas.setAttribute('tabindex', this.tabIndex);
        this.canvas.focus();

        this.animations = playerAnimations;
        this.frameRate = 30;
        this.frameDelay = 1000 / this.frameRate;
        this.lastFrameTime = 0;

        this.currentAnimation = 'Idle';
        this.animations = {};
        
        this.currentFrameIndex = 0;
        this.left = false;

        this.update();
    }

    handleKeyDown(event) {
        this.keysPressed[event.key] = true;
    }

    handleKeyUp(event) {
        delete this.keysPressed[event.key];
    }

    move(){
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
            this.currentAnimation = 'Run';

            this.posX -= this.speed;   
            this.left = true;
            this.moved = true;
            this.frameRate = 30;
        }

        if (this.keysPressed['d']) {
            this.currentAnimation = 'Run';

            this.posX += this.speed;
            this.left = false;
            this.moved = true;
            this.frameRate = 30;
        }

        if (JSON.stringify(this.keysPressed) == '{}' || (this.keysPressed['d'] && this.keysPressed['a'])){
            this.moved = false;
            this.currentAnimation = 'Idle'
            this.frameRate = 5;
        }

    }

    update(timestamp) {

        if (LOCAL_ID != this.id){
            return
        }

        this.move();

        try {
            this.updateAnimation(timestamp);
        } catch (error) {
            this.currentFrameIndex = 0;
            this.animations = loadAnimations();
        }

        requestAnimationFrame(this.update.bind(this));
    }

    updateAnimation(timestamp){
        let elapsedTime = timestamp - this.lastFrameTime;

        if (elapsedTime > this.frameDelay) {
            this.clear();

            if (this.currentAnimation == "Idle"){
                this.drawAnimationIdle();
            }

            if (this.currentAnimation == "Run"){
                this.drawAnimationRun();
            }

            this.lastFrameTime = timestamp;
        }

    }

    drawAnimationRun(){
        if (this.currentFrameIndex > this.animations.run.length){
            this.currentFrameIndex = 0;
        }

        if (this.left){
            const currentImage = this.animations.runLeft[this.currentFrameIndex];
            this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
            this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.runLeft.length;
            return;
        }

        const currentImage = this.animations.run[this.currentFrameIndex];
        this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
        this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.run.length;
        
    }

    drawAnimationIdle(){
        if (this.currentFrameIndex > this.animations.idle.length){
            this.currentFrameIndex = 0;
        }

        if (this.left){
            const currentImage = this.animations.idleLeft[this.currentFrameIndex];
            this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
            this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.idleLeft.length;
            return;
        }

        const currentImage = this.animations.idle[this.currentFrameIndex];
        this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
        this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.idle.length;
    }
    
}