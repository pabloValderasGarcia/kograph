<script>
export default {
    name: 'UserPicture',
    methods: {
        // Conseguir ruta de la foto de perfil
        fullPictureUrl(picture_path) {
            return `${process.env.VUE_APP_SERVER_URL}${picture_path}`;
        },
    },
}
</script>

<template>
    <div class="picture" :style="{ 'background-image': `url(${this.$store.state.user && this.$store.state.user.picture ? fullPictureUrl(this.$store.state.user.picture) : require('@/assets/img/defaultUser.png')})` }"></div>
</template>

<style>
.picture {
    cursor: pointer;
    width: 38px;
    aspect-ratio: 1/1;
    border-radius: 50%;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
}
</style>