<script>
import { NotificationGroup, Notification } from 'notiwind';
import '@/assets/css/main.css'
import axios from 'axios'

export default {
    name: 'App',
    beforeCreate() {
        const access = this.$store.state.access;
        if (access) {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
        } else {
            axios.defaults.headers.common['Authorization'] = '';
        }
    },
    mounted() {
        if (this.$store.state.access) {
            setInterval(() => {
                this.getAccess();
            }, 59000);
        }
    },
    methods: {
        getAccess() {
            const accessData = {
                refresh: this.$store.state.refresh
            }

            axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/refresh/`, accessData).then(response => {
                const access = response.data.access;
                localStorage.setItem('access', access);
                this.$store.commit('setAccess', access);
            }).catch(() => { })
        },
        closeNotification(id) {
            const index = this.notifications.findIndex(notification => notification.id === id);
            if (index !== -1) {
                this.notifications.splice(index, 1);
            }
        }
    },
    components: { NotificationGroup, Notification }
}
</script>

<template>
    <div id="app">
        <router-view />
        <NotificationGroup group="foo">
            <div class="fixed inset-0 flex items-end justify-end p-6 px-4 py-6 pointer-events-none">
                <div class="w-full max-w-sm">
                    <Notification 
                        v-slot="{ notifications }" 
                        enter="transform ease-out duration-300 transition"
                        enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
                        enter-to="translate-y-0 opacity-100 sm:translate-x-0"
                        leave="transition ease-in duration-500"
                        leave-from="opacity-100"
                        leave-to="opacity-0"
                        move="transition duration-500"
                        move-delay="delay-300"
                        @close="closeNotification"
                    >
                        <div v-for="notification in notifications" :key="notification.id">
                            <!-- INFO -->
                            <div v-if="notification.type === 'info'" class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md">
                                <div class="flex items-center justify-center px-4 bg-blue-500">
                                    <font-awesome-icon icon="circle-info" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-blue-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- SUCCESS -->
                            <div v-if="notification.type === 'success'" class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md">
                                <div class="flex items-center justify-center px-4 bg-green-500">
                                    <font-awesome-icon icon="circle-check" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-green-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- WARNING -->
                            <div v-if="notification.type === 'warning'" class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md">
                                <div class="flex items-center justify-center px-4 bg-yellow-500">
                                    <font-awesome-icon icon="circle-exclamation" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-yellow-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- ERROR -->
                            <div v-if="notification.type === 'error'" class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md">
                                <div class="flex items-center justify-center px-4 bg-red-500">
                                    <font-awesome-icon icon="triangle-exclamation" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-red-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Notification>
                </div>
            </div>
        </NotificationGroup>
    </div>
</template>