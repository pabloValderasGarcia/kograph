<script>
export default {
    name: 'ExploreItem',
    data() {
        return {
            pageWidth: window.innerWidth
        }
    },
    props: ['title', 'icon'],
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
    <div class="explore_item" :style="{ 'padding': pageWidth > 1050 ? '14px 20px' : '14px 14px' }">
        <font-awesome-icon :icon="icon" />
        <p v-if="pageWidth > 1050 && title && title != 'Settings'">{{ title }}</p>
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