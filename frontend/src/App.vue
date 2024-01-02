<script>
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
            }).catch(() => {})
        }
    }
}
</script>

<template>
    <router-view />
</template>