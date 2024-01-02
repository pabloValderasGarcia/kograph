<script>
import AppView from './AppView.vue';
import HomeView from './HomeView.vue';

export default {
    name: 'RootView',
    beforeCreate() {
        document.title = this.$store.state.access !== '' ? 'All - Kograph' : 'Home - Kograph';
    },
    computed: {
        isLoggedIn() {
            return this.$store.state.access !== '';
        }
    },
    components: { HomeView, AppView }
}
</script>

<template>
    <HomeView v-if="!isLoggedIn"/>
    <AppView v-if="isLoggedIn"/>
</template>