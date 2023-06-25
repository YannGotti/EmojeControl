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

let playerAnimations = {
    'run' : [],
    'runLeft' : [],
    'idle' : [],
    'idleLeft' : []
};
  
function loadAnimations(){

    let runAnimationImages = [];
    let runLeftAnimationImages = [];
    let idleAnimationImages = [];
    let idleLeftAnimationImages = [];

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

    return playerAnimations;
}