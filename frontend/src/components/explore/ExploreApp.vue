<script>
import ExploreItem from './ExploreItem.vue'
import AppSelection from '@/components/app/AppSelection.vue'

export default {
    name: 'ExploreApp',
    data() {
        return {
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
    computed: {
        left_items() {
            return this.items.slice(0, 5);
        },
        right_items() {
            return this.items.slice(5, 8);
        },
    },
    mounted() {
        this.clickedItemId = this.left_items[0].id;
    },
    methods: {
        selectItem(itemId) {
            this.clickedItemId = itemId;
            this.selected = this.items.find(item => item.id === itemId).url
            document.title = this.items.find(item => item.id === itemId).title + ' - Kograph';
        },
        hoverItem(itemId) {
            this.activeItemId = itemId;
        }
    },
    components: { ExploreItem, AppSelection }
}
</script>

<template>
    <div class="explore">
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
.explore {
    display: flex;
    justify-content: space-between;
    margin: 5px 30px 20px 30px;
}

.explore_items {
    display: flex;
    gap: 8px;
}
</style>