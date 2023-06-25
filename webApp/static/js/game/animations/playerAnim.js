const runAnimation = [
    '../static/Sprites/Animations/Run/1.png',
    '../static/Sprites/Animations/Run/2.png',
    '../static/Sprites/Animations/Run/3.png',
    '../static/Sprites/Animations/Run/4.png',
    '../static/Sprites/Animations/Run/5.png',
    '../static/Sprites/Animations/Run/6.png',
    '../static/Sprites/Animations/Run/7.png',
    '../static/Sprites/Animations/Run/8.png'
];

const runAnimationLeft = [
    '../static/Sprites/Animations/Run/left/1.png',
    '../static/Sprites/Animations/Run/left/2.png',
    '../static/Sprites/Animations/Run/left/3.png',
    '../static/Sprites/Animations/Run/left/4.png',
    '../static/Sprites/Animations/Run/left/5.png',
    '../static/Sprites/Animations/Run/left/6.png',
    '../static/Sprites/Animations/Run/left/7.png',
    '../static/Sprites/Animations/Run/left/8.png'
];

const idleAnimation = [
    '../static/Sprites/Animations/Idle/1.png',
    '../static/Sprites/Animations/Idle/2.png',
    '../static/Sprites/Animations/Idle/3.png',
    '../static/Sprites/Animations/Idle/4.png',
    '../static/Sprites/Animations/Idle/5.png',
    '../static/Sprites/Animations/Idle/6.png'
];

const idleLeftAnimation = [
    '../static/Sprites/Animations/Idle/left/1.png',
    '../static/Sprites/Animations/Idle/left/2.png',
    '../static/Sprites/Animations/Idle/left/3.png',
    '../static/Sprites/Animations/Idle/left/4.png',
    '../static/Sprites/Animations/Idle/left/5.png',
    '../static/Sprites/Animations/Idle/left/6.png'
];

const attack_1_Animation = [
    '../static/Sprites/Animations/Attack_1/1.png',
    '../static/Sprites/Animations/Attack_1/2.png',
    '../static/Sprites/Animations/Attack_1/3.png',
    '../static/Sprites/Animations/Attack_1/4.png',
];

const attack_1_LeftAnimation = [
    '../static/Sprites/Animations/Attack_1/left/1.png',
    '../static/Sprites/Animations/Attack_1/left/2.png',
    '../static/Sprites/Animations/Attack_1/left/3.png',
    '../static/Sprites/Animations/Attack_1/left/4.png',
];

const jumpAnimation = [
    '../static/Sprites/Animations/Jump/4.png',
];

const fallAnimation = [
    '../static/Sprites/Animations/Jump/7.png',
];

const jumpLeftAnimation = [
    '../static/Sprites/Animations/Jump/left/4.png',
];

const fallLeftAnimation = [
    '../static/Sprites/Animations/Jump/left/7.png',
];

let playerAnimations = {
    'run' : [],
    'runLeft' : [],
    'idle' : [],
    'idleLeft' : [],
    'jump' : [],
    'fall' : [],
    'jumpLeft' : [],
    'fallLeft' : [],
    'attack_1' : [],
    'attack_1_left' : [],
}
  
function loadAnimations(){

    let runAnimationImages = [];
    let runLeftAnimationImages = [];
    let idleAnimationImages = [];
    let idleLeftAnimationImages = [];
    let jumpAnimationImages = [];
    let fallAnimationImages = [];

    let attack_1_AnimationImages = [];
    let attack_1_LeftAnimationImages = [];

    let jumpLeftAnimationImages = [];
    let fallLeftAnimationImages = [];

    let imagesLoaded = 0;

    runAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === runAnimation.length) {
                playerAnimations.run = runAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        runAnimationImages.push(image);
    });

    runAnimationLeft.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === runAnimationLeft.length) {
                playerAnimations.runLeft = runLeftAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        runLeftAnimationImages.push(image);
    });

    idleAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === idleAnimation.length) {
                playerAnimations.idle = idleAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        idleAnimationImages.push(image);
    });

    idleLeftAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === idleLeftAnimation.length) {
                playerAnimations.idleLeft = idleLeftAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        idleLeftAnimationImages.push(image);
    });

    jumpAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === jumpAnimation.length) {
                playerAnimations.jump = jumpAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        jumpAnimationImages.push(image);
    });

    fallAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === fallAnimation.length) {
                playerAnimations.fall = fallAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        fallAnimationImages.push(image);
    });

    jumpLeftAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === jumpLeftAnimation.length) {
                playerAnimations.jumpLeft = jumpLeftAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        jumpLeftAnimationImages.push(image);
    });

    fallLeftAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === fallLeftAnimation.length) {
                playerAnimations.fallLeft = fallLeftAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        fallLeftAnimationImages.push(image);
    });

    attack_1_Animation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === attack_1_Animation.length) {
                playerAnimations.attack_1 = attack_1_AnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        attack_1_AnimationImages.push(image);
    });

    attack_1_LeftAnimation.forEach((path, index) => {
        const image = new Image();

        image.onload = function() {
            imagesLoaded++;
            if (imagesLoaded === attack_1_LeftAnimation.length) {
                playerAnimations.attack_1_left = attack_1_LeftAnimationImages;
                imagesLoaded = 0;
            }
        };

        image.src = path;
        attack_1_LeftAnimationImages.push(image);
    });

    return playerAnimations;
}