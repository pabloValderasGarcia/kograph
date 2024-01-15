<script>
export default {
    name: 'NavItem',
    data() {
        return {
            pageWidth: window.innerWidth
        }
    },
    props: ['title', 'url', 'icon'],
    mounted() {
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
    }
}
</script>

<template>
    <div @click="$router.push('/' + url)" class="explore_item" :style="{ 'padding': pageWidth > 1100 ? '13px 20px' : '13px 13px' }">
        <font-awesome-icon :icon="icon" />
        <p v-if="pageWidth > 1100 && title && title != 'Settings'">{{ title }}</p>
    </div>
</template>
  
<style scoped>
.explore_item {
    user-select: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    border-radius: 5px;
    font-weight: 500;
}

.active {
    background-color: #ececec;
}

body.dark-mode .active {
    background-color: #373737 !important;
}
</style>