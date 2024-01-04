<script>
export default {
    name: 'ButtonItem',
    props: ['url', 'title']
}
</script>

<template>
    <button @click="url && $router.push(url)">{{ title }}</button>
</template>

<style scoped>
button {
    user-select: none;
    font-size: 16px;
    cursor: pointer;
    border: none;
    padding: 12px 40px;
    border-radius: 5px;
    background-color: #318ba7;
    color: white;
    transition: all .1s ease-in-out;
}

button:hover {
    background-color: #2a7b93;
}

body.dark-mode button {
    background-color: #373737 !important;
}

body.dark-mode button:hover {
    background-color: #464646 !important;
}
</style>