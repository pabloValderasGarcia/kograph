<script setup>
import LogoItem from './LogoItem.vue'
import SearcherItem from './SearcherItem.vue';
import UserItem from './UserItem.vue';
</script>

<template>
    <div class="nav">
        <router-link to="/"><LogoItem /></router-link>
        <SearcherItem />
        <UserItem />
    </div>
</template>

<style>
.nav {
    padding: 10px 45px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    gap: 30px;
}
.search_tools {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>