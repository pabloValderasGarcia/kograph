<script>
import { NotificationGroup, Notification } from 'notiwind';
import ButtonItem from '@/components/others/ButtonItem.vue';
import { FwbModal } from 'flowbite-vue';
import { notify } from 'notiwind';
import '@/assets/css/main.css';
import axios from 'axios';

export default {
    name: 'App',
    data() {
        return {
            uploaded_success_open: false,
            uploaded_error_open: false,
            showCookies: localStorage.getItem('cookies') ? false : true
        }
    },
    beforeCreate() {
        const access = this.$store.state.access;
        if (access) {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
        } else {
            axios.defaults.headers.common['Authorization'] = '';
        }
    },
    mounted() {
        setInterval(() => {
            if (this.$store.state.access) this.getAccess();
        }, 59000);
    },
    methods: {
        // Método para conseguir acceso a la aplicación y actualizar token cada minuto
        getAccess() {
            const accessData = {
                refresh: this.$store.state.refresh
            }

            // Petición actualizar token
            axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/refresh/`, accessData).then(response => {
                const access = response.data.access;
                this.$store.commit('setAccess', access);
            }).catch(() => {
                // Si no tenemos acceso, lo quitamos
                this.$store.commit('removeAccess');
                notify({
                    group: "foo",
                    title: "Error",
                    text: "Token session has expired.",
                    type: "error"
                }, 4000);
            })
        },
        // Método para administración de cookies
        cookies(req) {
            switch(req) {
                case 'customize':
                    break;
                case 'reject':
                    this.closeCookies();
                    localStorage.setItem('cookies', false);
                    break;
                case 'accept':
                    this.closeCookies();
                    localStorage.setItem('cookies', true);
                    break;
            }
        },
        // Método para cerrar modal de cookies
        closeCookies() {
            this.showCookies = false;
        },
        // Método para evitar que el modal se cierre al darle a Escape
        handleKeyDown(event) {
            if (event.key === 'Escape' && this.showCookies) {
                event.preventDefault();
            }
        },
    },
    components: { NotificationGroup, Notification, FwbModal, ButtonItem }
}
</script>

<template>
    <div id="app">
        <!-- ROUTES -->
        <router-view />

        <!-- NOTIFICATIONS -->
        <NotificationGroup group="foo">
            <div class="z-[99999] fixed inset-0 flex items-end justify-end p-6 px-4 py-6 pointer-events-none alert-container">
                <div class="w-full">
                    <!-- ALERTS -->
                    <Notification v-slot="{ notifications, close }" enter="transform ease-out duration-300 transition"
                        enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
                        enter-to="translate-y-0 opacity-100 sm:translate-x-0" leave="transition ease-in duration-500"
                        leave-from="opacity-100" leave-to="opacity-0" move="transition duration-500" move-delay="delay-300">
                        <div v-for="notification in notifications" :key="notification.id">
                            <!-- INFO -->
                            <div v-if="notification.type === 'info'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto relative">
                                <div class="flex items-center justify-center px-4 bg-blue-500">
                                    <font-awesome-icon icon="circle-info" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-blue-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                                <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                            </div>
                            <!-- SUCCESS -->
                            <div v-if="notification.type === 'success'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto relative">
                                <div class="flex items-center justify-center px-4 bg-green-500">
                                    <font-awesome-icon icon="circle-check" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-green-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                                <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                            </div>
                            <!-- WARNING -->
                            <div v-if="notification.type === 'warning'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto relative">
                                <div class="flex items-center justify-center px-4 bg-yellow-500">
                                    <font-awesome-icon icon="circle-exclamation" class="text-white" />
                                    <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-yellow-400">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                                <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                            </div>
                            <!-- ERROR -->
                            <div v-if="notification.type === 'error'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto relative">
                                <div class="flex items-center justify-center px-4 bg-red-500">
                                    <font-awesome-icon icon="triangle-exclamation" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-red-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                                <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                            </div>
                        </div>
                    </Notification>
                    <!-- FILES -->
                    <Notification v-slot="{ notifications, close }" enter="transform ease-out transition"
                        enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
                        enter-to="translate-y-0 opacity-100 sm:translate-x-0" leave="transition ease-in"
                        leave-from="opacity-100" leave-to="opacity-0" move="transition" move-delay="delay-300">
                        <div v-for="notification in notifications" :key="notification.id">
                            <!-- UPLOADED FILES -->
                            <div v-if="notification.type === 'uploaded_info'" id="uploaded_alert"
                                class="flex w-fit min-w-[25rem] ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto">
                                <div class="flex px-4 pt-3 bg-blue-500">
                                    <font-awesome-icon :icon="['far', 'image']" class="text-white" />
                                </div>
                                <div class="w-full">
                                    <div class="relative">
                                        <p class="font-semibold text-black select-none cursor-pointer py-3 px-4" @click="uploaded_success_open = !uploaded_success_open"><font-awesome-icon icon="caret-down" class="mr-1 transition-all" :class="!uploaded_success_open ? 'rotate-180' : ''"/> {{ notification.title }}</p>
                                        <div class="pb-3 px-4 max-h-[300px] overflow-y-auto uploaded_files" :class="!uploaded_success_open ? '': 'hidden'">
                                            <div class="flex flex-col gap-2" id="uploaded_alert_content">
                                                <div class="flex items-center w-[313px] overflow-hidden" id="uploaded_count"></div>
                                                <hr class="mb-1 border-1 border-solid border-black"/>
                                            </div>
                                        </div>
                                        <font-awesome-icon @click="close(notification.id)" icon="xmark" class="text-black absolute top-2 right-3 cursor-pointer" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Notification>
                </div>
            </div>
        </NotificationGroup>

        <!-- COOKIES -->
        <fwb-modal class="my_modal cookies" v-if="showCookies" @close="closeCookies" @keydown.prevent="handleKeyDown">
            <template #header>
                <div class="flex items-center gap-3">
                    <font-awesome-icon icon="cookie-bite" class="text-amber-600" />Cookies Settings
                </div>
            </template>
            <template #body>
                We use cookies to enhance your browsing experience and provide personalized content on our website. Cookies are small text files that are stored on your device when you visit a website. They help us remember your preferences and improve the functionality of our site.
            </template>
            <template #footer>
                <div class="modal_buttons cookies_buttons">
                    <ButtonItem title="Customize" @click="cookies('customize')"/>
                    <ButtonItem title="Reject All" @click="cookies('reject')"/>
                    <ButtonItem title="Accept All" @click="cookies('accept')"/>
                </div>
            </template>
        </fwb-modal>
    </div>
</template>

<style>
    /* COOKIES */
    .cookies > div:last-child {
        pointer-events: none !important;
    }
    .cookies > div:last-child > div {
        display: flex !important;
        align-items: center;
        max-width: 800px !important;
    }
    .cookies > div:last-child > div > div {
        pointer-events: visible !important;
    }
    .cookies > div:last-child > div > div > *:first-child {
        padding: 1.2rem 1.5rem 1rem 1.5rem !important;
    }
    .cookies > div:last-child > div > div > *:last-child {
        padding: 1rem 1.5rem 1.2rem 1.5rem !important;
    }
    .cookies > div:last-child > div > div > div:first-child > button {
        display: none !important;
    }
    .cookies > div:last-child > div > div > *:not(:first-child, :last-child) {
        padding: 1rem 1.5rem !important;
        line-height: 1.4em !important;
    }
    .cookies_buttons button:first-child {
        background-color: #ececec !important;
        color: black;
    }
    .cookies_buttons button:first-child:hover {
        background-color: #e1e1e1 !important;
    }
    body.dark-mode .cookies_buttons button:first-child {
        background-color: #373737 !important;
        color: white;
    }
    body.dark-mode .cookies_buttons button:first-child:hover {
        background-color: #464646 !important;
    }
    .cookies_buttons button:nth-child(2) {
        background-color: #c14040 !important;
    }
    .cookies_buttons button:nth-child(2):hover {
        background-color: #ab3c3c !important;
    }
</style>