<script>
import ExploreApp from '@/components/explore/ExploreApp.vue';
import NavApp from '@/components/nav/NavApp.vue';
import axios from 'axios';

export default {
    name: 'AppView',
    mounted() {
        const accessData = {
            refresh: this.$store.state.refresh
        }
        axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/refresh/`, accessData).then(response => {
            const access = response.data.access;
            localStorage.setItem('access', access);
            this.$store.commit('setAccess', access);
        }).catch(() => { })
        
        axios.get(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, {
            headers: {
                'Authorization': `Bearer ${this.$store.state.access}`
            }
        }).then(response => {
            this.$store.state.user = response.data;
        }).catch(error => {
            console.log(error);
        })
    },
    components: { NavApp, ExploreApp }
}
</script>

<template>
    <NavApp />
    <ExploreApp />
</template>