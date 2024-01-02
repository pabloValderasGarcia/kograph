<script>
import '@/assets/css/components/input.css';

export default {
    name: 'SearcherItem',
    data() {
        return {
            clicked: false
        }
    },
    methods: {
        close(e) {
            if (!this.$el.contains(e.target)) {
                this.clicked = false;
            }
        }
    },
    mounted() {
        document.addEventListener('click', this.close)
    },
    beforeUnmount() {
        document.removeEventListener('click', this.close)
    }
}
</script>

<template>
    <div class="searcher" @click="clicked = true">
        <input class="input searcher" :class="{'left_padding': clicked}" placeholder="Explore your memories" />
        <font-awesome-icon icon="magnifying-glass" class="search_icon" v-if="!clicked"/>
    </div>
</template>

<style scoped>
.searcher {
    position: relative;
    user-select: none;
    flex: 1;
}

.searcher input {
    width: 100%;
    box-sizing: border-box;
    padding-left: 50px;
}

.left_padding {
    padding-left: 25px !important;
}

.search_icon {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-55%);
    opacity: .6;
    pointer-events: none;
}
</style>