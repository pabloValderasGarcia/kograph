<script>
// IMPORTS
import axios from 'axios';
import { notify } from 'notiwind';
import { mapState, mapMutations } from 'vuex';

// HOME
import HomeView from './HomeView.vue';

// NAV
import LogoItem from '@/components/nav/LogoItem.vue';
import SearcherItem from '@/components/nav/SearcherItem.vue';
import UserDropdown from '@/components/nav/UserDropdown.vue';
import NavItem from '@/components/app/NavItem.vue'

// APP
import DropZone from '@/components/app/dragndrop/DropZone.vue';
import AllView from './AllView.vue';
import AlbumView from './AlbumView.vue';
import AIView from './AIView.vue';
import FavoriteView from './FavoriteView.vue';
import SharedView from './SharedView.vue';
import PrivateView from './PrivateView.vue';
import SettingsView from './SettingsView.vue';

export default {
    name: 'RootView',
    data() {
        return {
            pageWidth: window.innerWidth,
            activeItemId: null,
            clickedItemId: null,
            selected: 'all',
            items: [
                { id: 1, url: 'all', title: 'All', icon: ['far', 'image'] },
                { id: 2, url: 'albums', title: 'Albums', icon: ['far', 'images'] },
                { id: 3, url: 'ai', title: 'AI Powered', icon: 'bolt' },
                { id: 4, url: 'favorites', title: 'Favorites', icon: ['far', 'star'] },
                { id: 5, url: 'shared', title: 'Shared', icon: 'retweet' },
                { id: 6, url: 'private', title: 'Private', icon: 'lock' },
                { id: 7, url: 'settings', title: 'Settings', icon: 'gear' }
            ],
            originalFilesData: [],
        }
    },
    computed: {
        ...mapState(['isDragging', 'isLoading', 'filesData', 'groupedFiles', 'searched']),
        left_items() {
            return this.items.slice(0, 5);
        },
        right_items() {
            return this.items.slice(5, 8);
        },
        isLoggedIn() {
            return this.$store.state.access !== '';
        },
        url() {
            return this.$route.meta.url || '';
        },
    },
    mounted() {
        document.body.addEventListener('dragover', this.handleDragOver);
        document.body.addEventListener('dragleave', this.handleDragLeave);
        document.body.addEventListener('drop', this.handleDragDrop);
        window.addEventListener('resize', this.handleResize);

        // Comprobamos que esté autenticado para obtener datos del usuario
        if (this.isLoggedIn) {
            this.fetchUserData();
            // Redireccionamos si la url es HOME y está autenticado
            if (!this.url) {
                this.$router.push('/all');
            } else {
                const selectedItem = this.items.find(item => item.title === this.url);
                if (selectedItem) {
                    this.clickedItemId = selectedItem.id;
                    this.fetchUserData();
                }
            }
        } else {
            this.$router.push('/');
        }
    },
    beforeUnmount() {
        document.body.removeEventListener('dragover', this.handleDragOver);
        document.body.removeEventListener('dragleave', this.handleDragLeave);
        document.body.removeEventListener('drop', this.handleDragDrop);
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        ...mapMutations(['setIsDragging', 'setIsLoading', 'setFilesData', 'setGroupedFiles', 'setSearched']),
        // Cambiar título al entrar en x componente
        onURLEnter() {
            document.title = this.url ? `${this.url} - Kograph` : 'Kograph';
        },
        // Método para el control del ratón al entrar en la zona
        handleDragOver(e) {
            e.preventDefault();
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');
            if (hasFiles & !this.isDragging) {
                this.setIsDragging(true);
                setTimeout(() => {
                    document.getElementById('dropArea').style.opacity = '1';
                }, 25);
            }
        },
        // Método para el control del ratón abandonando la zona
        handleDragLeave(e) {
            e.preventDefault();
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');
            const isOutsideWindow = e.clientY <= 0 || e.clientX <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight;
            if (hasFiles & isOutsideWindow) {
                this.fadeOut();
            }
        },
        // Método para realizar todas las operaciones necesarias al dropear ficheros
        handleDragDrop: async function (e) {
            e.preventDefault();
            this.selectedGroupIds = [];
            this.selectedFileIds = [];
            const hasFiles = Array.from(e.dataTransfer.types).includes('Files');

            // Comprobamos si lo arrastrable es/son un/os fichero/s
            if (hasFiles) {
                this.setIsLoading(true);
                this.fadeOut();

                await this.$refs.allView.addFiles(Array.from(e.dataTransfer.files)); // Añadir ficheros
                await this.$refs.allView.getFiles(); // Conseguir ficheros para mostrarlos
            }
        },
        // Método para quitar con transición el drop area
        fadeOut() {
            document.getElementById('dropArea').style.opacity = '0';
            setTimeout(() => {
                this.setIsDragging(false);
            }, 500);
        },
        // Obtener el userData
        fetchUserData() {
            axios.get(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.access}`
                }
            }).then(response => {
                this.$store.state.user = response.data;
            }).catch(() => {
                notify({
                    group: "foo",
                    title: "Error",
                    text: "Session token has expired.",
                    type: "error"
                }, 5000);
                this.$store.commit('removeAccess');
            });
        },
        selectItem(itemId) {
            this.clickedItemId = itemId;
            this.selected = this.items.find(item => item.id === itemId).url
        },
        hoverItem(itemId) {
            this.activeItemId = itemId;
        },
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
        // Método para conseguir archivos
        async getFiles() {
            await this.$refs.allView.getFiles();
            this.setSearched(false);
        },
        // Método para subir archivos
        async onInputChange(e) {
            await this.$refs.allView.addFiles(Array.from(e.target.files));
            await this.getFiles();
            e.target.value = null;
        },
        // Método para encontrar fotos donde aparecen caras de x fichero
        async searchImage(e) {
            e.stopPropagation();
            this.clicked = false;
            this.setSearched(false);

            // Variables necesarias
            this.setIsLoading(true);
            const token = localStorage.getItem('access');
            const formData = new FormData();
            formData.append('files', e.target.files[0]);
            formData.append('justOne', 'true');

            // Petición para conseguir ficheros donde caras aparecen
            try {
                // Poner mensaje en el loader
                setTimeout(() => {
                    const loader = document.getElementById('loader');
                    if (loader) {
                        const messageParagraph = document.createElement('p');
                        messageParagraph.textContent = 'Please wait. The process will take as long as the number of files you have.';
                        messageParagraph.classList.add('text-[1.2em]', 'text-center');

                        // Animación de aparición de mensaje estilo Windows
                        messageParagraph.animate(
                            [
                                { opacity: 0 },
                                { opacity: 1 }
                            ],
                            {
                                duration: 1500,
                                easing: 'ease-in-out',
                                fill: 'forwards'
                            }
                        );
                        loader.insertBefore(messageParagraph, loader.firstChild);
                    }
                }, 5000)

                // Petición al servidor para conseguir las fotos parecidas
                const response = await axios.post(`${process.env.VUE_APP_SERVER_URL}/file/search_person/`, formData, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data',
                    },
                });

                // Comprobamos si se han encontrado resultados
                if (response.data.length > 0) {
                    // Si es así, los mostramos
                    this.setFilesData(response.data);
                    await this.$refs.allView.groupFilesByMonthAndYear();
                    notify({
                        group: "foo",
                        title: "Success",
                        text: "Identical faces found in this file.",
                        type: "success"
                    }, 5000);
                    this.setSearched(true);
                } else {
                    // Si no es así, mostramos alerta
                    notify({
                        group: "foo",
                        title: "Not found",
                        text: "No identical faces found in this file.",
                        type: "info"
                    }, 5000);
                }
                this.setIsLoading(false);
            } catch (e) {
                this.setIsLoading(false);
            }
        },
        // Método para manejar los resultados de la búsqueda recibidos del componente SearcherItem
        async handleSearchResults(data) {
            this.setIsLoading(true);

            if (!this.originalFilesData.length) {
                this.originalFilesData = [...this.filesData];
                this.originalGroupedFiles = this.groupedFiles;
            }

            // Comprobamos que el usuario haya escrito algo
            if (data.value) {
                this.setFilesData(data.data);
                const filteredGroupedFiles = {};
                Object.keys(this.originalGroupedFiles).forEach(key => {
                    filteredGroupedFiles[key] = this.originalGroupedFiles[key].filter(file => {
                        return data.data.some(dataFile => dataFile.id === file.id);
                    });
                    if (filteredGroupedFiles[key].length === 0) {
                        delete filteredGroupedFiles[key];
                    }
                });

                this.setGroupedFiles({ files: filteredGroupedFiles });
            } else {
                if (data.data.length == this.originalFilesData.length) {
                    this.setFilesData(this.originalFilesData);
                    this.setGroupedFiles({ files: this.originalGroupedFiles });
                } else {
                    this.setFilesData([...data.data]);

                    const filteredGroupedFiles = {};
                    Object.keys(this.originalGroupedFiles).forEach(key => {
                        filteredGroupedFiles[key] = this.originalGroupedFiles[key].filter(file => {
                            return data.data.some(dataFile => dataFile.id === file.id);
                        });
                        if (filteredGroupedFiles[key].length === 0) {
                            delete filteredGroupedFiles[key];
                        }
                    });
                    this.setGroupedFiles({ files: filteredGroupedFiles });
                }
            }

            this.setIsLoading(false);
        },
    },
    components: { HomeView, LogoItem, SearcherItem, UserDropdown, NavItem, DropZone, AllView, AlbumView, AIView, FavoriteView, SharedView, PrivateView, SettingsView }
}
</script>

<template>
    <div>
        <!-- HOME VIEW -->
        <HomeView v-if="!isLoggedIn" />

        <div v-if="isLoggedIn">
            <!-- NAV -->
            <div class="nav">
                <LogoItem @click="this.$router.push('/all')" v-show="pageWidth > 600" />
                <div class="nav_mobile" v-show="pageWidth <= 600"></div>
                <SearcherItem @search-results="handleSearchResults"/>
                <font-awesome-icon v-if="url == 'All' && searched" @click="getFiles" icon="rotate" class="cursor-pointer" />
                <label for="search_image" title="Upload files" v-if="url == 'All' && filesData.length > 0">
                    <svg class="search_image_icon" xmlns="http://www.w3.org/2000/svg" width="17" height="18" viewBox="0 0 17 18"
                        fill="none">
                        <path
                            d="M0 3C0 1.34315 1.34315 0 3 0H11C14.3137 0 17 2.68629 17 6V15C17 16.6569 15.6569 18 14 18H3C1.34315 18 0 16.6569 0 15V3Z"
                            fill="black" class="i1" />
                        <path
                            d="M10.3129 9.65571C10.3129 10.4624 10.0509 11.2076 9.6097 11.8122L11.8352 14.0391C12.0549 14.2588 12.0549 14.6155 11.8352 14.8352C11.6155 15.0549 11.2586 15.0549 11.0389 14.8352L8.81337 12.6084C8.20865 13.0513 7.4633 13.3114 6.65643 13.3114C4.6366 13.3114 3 11.6751 3 9.65571C3 7.63628 4.6366 6 6.65643 6C8.67625 6 10.3129 7.63628 10.3129 9.65571ZM6.65643 12.1866C6.98885 12.1866 7.31802 12.1211 7.62514 11.9939C7.93226 11.8668 8.21132 11.6803 8.44638 11.4453C8.68144 11.2103 8.8679 10.9313 8.99511 10.6242C9.12233 10.3172 9.1878 9.98807 9.1878 9.65571C9.1878 9.32335 9.12233 8.99425 8.99511 8.68719C8.8679 8.38013 8.68144 8.10113 8.44638 7.86611C8.21132 7.6311 7.93226 7.44468 7.62514 7.31749C7.31802 7.1903 6.98885 7.12484 6.65643 7.12484C6.324 7.12484 5.99483 7.1903 5.68771 7.31749C5.38059 7.44468 5.10154 7.6311 4.86648 7.86611C4.63142 8.10113 4.44496 8.38013 4.31774 8.68719C4.19053 8.99425 4.12505 9.32335 4.12505 9.65571C4.12505 9.98807 4.19053 10.3172 4.31774 10.6242C4.44496 10.9313 4.63142 11.2103 4.86648 11.4453C5.10154 11.6803 5.38059 11.8668 5.68771 11.9939C5.99483 12.1211 6.324 12.1866 6.65643 12.1866Z"
                            fill="white" class="i2" />
                        <path d="M16.2188 4.11221L16.6158 5.7H11.3V0.384233L12.89 0.781739L14.981 1.92229L16.2188 4.11221Z"
                            fill="white" stroke="black" stroke-width="0.6" class="i3" />
                    </svg>
                </label>
                <input type="file" id="search_image" @change="searchImage($event)" class="hidden" v-if="url == 'All' && filesData.length > 0"/>
                <label for="file-input" title="Upload files">
                    <font-awesome-icon icon="upload" class="upload" />
                </label>
                <input type="file" id="file-input" multiple @change="onInputChange" class="hidden" />
                <UserDropdown v-show="pageWidth > 600" title="Profile" />
            </div>
            <!-- EXPLORE -->
            <div class="explore" v-show="pageWidth > 600">
                <div class="explore_items">
                    <NavItem v-for="item in left_items" :key="item.id" :title="item.title" :url="item.url" :icon="item.icon"
                        :class="{ active: this.$route.path.split('/')[1] == item.url || this.activeItemId == item.id }"
                        @click="selectItem(item.id)" @mouseover="hoverItem(item.id)" @mouseout="hoverItem(null)" />
                </div>
                <div class="explore_items">
                    <NavItem v-for="item in right_items" :key="item.id" :title="item.title" :url="item.url"
                        :icon="item.icon"
                        :class="{ active: this.$route.path.split('/')[1] == item.url || this.activeItemId == item.id }"
                        @click="selectItem(item.id)" @mouseover="hoverItem(item.id)" @mouseout="hoverItem(null)" />
                </div>
            </div>

            <!-- APP VIEWS -->
            <transition @enter="onURLEnter" appear>
                <AllView v-show="url == 'All' || url == 'Home'" ref="allView" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <AlbumView v-show="url == 'Albums'" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <AIView v-show="url == 'AI Powered'" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <FavoriteView v-show="url == 'Favorites'" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <SharedView v-show="url == 'Shared'" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <PrivateView v-show="url == 'Private'" />
            </transition>
            <transition @enter="onURLEnter" appear>
                <SettingsView v-show="url == 'Settings'" />
            </transition>

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
        </div>
    </div>
</template>

<style scoped>
.nav {
    position: fixed;
    top: 0;
    padding: 10px 45px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    gap: 25px;
    z-index: 99;
    background-color: white !important;
}

body.dark-mode .nav {
    background-color: #242424 !important;
}

.search_image_icon {
    cursor: pointer;
}

body.dark-mode .i1 {
    fill: white !important;
}

body.dark-mode .i2 {
    fill: black !important;
}

body.dark-mode .i3 {
    fill: black !important;
    stroke: white !important;
}

.upload {
    user-select: none;
    cursor: pointer;
}

.explore {
    display: flex;
    justify-content: space-between;
    margin: 65px 30px 20px 30px;
}

.explore_items {
    display: flex;
    gap: 8px;
}

.drop-area {
    z-index: 9999999999;
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

.drop-area label {
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

.drop-area label div {
    color: black;
    display: flex;
    flex-direction: column;
    gap: 20px;
    font-weight: bold;
}

body.dark-mode .drop-area label div {
    color: white !important;
}

.drop-area label div svg {
    font-size: 2em;
    color: #318ba7;
}

.drop-area label input[type=file]:not(:focus-visible) {
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

@keyframes fadeIn {
    from {
        opacity: 0;
        }
    to {
        opacity: 1;
    }
}

@keyframes appearAnimation {
    to {
        opacity: 1;
    }
}

@media screen and (max-width: 600px) {
    .nav {
        padding: 15px 20px 15px 20px;
    }

    .explore {
        display: flex;
        justify-content: space-between;
        margin: 5px 20px 20px 20px;
    }
}
</style>