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
// Regular Icons
import { faImage, faImages, faStar, faTrashCan, faCircle as solidCircle, faClock, faFileLines } from '@fortawesome/free-regular-svg-icons';
// Solid Icons
import { faBolt, faRotate, faRetweet, faLock, faGear, faMagnifyingGlass, faPenToSquare, faEye, 
    faCloudArrowUp, faCaretDown, faChevronLeft, faArrowLeft, faUser, faRightFromBracket, faInfoCircle, 
    faCircleCheck, faCircleXmark, faCircleExclamation, faTriangleExclamation, faXmark, faCircle as regularCircle, 
    faVideo, faPlus, faUpload, faHashtag, faSpinner, faFloppyDisk, faMicrophone, faEnvelope, faChartSimple, faCookieBite
} from '@fortawesome/free-solid-svg-icons';
// Add to library
library.add(
    faImage, faImages, faBolt, faStar, faRetweet, faLock, faTrashCan, faGear, faMagnifyingGlass,
    faPenToSquare, faEye, faCloudArrowUp, faCaretDown, faChevronLeft, faArrowLeft, faUser, faRightFromBracket, 
    faInfoCircle, faCircleCheck, faCircleXmark, faCircleExclamation, faTriangleExclamation, faXmark, faRotate,
    regularCircle, solidCircle, faVideo, faPlus, faUpload, faClock, faFileLines, faHashtag, faSpinner, faFloppyDisk,
    faMicrophone, faEnvelope, faChartSimple, faCookieBite
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