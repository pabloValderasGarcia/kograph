// Imports App
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Imports Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faImage } from '@fortawesome/free-regular-svg-icons'
import { faImages } from '@fortawesome/free-regular-svg-icons'
import { faBolt } from '@fortawesome/free-solid-svg-icons'
import { faStar } from '@fortawesome/free-regular-svg-icons'
import { faRetweet } from '@fortawesome/free-solid-svg-icons'
import { faLock } from '@fortawesome/free-solid-svg-icons'
import { faTrashCan } from '@fortawesome/free-regular-svg-icons'
import { faGear } from '@fortawesome/free-solid-svg-icons'
library.add(faImage, faImages, faBolt, faStar, faRetweet, faLock, faTrashCan, faGear)

// Create App
const app = createApp(App);
app.use(router);
app.use(store);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');