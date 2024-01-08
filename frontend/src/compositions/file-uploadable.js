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
            const img = new Image();
            img.src = this.url;

            img.onload = () => {
                this.width = img.width;
                this.height = img.height;
                resolve();
            };

            img.onerror = () => {
                reject(this.file.name);
            };
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