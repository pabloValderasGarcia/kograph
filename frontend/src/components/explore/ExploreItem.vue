<script setup>
import { defineProps } from 'vue'

defineProps(['title', 'icon'])
</script>

<template>
    <div class="explore_item">
        <font-awesome-icon :icon="icon" />
        <p v-if="title">{{ title }}</p>
    </div>
</template>
  
<style>
.explore_item {
    /* Box */
    user-select: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    border-radius: 5px;
    /* Text */
    font-weight: 500;
}
.active {
    background-color: #e9e9e9;
}
</style>