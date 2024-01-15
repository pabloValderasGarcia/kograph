export class UploadableFile {
    constructor(file) {
        this.file = file;
        this.id = `${file.name}-${file.size}-${file.lastModified}-${file.type}`;
        this.url = URL.createObjectURL(file);
        this.status = true;
        this.width = 0;
        this.height = 0;
    }

    calculateDimensions() {
        return new Promise((resolve, reject) => {
            if (this.file.type.startsWith('image/')) {
                const element = new Image();
                element.src = this.url;
    
                const onLoadHandler = () => {
                    this.width = element.width;
                    this.height = element.height;
                    resolve();
                };
    
                element.addEventListener('load', onLoadHandler);
                element.addEventListener('error', () => {
                    reject(`${this.file.name} failed to load.`);
                });
            } else if (this.file.type.startsWith('video/')) {
                const element = document.createElement('video');
                element.src = this.url;
    
                const onLoadHandler = () => {
                    this.width = element.videoWidth;
                    this.height = element.videoHeight;
                    resolve();
                };
    
                element.addEventListener('loadeddata', onLoadHandler);
                element.addEventListener('error', () => {
                    reject(`${this.file.name} failed to load.`);
                });
            } else {
                this.file.status = false;
                reject(`${this.file.name} is not an image or video.`);
            }
        });
    }    
}

export class NoUploadableFile {
    constructor(file) {
        this.file = file;
        this.id = `${file.name}-${file.size}-${file.lastModified}-${file.type}`;
        this.url = URL.createObjectURL(file);
        this.status = false;
        this.width = 0;
        this.height = 0;
    }
}