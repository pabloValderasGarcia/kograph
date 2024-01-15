<script>
import { NotificationGroup, Notification } from 'notiwind';
import { notify } from 'notiwind';
import '@/assets/css/main.css'
import axios from 'axios'

export default {
    name: 'App',
    data() {
        return {
            uploaded_success_open: false,
            uploaded_error_open: false,
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
        getAccess() {
            const accessData = {
                refresh: this.$store.state.refresh
            }

            axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/refresh/`, accessData).then(response => {
                const access = response.data.access;
                this.$store.commit('setAccess', access);
            }).catch(() => {
                this.$store.commit('removeAccess');
                notify({
                    group: "foo",
                    title: "Error",
                    text: "Token session has expired.",
                    type: "error"
                }, 4000);
            })
        }
    },
    components: { NotificationGroup, Notification }
}
</script>

<template>
    <div id="app">
        <router-view />
        <NotificationGroup group="foo">
            <div class="z-[99999] fixed inset-0 flex items-end justify-end p-6 px-4 py-6 pointer-events-none">
                <div class="w-full">
                    <!-- ALERTS -->
                    <Notification v-slot="{ notifications }" enter="transform ease-out duration-300 transition"
                        enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
                        enter-to="translate-y-0 opacity-100 sm:translate-x-0" leave="transition ease-in duration-500"
                        leave-from="opacity-100" leave-to="opacity-0" move="transition duration-500" move-delay="delay-300">
                        <div v-for="notification in notifications" :key="notification.id">
                            <!-- INFO -->
                            <div v-if="notification.type === 'info'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto">
                                <div class="flex items-center justify-center px-4 bg-blue-500">
                                    <font-awesome-icon icon="circle-info" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-blue-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- SUCCESS -->
                            <div v-if="notification.type === 'success'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto">
                                <div class="flex items-center justify-center px-4 bg-green-500">
                                    <font-awesome-icon icon="circle-check" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-green-500">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- WARNING -->
                            <div v-if="notification.type === 'warning'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto">
                                <div class="flex items-center justify-center px-4 bg-yellow-500">
                                    <font-awesome-icon icon="circle-exclamation" class="text-white" />
                                </div>
                                <div class="px-4 py-2 -mx-3">
                                    <div class="mx-3">
                                        <span class="font-semibold text-yellow-400">{{ notification.title }}</span>
                                        <p class="text-sm text-gray-600 leading-4 mt-1">{{ notification.text }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- ERROR -->
                            <div v-if="notification.type === 'error'"
                                class="flex w-full max-w-sm ml-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md pointer-events-auto">
                                <div class="flex items-center justify-center px-4 bg-red-500">
                                    <font-awesome-icon icon="triangle-exclamation" class="text-white" />
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
                                        <div class="pb-3 px-4 max-h-[300px] overflow-y-auto" :class="!uploaded_success_open ? '': 'hidden'">
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
    </div>
</template>