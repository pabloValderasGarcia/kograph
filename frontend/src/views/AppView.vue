<script>
import AppSelection from '@/components/app/AppSelection.vue';
import SearcherItem from '@/components/nav/SearcherItem.vue';
import UserDropdown from '@/components/nav/UserDropdown.vue';
import ExploreItem from '@/components/app/ExploreItem.vue'
import LogoItem from '@/components/nav/LogoItem.vue';
import { notify } from 'notiwind';
import axios from 'axios';

export default {
    name: 'AppView',
    data() {
        return {
            pageWidth: window.innerWidth,
            activeItemId: null,
            clickedItemId: null,
            selected: 'all',
            items: [
                { id: 1, url: 'all', title: 'All', icon: ['far', 'image'] },
                { id: 2, url: 'albums', title: 'Albums', icon: ['far', 'images'] },
                { id: 3, url: 'ai', title: 'AI Categories', icon: 'bolt' },
                { id: 4, url: 'favorites', title: 'Favorites', icon: ['far', 'star'] },
                { id: 5, url: 'shared', title: 'Shared', icon: 'retweet' },
                { id: 6, url: 'private', title: 'Private', icon: 'lock' },
                { id: 7, url: 'trash', title: 'Recycle Bin', icon: ['far', 'trash-can'] },
                { id: 8, url: 'settings', title: 'Settings', icon: 'gear' }
            ]
        }
    },
    mounted() {
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    created() {
        this.clickedItemId = this.left_items[0].id;

        axios.get(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, {
            headers: {
                'Authorization': `Bearer ${this.$store.state.access}`
            }
        }).then(response => {
            this.$store.state.user = response.data;
        }).catch(() => {
            notify({
                group: "foo",
                title: "Error",
                text: "Session token has expired.",
                type: "error"
            }, 5000);
            this.$store.commit('removeAccess');
        })
    },
    computed: {
        left_items() {
            return this.items.slice(0, 5);
        },
        right_items() {
            return this.items.slice(5, 8);
        },
    },
    methods: {
        selectItem(itemId) {
            this.clickedItemId = itemId;
            this.selected = this.items.find(item => item.id === itemId).url
            document.title = this.items.find(item => item.id === itemId).title + ' - Kograph';
        },
        hoverItem(itemId) {
            this.activeItemId = itemId;
        },
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
    },
    components: { LogoItem, SearcherItem, UserDropdown, ExploreItem, AppSelection }
}
</script>

<template>
    <!-- NAV -->
    <div class="nav">
        <LogoItem @click="selectItem(1)" v-if="pageWidth > 600" />
        <div class="nav_mobile" v-if="pageWidth <= 600"></div>
        <SearcherItem />
        <UserDropdown v-if="pageWidth > 600" />
    </div>
    <!-- EXPLORE -->
    <div class="explore" v-if="pageWidth > 600">
        <div class="explore_items">
            <ExploreItem v-for="item in left_items" :key="item.id" :title="item.title" :icon="item.icon"
                :class="{ active: activeItemId === item.id || clickedItemId === item.id }" @click="selectItem(item.id)"
                @mouseover="hoverItem(item.id)" @mouseout="hoverItem(null)" />
        </div>
        <div class="explore_items">
            <ExploreItem v-for="item in right_items" :key="item.id" :title="item.title" :icon="item.icon"
                :class="{ active: activeItemId === item.id || clickedItemId === item.id }" @click="selectItem(item.id)"
                @mouseover="hoverItem(item.id)" @mouseout="hoverItem(null)" />
        </div>
    </div>
    <AppSelection :item="selected" @updateSelected="(newSelected) => selected.value = newSelected" />
</template>

<style scoped>
.nav {
    position: sticky;
    padding: 10px 45px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    gap: 30px;
}

.nav_mobile {

}

.explore {
    display: flex;
    justify-content: space-between;
    margin: 5px 30px 20px 30px;
}

.explore_items {
    display: flex;
    gap: 8px;
}

@media screen and (max-width: 600px) {
    .nav {
        padding: 15px 20px 15px 20px;
    }

    .explore {
        display: flex;
        justify-content: space-between;
        margin: 5px 20px 20px 20px;
    }
}
</style>