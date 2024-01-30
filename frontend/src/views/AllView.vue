<script>
import { UploadableFile, NoUploadableFile } from './js/file/file-uploadable.js';
import createUploader from './js/file/file-uploader';
import { mapState, mapMutations } from 'vuex';
const { uploadFile } = createUploader();
import { FwbModal } from 'flowbite-vue'
import { notify } from 'notiwind';
import axios from 'axios';
import ButtonItem from '@/components/others/ButtonItem.vue';

export default {
    name: 'AllView',
    data() {
        return {
            // Otros
            darkMode: document.body.classList.contains('dark-mode'),
            pageWidth: window.innerWidth,
            // Ficheros
            groupedFiles: {}, // Por mes y año
            selected: 'off',
            // Edición ficheros
            selectedGroupIds: [],
            selectedFileIds: [],
            // Eliminación ficheros
            isShowDeleteModal: false
        }
    },
    emits: ['updateSelected'],
    async mounted() {
        // Al ser montado el componente, se recogen los ficheros y se activan eventos necesarios
        await this.getFiles();
        window.addEventListener('resize', this.handleResize);
        window.addEventListener('darkModeChanged', this.handleDarkModeChanged);
    },
    beforeUnmount() {
        // Al ser desmontado el componente, se recogen los ficheros y se desactivan eventos activados
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('darkModeChanged', this.handleDarkModeChanged);
    },
    computed: {
        ...mapState(['isLoading', 'files', 'filesData', 'selectedFiles']),
        // Manejo de archivos FRONTEND - BACKEND
        fullFileUrl() {
            return (file) => {
                if (file.type == 'image') return `${process.env.VUE_APP_SERVER_URL}${file.file}`;
                else return `${process.env.VUE_APP_SERVER_URL}/thumbnails${file.thumbnail}.png`;
            };
        },
    },
    methods: {
        // | --------------------------------------------------- |
        // | ---------------------- OTROS ---------------------- |
        // | --------------------------------------------------- |
        ...mapMutations(['setIsLoading', 'setFiles', 'setFilesData', 'setSelectedFiles']),
        // Método para comprobar si es gridInit (para funcionamiento masonry excelente)
        isGridInit(monthYearKey) {
            const files = this.groupedFiles[monthYearKey] || [];
            const totalWidth = files.reduce((sum, file) => sum + (file.width * (200 / file.height)), 0);
            return totalWidth < this.pageWidth - 100 && this.pageWidth > 1000;
        },
        // Método de control de ancho de página
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
        // Método para comprobar si el modo oscuro se ha cambiado
        handleDarkModeChanged() {
            this.darkMode = localStorage.getItem('darkMode') === 'true';
        },
        // | ----------------------------------------------------- |
        // | ---------------------- BACKEND ---------------------- |
        // | ----------------------------------------------------- |
        // Método para añadir ficheros al backend
        async addFiles(newFiles) {
            this.setIsLoading(true);

            // Actualizamos la alerta y los ficheros a 0
            if (document.getElementById('uploaded_alert')) document.getElementById('uploaded_alert').remove();
            this.files.splice(0, this.files.length);

            // Conteo de estados de ficheros
            let successCount = 0;
            let duplicateCount = 0;
            let invalidCount = 0;

            // Creamos contenedor alerta
            notify({
                group: "foo",
                title: "Uploaded files",
                text: "",
                type: "uploaded_info"
            }, -1);

            // Insertamos valores count a 0
            setTimeout(() => {
                if (document.getElementById('uploaded_count')) {
                    document.getElementById('uploaded_count').innerHTML = `
                        <p class="text-sm text-green-500 leading-4 m-0 mr-2">0 success</p>
                        <p class="text-sm text-yellow-400 leading-4 m-0 mr-2">0 duplicate</p>
                        <p class="text-sm text-red-500 leading-4 m-0">0 invalid</p>
                    `;
                }
            }, 50)

            // Recorremos cada archivo
            let started = false;
            for (const file of newFiles) {
                // Intentamos subirlo al servidor y a la lista de ficheros frontend
                try {
                    const uploadableFile = new UploadableFile(file);
                    await uploadableFile.calculateDimensions();
                    const response = await uploadFile(uploadableFile);
                    if (response['status'] == false) file.status = 'duplicate';
                    else file.status = true;
                    this.files.push(uploadableFile);
                }
                // Si no funciona, declaramos el fichero como no uploadable
                catch (error) {
                    const noUploadableFile = new NoUploadableFile(file);
                    file.status = false;
                    this.files.push(noUploadableFile);
                }

                // Notificación/alerta de ficheros subiéndose
                if (file.status == true) successCount++;
                else if (file.status == 'duplicate') duplicateCount++;
                else if (file.status == false) invalidCount++;

                // Actualizamos por cada fichero la alerta
                if (document.getElementById('uploaded_count')) {
                    document.getElementById('uploaded_count').innerHTML = `
                        <p class="text-sm text-green-500 leading-4 m-0 mr-2">${successCount} success</p>
                        <p class="text-sm text-yellow-400 leading-4 m-0 mr-2">${duplicateCount} duplicate</p>
                        <p class="text-sm text-red-500 leading-4 m-0">${invalidCount} invalid</p>
                    `;
                }
                if (document.getElementById('uploaded_alert_content')) {
                    document.getElementById('uploaded_alert_content').innerHTML += `
                        <div class="flex items-center w-[313px] overflow-hidden">
                            ${file.status == true ? '<svg data-v-39738549="" class="svg-inline--fa fa-circle-check mr-2 text-green-500" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-check" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"></path></svg>' : file.status == false ? '<svg data-v-39738549="" class="svg-inline--fa fa-circle-xmark mr-2 text-red-500" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-xmark" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z"></path></svg>' : '<svg data-v-39738549="" class="svg-inline--fa fa-circle-exclamation mr-2 text-yellow-400" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-exclamation" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path class="" fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"></path></svg>'}
                            <p class="text-sm text-black leading-4 m-0 truncate ${file.type.trim().split('/')[0] == 'video' ? 'flex items-center gap-2' : ''}">${file.type.trim().split('/')[0] == 'video' ? '<svg data-v-39738549="" class="svg-inline--fa fa-video text-[rgba(0,0,0,.7)] text-[12px]" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="video" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path class="" fill="currentColor" d="M0 128C0 92.7 28.7 64 64 64H320c35.3 0 64 28.7 64 64V384c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V128zM559.1 99.8c10.4 5.6 16.9 16.4 16.9 28.2V384c0 11.8-6.5 22.6-16.9 28.2s-23 5-32.9-1.6l-96-64L416 337.1V320 192 174.9l14.2-9.5 96-64c9.8-6.5 22.4-7.2 32.9-1.6z"></path></svg>' : ''}${file.name}</p>
                        </div>
                    `
                }

                // Insertamos valores count
                if (!started && document.getElementById('uploaded_count')) {
                    document.getElementById('uploaded_count').innerHTML = `
                        <p class="text-sm text-green-500 leading-4 m-0 mr-2">${successCount} success</p>
                        <p class="text-sm text-yellow-400 leading-4 m-0 mr-2">${duplicateCount} duplicate</p>
                        <p class="text-sm text-red-500 leading-4 m-0">${invalidCount} invalid</p>
                    `;
                }
                started = true;
            }

            this.setFilesData(this.files);
            this.setIsLoading(false);
        },
        // Método para mostrar ficheros del backend
        async getFiles() {
            this.setIsLoading(true);
            try {
                // Petición para recoger todos los ficheros según categoría
                const token = localStorage.getItem('access');
                const response = await axios.get(`${process.env.VUE_APP_SERVER_URL}/file/get/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.setFilesData(response.data);
                await this.groupFilesByMonthAndYear();
            } catch (error) {/**/ }
            this.setIsLoading(false);

            return this.filesData;
        },
        // Método para obtener los ficheros organizados por mes y año
        async groupFilesByMonthAndYear() {
            this.groupedFiles = {};

            // Se recorre cada fichero añadiéndole su ancho y alto para masonry
            const filesWithDimensions = await Promise.all(this.filesData.map(async file => {
                try {
                    // Verificar si el tipo de archivo está definido y no es nulo
                    if (file.type == 'image') {
                        const element = new Image();
                        element.src = `${process.env.VUE_APP_SERVER_URL}${file.file}`;

                        // Esperar a que la imagen esté completamente cargada
                        await new Promise((resolve, reject) => {
                            element.onload = resolve;
                            element.onerror = reject;
                        });

                        return {
                            ...file,
                            width: element.width,
                            height: element.height,
                        };
                    } else if (file.type == 'video') {
                        const element = document.createElement('video');
                        element.src = `${process.env.VUE_APP_SERVER_URL}${file.file}`;

                        // Esperar a que el video esté completamente cargado
                        await new Promise((resolve, reject) => {
                            element.onloadedmetadata = resolve;
                            element.onerror = reject;
                        });

                        return {
                            ...file,
                            width: element.videoWidth,
                            height: element.videoHeight,
                        };
                    } else {
                        return file;
                    }
                } catch (error) {
                    return file; // Devolver el archivo original en caso de error
                }
            }));
            this.setFilesData(filesWithDimensions);

            // Agrupar las imágenes por mes y año
            this.filesData.forEach((file) => {
                const date = new Date(file.origin_created_at);
                const monthYearKey = `${date.getMonth() + 1}-${date.getFullYear()}`;

                if (!this.groupedFiles[monthYearKey]) {
                    this.groupedFiles[monthYearKey] = [];
                }

                this.groupedFiles[monthYearKey].push(file);
            });

            // Ordenar las claves por fecha
            const sortedKeys = Object.keys(this.groupedFiles).sort((a, b) => {
                const [monthA, yearA] = a.split('-').map(Number);
                const [monthB, yearB] = b.split('-').map(Number);

                if (yearA !== yearB) {
                    return yearB - yearA;
                } else {
                    return monthB - monthA;
                }
            });

            // Crear un nuevo objeto ordenado
            const sortedGroupedFiles = {};
            sortedKeys.forEach((key) => {
                sortedGroupedFiles[key] = this.groupedFiles[key];
            });

            // Actualizar el objeto groupedFiles con el ordenado
            this.groupedFiles = sortedGroupedFiles;
        },
        getFormattedMonthYear(monthYearKey) {
            const [month, year] = monthYearKey.split('-');
            const monthName = new Date(`${year}-${month}-01`).toLocaleString('default', { month: 'long' });
            return `${monthName} ${year}`;
        },
        // | ---------------------------------------------------------------- |
        // | ---------------------- SELECCION FICHEROS ---------------------- |
        // | ---------------------------------------------------------------- |
        // Método para conseguir la clase de la imagen para masonry
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
        // Método para verificar si un archivo está seleccionado
        isFileSelected(file) {
            const fileId = file.id;
            return this.selectedFileIds.includes(fileId);
        },
        // Método para verificar si un grupo está seleccionado
        isGroupSelected(monthYearKey) {
            return this.selectedGroupIds.includes(monthYearKey);
        },
        // Método para seleccionar/deseleccionar fichero individual
        selectFile(monthYearKey, file) {
            this.selected = 'on';
            const fileId = file.id;
            if (this.selectedGroupIds.includes(monthYearKey)) {
                // Si el grupo está seleccionado, toogle del archivo individual
                this.selectedFileIds = this.selectedFileIds.includes(fileId)
                    ? this.selectedFileIds.filter(selectedFileId => selectedFileId !== fileId)
                    : [...this.selectedFileIds, fileId];
            } else {
                // Si el grupo no está seleccionado, manejar la selección/deselección normal del archivo
                if (this.selectedFileIds.includes(fileId)) {
                    this.selectedFileIds = this.selectedFileIds.filter(selectedFileId => selectedFileId !== fileId);
                } else {
                    this.selectedFileIds = [...this.selectedFileIds, fileId];
                }
            }
            this.updateGroupSelection(monthYearKey);
        },
        // Método para seleccionar/deseleccionar grupo
        selectGroup(monthYearKey, files) {
            if (this.selectedGroupIds.includes(monthYearKey)) {
                this.selected = 'off';
                this.selectedGroupIds = this.selectedGroupIds.filter(group => group !== monthYearKey);
                files.forEach(file => {
                    const fileId = file.id;
                    this.selectedFileIds = this.selectedFileIds.filter(selectedFileId => selectedFileId !== fileId);
                });
            } else {
                this.selected = 'on';
                this.selectedGroupIds = [...this.selectedGroupIds, monthYearKey];
                files.forEach(file => {
                    const fileId = file.id;

                    // Verificar si el archivo no está ya seleccionado antes de agregarlo
                    if (!this.selectedFileIds.includes(fileId)) {
                        this.selectedFileIds = [...this.selectedFileIds, fileId];
                    }
                });
            }
            this.updateGroupSelection(monthYearKey);
        },
        // Método para actualizar la selección del grupo según los archivos individuales
        updateGroupSelection(monthYearKey) {
            const files = this.groupedFiles[monthYearKey] || [];
            const allFilesSelected = files.every(file => this.isFileSelected(file));
            if (allFilesSelected) {
                this.selectedGroupIds = [...this.selectedGroupIds, monthYearKey];
            } else {
                this.selectedGroupIds = this.selectedGroupIds.filter(group => group !== monthYearKey);
            }
        },
        // Métodos de control de hover de ficheros
        handleHover(e) {
            e.isHovered = true;
        },
        handleLeave(e) {
            e.isHovered = false;
        },
        // | --------------------------------------------------------------- |
        // | ---------------------- ACCIONES FICHEROS ---------------------- |
        // | --------------------------------------------------------------- |
        // Método para mostrar fichero
        async showFile(file_id) {
            if (this.selected != 'on') this.$router.push(`/file/${file_id}`);
            if (this.selected == 'on' && !this.selectedFileIds.length > 0) this.selected = 'off';
        },
        // Método para compartir ficheros
        shareFiles() {
            // PETICION COMPARTIR FICHEROS CON IDS:
            if (this.selectedFileIds.length > 0) {
                this.selectedFileIds;
            }
        },
        // Método para añadir ficheros a álbum
        addFilesToAlbum() {
            // PETICION AÑADIR A ALBUM FICHEROS CON IDS:
            if (this.selectedFileIds.length > 0) {
                this.selectedFileIds;
            }
        },
        // Métodos para eliminar ficheros
        closeDeleteModal () {
            this.isShowDeleteModal = false
        },
        showDeleteModal () {
            this.isShowDeleteModal = true
        },
        async deleteFiles() {
            this.closeDeleteModal();

            // Petición eliminar ficheros con x IDs
            if (this.selectedFileIds.length > 0) {
                try {
                    await axios.post(`${process.env.VUE_APP_SERVER_URL}/file/delete/`, { 'file_ids': this.selectedFileIds });
                    await this.getFiles();
                    this.selectedGroupIds = [];
                    this.selectedFileIds = [];
                    notify({
                        group: "foo",
                        title: "Success",
                        text: "File/s deleted successfully.",
                        type: "success"
                    }, 4000);
                } catch (e) {
                    notify({
                        group: "foo",
                        title: "Error",
                        text: "There was an error trying to delete.",
                        type: "error"
                    }, 4000);
                }
            }
        },
    },
    components: { FwbModal, ButtonItem },
};
</script>

<template>
    <div>
        <!-- MODALS -->
        <fwb-modal v-if="isShowDeleteModal" @close="closeDeleteModal" class="my_modal">
            <template #header>
                <div class="flex items-center text-lg gap-3">
                    <font-awesome-icon icon="circle-exclamation" class="text-yellow-400" />Are you sure to delete {{ this.selectedFileIds.length == 1 ? 'this file' : 'those files' }}?
                </div>
            </template>
            <template #footer>
                <div class="modal_buttons">
                    <ButtonItem @click="closeDeleteModal" color="alternative" title="Cancel"/>
                    <ButtonItem @click="deleteFiles" color="green" title="Delete"/>
                </div>
            </template>
        </fwb-modal>

        <!-- SELECTED BAR -->
        <div class="selected_bar" v-if="selectedFileIds.length > 0">
            <p class="flex items-center gap-2"><font-awesome-icon class="selected_bar_close" icon="xmark"
                    @click="selectedGroupIds = []; selectedFileIds = [];" />{{
                        selectedFileIds.length }} selected</p>
            <div class="selected_bar_buttons">
                <font-awesome-icon icon="retweet" @click="shareFiles" />
                <font-awesome-icon icon="plus" @click="addFilesToAlbum" />
                <font-awesome-icon :icon="['far', 'trash-can']" @click="showDeleteModal" />
            </div>
        </div>
        
        <!-- LAYOUT NO PHOTOS -->
        <div class="no_photos" v-if="!isLoading & filesData.length == 0">
            <div
                :style="{ 'background-image': `url(${this.darkMode ? require('@/assets/img/app/no_photos_dark.png') : require('@/assets/img/app/no_photos.png')})` }">
            </div>
            <div>
                <p>Do you want to add your memories?</p>
                <p>Drag and drop your memories anywhere on the screen</p>
            </div>
        </div>

        <!-- GRID MASONRY -->
        <div v-if="!isLoading">
            <div v-for="(files, monthYearKey) in groupedFiles" :key="monthYearKey" class="file_container">
                <p class="month_year" v-if="!isLoading" @mouseover="handleHover(files)" @mouseleave="handleLeave(files)">
                    {{ getFormattedMonthYear(monthYearKey) }}
                    <font-awesome-icon v-if="files.isHovered || isGroupSelected(monthYearKey)"
                        @click="selectGroup(monthYearKey, files)"
                        :class="[isGroupSelected(monthYearKey) ? 'text-blue-500' : (darkMode ? 'text-white' : 'text-black')]"
                        :icon="isGroupSelected(monthYearKey) ? ['fas', 'circle'] : ['far', 'circle']" />
                </p>
                <div v-if="!isLoading"
                    :class="{ 'grid-wrapper': true, 'grid-init': isGridInit(monthYearKey), 'grid-cols-mine': pageWidth > 800, 'auto-rows-[140px]': pageWidth > 800 }">
                    <div :class="[getImageClass(file), isFileSelected(file) ? 'bg-clip-padding border-[3px] border-solid border-[rgb(59,130,246)]' : '']"
                        v-for="file in files" :key="file.id" :file="file"
                        :style="{ 'background-image': `url(${fullFileUrl(file)})`, 'height': isGridInit(monthYearKey) ? '200px' : 'unset', 'width': isGridInit(monthYearKey) ? (200 * file.width) / file.height + 'px' : 'unset' }"
                        @click="showFile(file.id)" @mouseover="handleHover(file)" @mouseleave="handleLeave(file)">
                        <div class="file_overlay">
                            <div></div>
                            <div class="overlay_video" v-if="file.type == 'video'">
                                <font-awesome-icon icon="video" class="text-white" />
                                <p class="text-[12px] text-white">{{ file.duration }}</p>
                            </div>
                            <font-awesome-icon class="absolute top-[10px] right-[10px] text-[20px] z-10"
                                v-if="file.isHovered || isFileSelected(file)"
                                @click="selectFile(monthYearKey, file)"
                                :class="isFileSelected(file) ? 'text-blue-500' : 'text-white'"
                                :icon="isFileSelected(file) ? ['fas', 'circle'] : ['far', 'circle']" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- LOADER -->
        <div class="loader_container" v-if="isLoading">
            <div class="loader"></div>
        </div>
    </div>
</template>

<style scoped>
.selected_bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 59px;
    background-color: white;
    box-shadow: 0 1px 2px 0 rgba(60, 64, 67, .3), 0 2px 6px 2px rgba(60, 64, 67, .15);
    padding: 10px 35px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 9999;
}

body.dark-mode .selected_bar {
    background-color: #242424;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.3), 0 2px 6px 2px rgba(0, 0, 0, .15);
}

.selected_bar_buttons {
    display: flex;
    align-items: center;
    gap: 4px;
}

.selected_bar_buttons > svg, .selected_bar_close {
    user-select: none;
    cursor: pointer;
    aspect-ratio: 1/1;
    border-radius: 5px;
    font-weight: 500;
    padding: 10px;
}

.selected_bar svg:hover {
    background-color: #ececec;
}

body.dark-mode .selected_bar svg:hover {
    background-color: #373737 !important;
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

.file_container {
    display: flex;
    flex-direction: column;
    margin-bottom: 30px;
    position: relative;
}

.month_year {
    user-select: none;
    font-size: 25px;
    margin: 5px 30px 15px 30px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.month_year svg {
    font-size: 20px;
    cursor: pointer;
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

.grid-wrapper div .file_overlay {
    width: 100%;
    height: 100%;
    position: relative;
    transition: all .1s ease-in-out;
}

.grid-wrapper div .file_overlay div:first-child {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .15);
    opacity: 0;
    transition: opacity .1s ease-in-out;
}

.overlay_video {
    background-color: rgba(0, 0, 0, .6);
    padding: 5px;
    position: absolute;
    top: 5px !important;
    left: 5px !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.grid-wrapper div:hover .file_overlay div:first-child {
    opacity: 1;
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
    z-index: 9;
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

@media screen and (max-width: 600px) {
    .grid-wrapper {
        margin: 5px 20px;
    }
}</style>