<script>
export default {
    name: 'SearcherItem',
    data() {
        return {
            clicked: false,
        }
    },
    props: ['url'],
    methods: {
        close(e) {
            if (!this.$el.contains(e.target)) {
                this.clicked = false;
            }
        },
        search() {

        },
    },
    mounted() {
        document.addEventListener('click', this.close)
    },
    beforeUnmount() {
        document.removeEventListener('click', this.close)
    },
}
</script>

<template>
    <div class="searcher" @click="clicked = true">
        <input name="search" class="input_searcher" :class="{ '!pl-[25px]': clicked }"
            placeholder="Explore your memories" />
        <font-awesome-icon icon="magnifying-glass" class="search_icon" v-if="!clicked" />
    </div>
</template>

<style>
.searcher {
    position: relative;
    user-select: none;
    flex: 1;
}

.input_searcher {
    width: 100%;
    box-sizing: border-box;
    outline: none;
    border: none;
    border-radius: 20px !important;
    background-color: #ececec;
    padding: 10px 25px 10px 50px;
    font-size: 16px;
}

body.dark-mode .input_searcher {
    color: white !important;
    background-color: #373737 !important;
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