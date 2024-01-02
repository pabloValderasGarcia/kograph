<script>
export default {
    name: 'UserItem',
    data() {
        return {
            state: false,
            darkMode: false
        }
    },
    methods: {
        logout() {
            this.$store.commit('removeAccess');
            this.$nextTick(() => {
                this.$router.push('/');
            });
        },
        toggleDropdown() {
            this.state = !this.state;
        },
        close(e) {
            if (!this.$el.contains(e.target)) {
                this.state = false;
            }
        },
        dark() {
            document.querySelector('body').classList.add('dark-mode')
            this.darkMode = true
            this.$emit('dark')
        },
        light() {
            document.querySelector('body').classList.remove('dark-mode')
            this.darkMode = false
            this.$emit('light')
        },
        modeToggle() {
            if (this.darkMode || document.querySelector('body').classList.contains('dark-mode')) {
                this.light()
            } else {
                this.dark()
            }
        },
    },
    computed: {
        darkDark() {
            return this.darkMode && 'darkmode-toggled'
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
    <div class="user">
        <div class="picture" @click.prevent="toggleDropdown"></div>
        <div class="dropdown" v-if="state">
            <div class="user_info">
                <div class="user_data">
                    <div class="picture picture_dropdown"></div>
                    <div v-if="this.$store.state.user">
                        <p>{{ this.$store.state.user.username }}</p>
                        <div class="user_email">
                            <p>{{ this.$store.state.user.email.split('@')[0] }}</p>
                            <p>@{{ this.$store.state.user.email.split('@')[1] }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="dropdown_buttons">
                <p @click="this.$router.push('/account')">My Account</p>
                <p @click="modeToggle">Dark Mode
                    <span class="mode-toggle" :class="darkDark">
                        <div class="toggle">
                            <div id="dark-mode" type="checkbox"></div>
                        </div>
                    </span>
                </p>
                <p @click="logout">Logout<font-awesome-icon icon="right-from-bracket" /></p>
            </div>
            <div class="dropdown_policy">
                <p>Privacy Policy</p>
                <p>Terms of Service</p>
            </div>
        </div>
    </div>
</template>

<style>
.user {
    position: relative;
}

.picture {
    cursor: pointer;
    width: 38px;
    aspect-ratio: 1/1;
    border-radius: 50%;
    background-color: #D06C6C;
}

.dropdown {
    position: absolute;
    right: -15px;
    top: 53px;
    min-width: 450px;
    height: auto;
    display: flex;
    flex-direction: column;
    padding-top: 20px;
    background-color: #ececec;
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    border-bottom-right-radius: 20px;
}

body.dark-mode .dropdown {
    background-color: #373737;
}

.dropdown>div:not(:last-child) {
    padding-left: 25px;
    padding-right: 25px;
}

.dropdown_buttons {
    padding-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.dropdown_buttons p {
    user-select: none;
    cursor: pointer;
    width: fit-content;
    display: flex;
    align-items: center;
    gap: 12px;
}

.dropdown_buttons p:hover {
    font-weight: bold;
}

.picture_dropdown {
    width: 70px !important;
    cursor: default !important;
}

.user_info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding-bottom: 20px;
    border-bottom: 3px solid white;
}

body.dark-mode .user_info {
    border-bottom: 3px solid #484848 !important;
}

.user_data {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
}

.user_data>div:last-child {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.user_data p:first-child {
    font-weight: bold;
}

.user_email {
    display: flex;
}

.user_email p {
    font-weight: 400 !important;
    opacity: .8 !important;
}

.user_email p:first-child {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 400px;
}

.dark-mode {
    background-color: #242424;
    color: #fff;
}

.mode-toggle {
    position: relative;
    padding: 0;
    width: 44px;
    height: 24px;
    min-width: 36px;
    min-height: 20px;
    background-color: #262626;
    border: 0;
    border-radius: 24px;
    outline: 0;
    overflow: hidden;
    cursor: pointer;
    z-index: 2;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    -webkit-touch-callout: none;
    appearance: none;
    transition: background-color 0.5s ease;
}

.mode-toggle .toggle {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    margin: auto;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 3px solid transparent;
    box-shadow: inset 0 0 0 2px #ffffff;
    overflow: hidden;
    transition: transform 0.5s ease;
}

.mode-toggle .toggle #dark-mode {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    border-radius: 50%;
}

.mode-toggle .toggle #dark-mode:before {
    content: "";
    position: relative;
    width: 100%;
    height: 100%;
    left: 50%;
    float: left;
    background-color: #ffffff;
    transition: border-radius 0.5s ease, width 0.5s ease, height 0.5s ease, left 0.5s ease, transform 0.5s ease;
}

.dark-mode .mode-toggle {
    background-color: #4b4b4b;
}

.dark-mode .mode-toggle .toggle {
    transform: translateX(19px);
}

.dark-mode .mode-toggle .toggle #dark-mode:before {
    border-radius: 50%;
    width: 150%;
    height: 85%;
    left: 40%;
    transform: translate(-10%, -40%), rotate(-35deg);
}

.dropdown_policy {
    padding-top: 20px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2px;
}

.dropdown_policy p {
    user-select: none;
    cursor: pointer;
    padding: 15px;
    flex: 2;
    text-align: center;
}

.dropdown_policy p:first-child {
    border-bottom-left-radius: 20px;
}

.dropdown_policy p:last-child {
    border-bottom-right-radius: 20px;
}

.dropdown_policy p {
    background-color: #dddddd;
}

.dropdown_policy p:hover {
    background-color: #d1d1d1;
}

body.dark-mode .dropdown_policy p {
    background-color: #3f3f3f !important;
}

body.dark-mode .dropdown_policy p:hover {
    background-color: #484848 !important;
}
</style>