<script>
// Enable the "jsx" plugin
/* @jsx h */
export default {
    name: 'DropZone',
    data() {
        return {
            active: false,
            inActiveTimeout: null,
            events: ['dragenter', 'dragover', 'dragleave', 'drop'],
        };
    },
    mounted() {
        this.events.forEach((eventName) => {
            document.body.addEventListener(eventName, this.preventDefault);
        });
    },
    unmounted() {
        this.events.forEach((eventName) => {
            document.body.removeEventListener(eventName, this.preventDefault);
        });
    },
    methods: {
        setActive() {
            this.active = true;
            clearTimeout(this.inActiveTimeout);
        },
        setInactive() {
            this.inActiveTimeout = setTimeout(() => {
                this.active = false;
            }, 500);
        },
        preventDefaults(e) {
            e.preventDefault();
        },
        onDrop(e) {
            this.setInactive();
            this.$emit('files-dropped', [...e.dataTransfer.files]);
        },
        getChildrenTextContent(children) {
            return children
                .filter(child => typeof child === 'string')
                .join(' ');
        }
    },
    render(createElement) {
        var dropZoneId = this.getChildrenTextContent(this.$slots.default)
            .toLowerCase()
            .replace(/\W+/g, '-')
            .replace(/(^-|-$)/g, '');

        return createElement('div', {
            attrs: {
                'data-active': this.active
            },
            on: {
                dragenter: (event) => {
                    event.preventDefault();
                    this.setActive();
                },
                dragover: (event) => {
                    event.preventDefault();
                    this.setActive();
                },
                dragleave: (event) => {
                    event.preventDefault();
                    this.setInactive();
                },
                drop: (event) => {
                    event.preventDefault();
                    this.onDrop();
                }
            }
        }, [
            createElement('a', {
                attrs: {
                    name: dropZoneId,
                    href: '#' + dropZoneId
                }
            }, this.$slots.default({ dropZoneActive: this.active }))
        ]);
    },
};
</script>

<template>
    <div :data-active="active" @dragenter.prevent="setActive" @dragover.prevent="setActive" @dragleave.prevent="setInactive"
        @drop.prevent="onDrop">
        <slot :dropZoneActive="active"></slot>
    </div>
</template>