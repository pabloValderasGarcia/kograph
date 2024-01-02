<script setup>
import { defineProps, ref, watchEffect } from 'vue';
import { MasonryGrid } from "@egjs/vue-grid";
const props = defineProps(['item'])
const selectedValue = ref(props.item);

// Masonry
const gap = ref(5);
const align = ref('justify');

watchEffect(() => {
    selectedValue.value = props.item;
});
</script>

<template>
    <div class="selection" v-if="selectedValue == 'all'">
        2022-01-03
        <masonry-grid class="container" v-bind:gap="gap" v-bind:align="align">
            IMAGEN
        </masonry-grid>
    </div>
</template>

<style scoped>
.selection {
    display: grid;
    justify-content: space-between;
    margin: 5px 30px;
}
</style>