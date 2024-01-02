<script>
export default {
    name: 'ExploreItem',
    props: ['title', 'icon']
}
</script>

<template>
    <div class="explore_item">
        <font-awesome-icon :icon="icon" />
        <p v-if="title && title != 'Settings'">{{ title }}</p>
    </div>
</template>
  
<style scoped>
.explore_item {
    user-select: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px;
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