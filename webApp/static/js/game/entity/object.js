class CustomObject {
    constructor(canvas) {

        this.posX = 0;
        this.posY = 0;

        this.width = 0;
        this.height = 0;

        this.canvas = canvas;
        this.ctx = this.canvas.getContext('2d');
    }

    clear(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    toJson(){
        let data = {
            'posX' : this.posX,
            'posY': this.posY,
            'width' : this.width,
            'height': this.height
        };

        return data;
    }

    remove(){
        this.clear();
        this.canvas.remove();

        delete this;
    }
}