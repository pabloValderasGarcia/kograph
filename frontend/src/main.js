// App
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import Notifications from 'notiwind';
import './assets/css/main.css';

// Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
// Explorar
import { faImage } from '@fortawesome/free-regular-svg-icons';
import { faImages } from '@fortawesome/free-regular-svg-icons';
import { faBolt } from '@fortawesome/free-solid-svg-icons';
import { faStar } from '@fortawesome/free-regular-svg-icons';
import { faRetweet } from '@fortawesome/free-solid-svg-icons';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import { faTrashCan } from '@fortawesome/free-regular-svg-icons';
import { faGear } from '@fortawesome/free-solid-svg-icons';
// Otros
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';
import { faPenToSquare } from '@fortawesome/free-solid-svg-icons';
import { faEye } from '@fortawesome/free-solid-svg-icons';
import { faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
// Usuario
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
// Notificaciones
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import { faCircleCheck } from '@fortawesome/free-solid-svg-icons';
import { faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { faCircleExclamation } from '@fortawesome/free-solid-svg-icons';
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import { faXmark } from '@fortawesome/free-solid-svg-icons';
// Ficheros
import { faCircle as regularCircle } from '@fortawesome/free-solid-svg-icons';
import { faCircle as solidCircle } from '@fortawesome/free-regular-svg-icons';
import { faVideo } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
library.add(
    faImage, faImages, faBolt, faStar, faRetweet, faLock, faTrashCan, faGear, faMagnifyingGlass,
    faPenToSquare, faEye, faCloudArrowUp, faCaretDown, faUser, faRightFromBracket, faInfoCircle, 
    faCircleCheck, faCircleXmark, faCircleExclamation, faTriangleExclamation, faXmark, regularCircle,
    solidCircle, faVideo, faPlus, faUpload
);

// Axios
axios.interceptors.request.use((config) => {
    const token = store.state.token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Dark Mode
if (!eval(localStorage.getItem('darkModeChanged'))) {
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    document.body.classList.toggle('dark-mode', darkModeMediaQuery.matches);
    localStorage.setItem('darkMode', darkModeMediaQuery.matches)
} else {
    store.commit('setDarkMode', eval(localStorage.getItem('darkMode')));
}

// Create App
const app = createApp(App);
app.use(store).use(router, axios, Notifications).component('font-awesome-icon', FontAwesomeIcon).mount('#app');