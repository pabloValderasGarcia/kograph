<script>
import LogoItem from './LogoItem.vue';
import SearcherItem from './SearcherItem.vue';
import UserDropdown from './UserDropdown.vue';

export default {
    name: 'NavApp',
    components: { LogoItem, SearcherItem, UserDropdown }
}
</script>

<template>
    <div class="nav">
        <router-link to="/"><LogoItem /></router-link>
        <SearcherItem />
        <UserDropdown />
    </div>
</template>

<style scoped>
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