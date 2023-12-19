<script setup>
import { ref, onMounted } from 'vue'
import ExploreItem from './ExploreItem.vue'

const activeItemId = ref(null)
const clickedItemId = ref(null);

const selectItem = (itemId) => {
    clickedItemId.value = itemId;
}

const hoverItem = (itemId) => {
    activeItemId.value = itemId;
};

const left_items = ref([
    { id: 1, title: 'All', icon: ['far', 'image'] },
    { id: 2, title: 'Albums', icon: ['far', 'images'] },
    { id: 3, title: 'AI Categories', icon: 'bolt' },
    { id: 4, title: 'Favorites', icon: ['far', 'star'] },
    { id: 5, title: 'Shared', icon: 'retweet' }
])

const right_items = ref([
    { id: 6, title: 'Private', icon: 'lock' },
    { id: 7, title: 'Recycle Bin', icon: ['far', 'trash-can'] },
    { id: 8, icon: 'gear' }
])

onMounted(() => {
    if (left_items.value.length > 0) {
        clickedItemId.value = left_items.value[0].id;
    }
});
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
</template>
  
<style>
.explore {
    display: flex;
    justify-content: space-between;
    margin: 5px 30px;
}
.explore_items {
    display: flex;
    gap: 8px;
}
</style>