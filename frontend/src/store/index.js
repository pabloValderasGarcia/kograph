import { createStore } from 'vuex';
import axios from 'axios'

export default createStore({
    state: {
        // Access
        access: '',
        refresh: '',
        user: null,
        // Dark mode
        darkMode: true,
        // Ficheros
        searchValue: '',
        isDragging: false,
        isLoading: false,
        files: [],
        filesData: [],
        originalFilesData: [],
        groupedFiles: {},
        originalGroupedFiles: [],
        selectedFiles: [],
        searched: false,
        // AI
        aiMap: null,
        aiMapElement: null,
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('access')) {
                state.access = localStorage.getItem('access');
                state.refresh = localStorage.getItem('refresh');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.access;
            }
        },
        // Acceso
        setAccess(state, access) {
            state.access = access;
            localStorage.setItem('access', access);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
        },
        setRefresh(state, refresh) {
            state.refresh = refresh;
            localStorage.setItem('refresh', refresh);
        },
        removeAccess(state) {
            state.access = '';
            state.refresh = '';
            state.user = null;
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            localStorage.removeItem('darkMode');
            localStorage.setItem('darkModeChanged', false);
            delete axios.defaults.headers.common['Authorization'];
        },
        // Dark mode
        setDarkMode(state, value) {
            localStorage.setItem('darkMode', value);
            document.body.classList.toggle('dark-mode', eval(value));
            this.darkMode = eval(value);
            window.dispatchEvent(new Event('darkModeChanged'));
        },
        setDarkModeChanged(state, value) {
            localStorage.setItem('darkModeChanged', true);
            this.commit('setDarkMode', value);
        },
        // Ficheros
        setSearchValue(state, value) {
            state.searchValue = value;
        },
        setIsDragging(state, value) {
            state.isDragging = value;
        },
        setIsLoading(state, value) {
            state.isLoading = value;
        },
        setFiles(state, files) {
            state.files = files;
        },
        setFilesData(state, filesData) {
            state.filesData = filesData;
        },
        setOriginalFilesData(state, originalFilesData) {
            state.originalFilesData = originalFilesData;
        },
        setGroupedFiles(state, payload) {
            const { key, files } = payload;
            if (key) {
                if (files.length == 0) {
                    delete state.groupedFiles[key];
                } else {
                    if (!state.groupedFiles[key]) {
                        state.groupedFiles[key] = [];
                    }
                    state.groupedFiles[key].push(files);
                }
            } else state.groupedFiles = files;
        },
        setOriginalGroupedFiles(state, payload) {
            const { key, files } = payload;
            if (key) {
                if (files.length == 0) {
                    delete state.originalGroupedFiles[key];
                } else {
                    state.originalGroupedFiles[key].push(files);
                }
            } else state.originalGroupedFiles = files;
        },
        setSelectedFiles(state, selectedFiles) {
            state.selectedFiles = selectedFiles;
        },
        setSearched(state, value) {
            state.searched = value;
        },
        // AI
        setAIMap(state, value) {
            state.aiMap = value;
        },
        setAIMapElement(state, value) {
            state.aiMapElement = value;
        }
    },
});