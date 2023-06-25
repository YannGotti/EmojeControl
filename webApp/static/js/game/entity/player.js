class Player extends CustomObject {
    constructor(canvas, data) {
        super(canvas);
        this.id = data.id;
        this.username = data.username;

        this.posY = 310;

        this.maxSpeed = 15;
        this.minSpeed = 1;

        this.speed = 1;
        this.acceleration = 0.5;
        this.jumpAcceleration = 8;
        this.keysPressed = {};

        this.moved = false;
        this.jump = false;
        this.fall = false;

        this.attack = false;

        this.cooldownAction = 900;
        this.lastActionFrame = 0; 
        this.cooldown = false;

        this.spawnHeight = 310;
        this.jumpHeight = this.posY - 100;

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
        this.keysPressed[event.code] = true;

        if (this.attack) {
            return;
        }

        if (this.cooldown){
            return;
        }

        if (event.code == 'KeyF') {
            if (!this.jump){
                this.currentAnimation = 'Run';
                this.frameRate = 30;
            }
            
            this.attack = true;

            
        }
    }

    handleKeyUp(event) {
        delete this.keysPressed[event.code];
    }

    move(timestamp){

        let elapsedTime = timestamp - this.lastActionFrame;

        if (elapsedTime > this.cooldownAction) {
            this.cooldown = this.false;
        }

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

        if (this.jump){

            if (this.posY <= this.jumpHeight){
                this.fall = true;
            }

            if (this.posY > this.spawnHeight){
                this.fall = false;
                this.jump = false;
                this.posY = this.spawnHeight;
                this.cooldown = true;
                this.lastActionFrame = timestamp;
            }

            if (this.posY > this.jumpHeight && !this.fall){
                this.posY -= this.jumpAcceleration;
                this.currentAnimation = 'Jump';
                this.frameRate = 10;
            }

            if (this.fall){
                this.posY += this.jumpAcceleration;
                this.currentAnimation = 'Fall';

            }

        }

        
        if (this.keysPressed['Space'] && !this.jump && !this.cooldown){

            this.jump = true;
            this.left = false;
            this.moved = true;

        }

        if (this.keysPressed['Space'] && !this.jump && !this.cooldown){
            this.posX += this.speed + 5;
            this.jump = true;
            this.left = true;
            this.moved = true;
        }
        

        if (this.keysPressed['KeyA']) {
            if (!this.jump){
                this.currentAnimation = 'Run';
                this.frameRate = 30;
            }

            this.posX -= this.speed;   
            this.left = true;
            this.moved = true;
        }

        if (this.keysPressed['KeyD']) {
            if (!this.jump){
                this.currentAnimation = 'Run';
                this.frameRate = 30;
            }

            this.posX += this.speed;
            this.left = false;
            this.moved = true;
        }


        if (JSON.stringify(this.keysPressed) == '{}' || (this.keysPressed['KeyD'] && this.keysPressed['KeyA']) || (this.keysPressed['KeyD'] && this.keysPressed['KeyA'])){
            if (this.jump){
                return;
            }

            this.moved = false;
            this.currentAnimation = 'Idle'
            this.frameRate = 5;
        }

    }

    update(timestamp) {

        if (LOCAL_ID != this.id){
            return
        }

        this.move(timestamp);

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

        if (this.attack){
            this.currentAnimation = 'Attack_1';
            this.cooldown = true;
            this.lastActionFrame = timestamp;

            setTimeout(() => {
                this.attack = false;
                this.currentAnimation = 'Idle';
            }, 200);
        }

        if (elapsedTime > this.frameDelay) {
            this.clear();

            if (this.currentAnimation == "Idle"){
                this.drawAnimationIdle();
            }

            if (this.currentAnimation == "Run"){
                this.drawAnimationRun();
            }

            if (this.currentAnimation == "Jump"){
                this.drawAnimationJump();
            }

            if (this.currentAnimation == "Fall"){
                this.drawAnimationFall();
            }

            if (this.currentAnimation == "Attack_1"){
                this.drawAnimationAttack_1();
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

    drawAnimationJump(){
        if (this.currentFrameIndex > this.animations.jump.length){
            this.currentFrameIndex = 0;
        }

        if (this.left){
            const currentImage = this.animations.jumpLeft[this.currentFrameIndex];
            this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
            this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.jumpLeft.length;
            return;
        }

        const currentImage = this.animations.jump[this.currentFrameIndex];
        this.ctx.drawImage(currentImage, this.posX, this.posY);
        this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.jump.length;
    }

    drawAnimationFall(){
        if (this.currentFrameIndex > this.animations.fall.length){
            this.currentFrameIndex = 0;
        }

        if (this.left){
            const currentImage = this.animations.fallLeft[this.currentFrameIndex];
            this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
            this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.fallLeft.length;
            return;
        }

        const currentImage = this.animations.fall[this.currentFrameIndex];
        this.ctx.drawImage(currentImage, this.posX, this.posY);
        this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.fall.length;
    }


    drawAnimationAttack_1(){
        if (this.currentFrameIndex > this.animations.attack_1.length){
            this.currentFrameIndex = 0;
        }

        if (this.left){
            const currentImage = this.animations.attack_1_left[this.currentFrameIndex];
            this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
            this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.attack_1_left.length;
            return;
        }

        const currentImage = this.animations.attack_1[this.currentFrameIndex];
        this.ctx.drawImage(currentImage, this.posX, this.posY + 10);
        this.currentFrameIndex = (this.currentFrameIndex + 1) % this.animations.attack_1.length;
    }
    
}