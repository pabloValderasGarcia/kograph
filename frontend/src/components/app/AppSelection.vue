<script>
import DropZone from '@/components/app/dragndrop/DropZone.vue';
import axios from 'axios';
import { notify } from 'notiwind';
import { UploadableFile, NoUploadableFile } from '@/compositions/file-uploadable.js';
import createUploader from '@/compositions/file-uploader';
const { uploadFile } = createUploader();

export default {
    name: 'AppSelection',
    data() {
        return {
            darkMode: localStorage.getItem('darkMode') === 'true',
            pageWidth: window.innerWidth,
            isDragging: false,
            isLoading: true,
            files: [],
            filesData: [],
        }
    },
    props: ['item'],
    emits: ['updateSelected'],
    mounted() {
        this.db_files();
        document.body.addEventListener('dragover', this.handleDragOver);
        document.body.addEventListener('dragleave', this.handleDragLeave);
        document.body.addEventListener('drop', this.handleDragDrop);
        window.addEventListener('resize', this.handleResize);
        window.addEventListener('darkModeChanged', this.handleDarkModeChanged);
    },
    beforeUnmount() {
        document.body.removeEventListener('dragover', this.handleDragOver);
        document.body.removeEventListener('dragleave', this.handleDragLeave);
        document.body.removeEventListener('drop', this.handleDragDrop);
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('darkModeChanged', this.handleDarkModeChanged);
    },
    computed: {
        // Manejo de archivos FRONTEND - BACKEND
        fullImageUrl() {
            return (file) => {
                return `${process.env.VUE_APP_SERVER_URL}${file.file}`;
            };
        },
        // Comprobar si es gridInit (para funcionamiento masonry excelente)
        isGridInit() {
            const totalWidth = this.filesData.reduce((sum, file) => sum + (file.width * (200 / file.height)), 0);
            return totalWidth < this.pageWidth - 100 && this.pageWidth > 1000;
        },
    },
    methods: {
        // FRONTEND
        getImageClass(file) {
            const aspectRatio = file.width / file.height;
            if (file.width < 500 & file.height < 500) {
                return '';
            } else if (aspectRatio > 1.4) {
                return 'wide';
            } else if (aspectRatio < 1) {
                return 'tall';
            } else {
                return 'big';
            }
        },
        handleDragOver(e) {
            e.preventDefault();
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');
            if (hasFiles & !this.isDragging) {
                this.isDragging = true;
                setTimeout(() => {
                    document.getElementById('dropArea').style.opacity = '1';
                }, 25);
            }
        },
        handleDragLeave(e) {
            e.preventDefault();
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');
            const isOutsideWindow = e.clientY <= 0 || e.clientX <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight;
            if (hasFiles & isOutsideWindow) {
                this.fadeOut();
            }
        },
        handleDragDrop: async function (e) {
            e.preventDefault();
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');
            if (hasFiles) {
                this.isLoading = true;
                this.fadeOut();
                
                await this.addFiles(Array.from(e.dataTransfer.files)); // Añadir ficheros
                await this.db_files(); // Conseguir ficheros para mostrarlos

                if (document.getElementById('uploaded_alert')) document.getElementById('uploaded_alert').remove();
                let text = `
                    <div class="flex items-center w-[313px] overflow-hidden">
                        <p class="text-sm text-green-500 leading-4 m-0 mr-2">${this.files.filter((file) => file.status == true).length} success</p>
                        <p class="text-sm text-yellow-500 leading-4 m-0 mr-2">${this.files.filter((file) => file.status == 'existing').length} existing</p>
                        <p class="text-sm text-red-500 leading-4 m-0">${this.files.filter((file) => file.status == false).length} invalid</p>
                    </div>
                    <hr class="mb-1 border-1 border-solid border-black"/>
                `
                this.files.forEach((file) => {
                    text += `
                        <div class="flex items-center w-[313px] overflow-hidden">
                            ${file.status == true ? '<svg data-v-39738549="" class="svg-inline--fa fa-circle-check mr-2 text-green-500" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-check" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"></path></svg>' : file.status == false ? '<svg data-v-39738549="" class="svg-inline--fa fa-circle-xmark mr-2 text-red-500" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-xmark" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z"></path></svg>' : '<svg data-v-39738549="" class="svg-inline--fa fa-circle-exclamation mr-2 text-yellow-500" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-exclamation" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"></path></svg>'}
                            <p class="text-sm text-black leading-4 m-0 truncate">${file.file.name}</p>
                        </div>
                    `
                })
                notify({
                    group: "foo",
                    title: "Uploaded status",
                    text: text,
                    type: "uploaded_info"
                }, -1);
            }
        },
        fadeOut() {
            document.getElementById('dropArea').style.opacity = '0';
            setTimeout(() => {
                this.isDragging = false;
            }, 500);
        },
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
        handleDarkModeChanged() {
            this.darkMode = localStorage.getItem('darkMode') === 'true';
        },
        async addFiles(newFiles) {
            this.files.splice(0, this.files.length);
            for (const file of newFiles) {
                try {
                    const uploadableFile = new UploadableFile(file);
                    await uploadableFile.calculateDimensions();
                    const state = await uploadFile(uploadableFile);
                    uploadableFile.status = state.status ? true : 'existing'
                    this.files.push(uploadableFile);
                } catch (error) {
                    const noUploadableFile = new NoUploadableFile(file);
                    this.files.push(noUploadableFile);
                }
            }
        },
        // BACKEND
        async db_files() {
            this.isLoading = true;
            try {
                const token = localStorage.getItem('access');
                const response = await axios.get(`${process.env.VUE_APP_SERVER_URL}/file/get_all/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                const filesWithDimensions = await Promise.all(response.data.map(async file => {
                    const image = new Image();
                    image.src = `${process.env.VUE_APP_SERVER_URL}${file.file}`;

                    // Esperar a que la imagen esté completamente cargada
                    await new Promise(resolve => image.onload = resolve);

                    return {
                        ...file,
                        width: image.width,
                        height: image.height
                    };
                }));

                this.filesData = filesWithDimensions;
            } catch (error) {
                // console.error(error);
            }
            this.isLoading = false;
        }
    },
    components: { DropZone },
};
</script>

<template>
    <!-- !DRAGNDROP -->
    <DropZone v-if="isDragging" id="dropArea" ref="dropArea" class="drop-area">
        <template #default="{ dropZoneActive }">
            <label for="file-input" v-if="dropZoneActive">
                <div>
                    <font-awesome-icon icon="cloud-arrow-up" />
                    <p>Drop Them Here</p>
                </div>
            </label>
        </template>
    </DropZone>
    <!-- LAYOUT NO PHOTOS -->
    <div class="no_photos" v-if="!isLoading & filesData.length == 0">
        <div
            :style="{ 'background-image': `url(${this.darkMode ? require('@/assets/img/app/no_photos_dark.png') : require('@/assets/img/app/no_photos.png')})` }">
        </div>
        <div>
            <p>Do you want to add your memories?</p>
            <p>Drag your memories anywhere on the screen</p>
        </div>
    </div>
    <!-- GRID MASONRY -->
    <div id="grid-wrapper" :class="{ 'grid-wrapper': true, 'grid-init': isGridInit, '!grid-cols-mine !auto-rows-[140px]': pageWidth <= 800 }" v-if="!isLoading & item == 'all'">
        <div :class="getImageClass(file)" v-for="file in filesData" :key="file.id" :file="file"
            :style="{ 'background-image': `url(${fullImageUrl(file)})`, 'height': isGridInit ? '200px' : 'unset', 'width': isGridInit ? (200 * file.width) / file.height + 'px' : 'unset' }">
        </div>
    </div>
    <!-- LOADER -->
    <div class="loader_container" v-if="isLoading">
        <div class="loader"></div>
    </div>
</template>

<style scoped>
.drop-area {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    margin: 0 auto;
    opacity: 0;
    background-color: white;
    transition: opacity 0.4s ease;
}

body.dark-mode .drop-area {
    background-color: #242424 !important;
}

label {
    user-select: none;
    position: relative;
    font-size: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    opacity: 0;
    animation: appearAnimation .5s ease-in-out forwards;
}

label div {
    color: black;
    display: flex;
    flex-direction: column;
    gap: 20px;
    font-weight: bold;
}

body.dark-mode label div {
    color: white !important;
}

label div svg {
    font-size: 2em;
    color: #318ba7;
}

label input[type=file]:not(:focus-visible) {
    position: absolute !important;
    width: 100% !important;
    height: 100% !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0, 0, 0, 0) !important;
    white-space: nowrap !important;
    border: 0 !important;
}

.no_photos {
    user-select: none;
    height: calc(100svb - 200px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 45px;
}

.no_photos div:first-child {
    height: 285px;
    width: 400px;
    background-position: center center;
    background-size: contain;
    background-repeat: no-repeat;
}

.no_photos div:last-child {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 15px;
}

.no_photos div p:nth-child(1) {
    font-size: 35px;
}

.grid-wrapper {
    margin: 5px 30px;
    display: grid;
    grid-gap: 10px;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    grid-auto-rows: 200px;
    grid-auto-flow: dense;
}

.grid-init {
    display: flex !important;
}

.grid-wrapper div {
    cursor: pointer;
    background-size: cover;
    background-position: center center;
}

.grid-init div {
    background-size: 100% 100% !important;
    background-repeat: no-repeat !important;
}

.grid-wrapper .wide {
    grid-column: span 2;
}

.grid-wrapper .tall {
    grid-row: span 2;
}

.grid-wrapper .big {
    grid-column: span 2;
    grid-row: span 2;
}

.loader_container {
    z-index: 9999;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: calc(100vh - 200px);
    background-color: white;
}

body.dark-mode .loader_container {
    background-color: #242424 !important;
}

.loader {
    width: 48px;
    height: 48px;
    border: 5px solid #318ba7;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

@keyframes appearAnimation {
    to {
        opacity: 1;
    }
}

@media screen and (max-width: 600px) {
    .grid-wrapper {
        margin: 5px 20px;
    }
}
</style>