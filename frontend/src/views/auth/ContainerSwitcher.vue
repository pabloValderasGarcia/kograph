<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
import LogIn from './LogIn.vue';
import SignUp from './SignUp.vue';

export default {
    name: 'ContainerSwitcher',
    data() {
        return {
            isLogIn: this.$route.path === '/login',
            currentComponentKey: 1,
        };
    },
    computed: {
        currentComponent() {
            return this.isLogIn ? 'LogIn' : 'SignUp';
        },
    },
    watch: {
        $route(to) {
            this.isLogIn = to.path === '/login';
            this.currentComponentKey = this.currentComponentKey === 1 ? 2 : 1;
        },
    },
    methods: {
        handleSwitchContainer() {
            this.isLogIn = !this.isLogIn;
            this.currentComponentKey = this.currentComponentKey === 1 ? 2 : 1;
            this.$router.push(this.isLogIn ? '/login' : '/signup');
        },
    },
    components: { LogIn, SignUp, ButtonItem }
}
</script>

<template>
    <div class="container_switcher" :class="isLogIn ? '' : 'container_signup'">
        <div class="formside" :class="isLogIn ? '' : 'formside_signup'">
            <transition name="fade" mode="out-in">
                <component :is="currentComponent" :key="currentComponentKey" />
            </transition>
        </div>
        <div class="otherside" :class="isLogIn ? '' : 'otherside_signup'">
            <img class="svg" src="@/assets/svg/login/login.svg" />
            <section>
                <p>{{ isLogIn ? 'It\'s Never Too Late' : 'Welcome to Kograph' }}</p>
                <div>
                    <ButtonItem @click="this.$router.push('/')" title='Home' />
                    <ButtonItem @click="handleSwitchContainer" :title="isLogIn ? 'Sign Up' : 'Log In'" />
                </div>
            </section>
        </div>
    </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: all 0.2s ease-in-out;
}

.container_switcher {
    display: flex;
    user-select: none;
    overflow: hidden;
}

.formside {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 70%;
    transition-property: transform;
    transition-duration: 500ms;
    transition-timing-function: ease-in-out;
}

.otherside {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 50%;
    transition-property: transform;
    transition-duration: 500ms;
    transition-timing-function: ease-in-out;
    background-color: rgb(187, 229, 255);
}

.otherside section {
    transform: translateY(-40px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 25px;
}

.otherside div {
    display: flex;
    gap: 12px;
}

.otherside p {
    font-size: 25px;
    font-weight: bold;
}

.otherside .svg {
    transform: translateY(-25px) !important;
    width: 350px !important;
    height: fit-content !important;
}

.otherside button:first-child {
    background-color: rgb(79, 152, 79) !important;
}

.otherside button:first-child:hover {
    background-color: rgb(70, 139, 70) !important;
}

body.dark-mode .otherside {
    background-color: #318ba7;
}

@media screen and (max-width: 768px) {
    .otherside {
        flex: .5;
    }
}

@media screen and (min-width: 768px) {
    .formside {
        height: 100svb;
    }

    .otherside {
        height: 100svb;
    }
}

@media screen and (min-width: 1190px) {
    .formside {
        transform: translateX(0);
        left: 0;
    }

    .formside_signup {
        transform: translateX(100%);
        left: 0;
    }

    .otherside {
        transform: translateX(0);
        left: 0;
    }

    .otherside_signup {
        transform: translateX(-100%);
        left: 0;
    }
}

@media screen and (max-width: 1190px) {
    .container_switcher {
        flex-direction: column-reverse;
        justify-content: center;
        align-items: center;
        height: 100svb;
    }

    .formside {
        flex: 1;
        width: 100%;
    }

    .otherside {
        display: none;
    }

    .form_control {
        width: 80%;
    }
}

@media screen and (max-width: 600px) {
    .formside {
        width: 110%;
    }
}</style>