<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
import LogoItem from '@/components/nav/LogoItem.vue';
import { notify } from 'notiwind';
import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return {
            pageWidth: window.innerWidth,
            email: '',
            username: '',
            password: '',
            showPassword: false,
            errorMessages: {
                email: [],
                username: [],
                password: [],
                others: []
            }
        };
    },
    beforeMount() {
        document.title = 'SignUp - Kograph';
        if (this.$store.state.access != '') {
            this.$router.push('/');
        }
    },
    mounted() {
		window.addEventListener('resize', this.handleResize);
	},
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        async submitForm() {
            notify({
                group: 'foo',
                title: 'Signup',
                text: 'Trying to register... Please, wait.',
                type: 'info',
            }, 2000);
            try {
                const formData = {
                    email: this.email,
                    username: this.username,
                    password: this.password,
                };

                await axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/users/`, formData);
                
                Object.keys(this.errorMessages).forEach(key => {
                    this.errorMessages[key] = [];
                });

                notify({
                    group: 'foo',
                    title: 'Activate Account',
                    text: 'We have sent you an activation email. Click the link to activate your account',
                    type: 'info',
                }, -1);

                this.$router.push('/login');
                notify({
                    group: 'foo',
                    title: 'Success',
                    text: 'Successfully registered.',
                    type: 'success',
                }, 4000);
            } catch (error) {
                console.log(error)
                if (error.response.status === 429) {
                    notify({
                        group: "foo",
                        title: "Warning",
                        text: "Too many requests. Please, try again later.",
                        type: "warning"
                    }, 4000);
                    return;
                } else {
                    notify({
                        group: 'foo',
                        title: 'Error',
                        text: 'User registration failed.',
                        type: 'error',
                    }, 4000);
                    const newErrorMessages = {};
                    let allFieldsRequired = false;
                    if (Array.isArray(error.response.data)) {
                        Object.entries(error.response.data).forEach(([key, errorArray]) => {
                            newErrorMessages[key] = errorArray;
                        });
                        Object.keys(this.errorMessages).forEach(key => {
                            this.errorMessages[key] = [];
                        });
                        error.response.data.forEach((e) => {
                            if (e == 'Unable to create account.') e = 'Account with this email or username already exists.'
                            this.errorMessages["others"].push(e);
                        });
                    } else if (typeof error.response.data === 'object' && error.response.data !== null) {
                        Object.entries(error.response.data).forEach(([key, errorArray]) => {
                            newErrorMessages[key] = errorArray;
                            if (errorArray.includes('This field may not be blank.')) {
                                allFieldsRequired = true;
                                return;
                            }
                        });
                        if (!allFieldsRequired) {
                            Object.keys(this.errorMessages).forEach(key => {
                                if (newErrorMessages[key]) {
                                    this.errorMessages[key] = newErrorMessages[key];
                                } else {
                                    this.errorMessages[key] = [];
                                }
                            });
                        } else {
                            this.errorMessages["others"] = ["All fields are required."];
                        }
                    }
                }
            }
        },
        toggleShowPassword() {
            this.showPassword = !this.showPassword;
        },
        hideErrorMessages(key) {
            this.errorMessages[key] = [];
        },
        handleResize() {
            this.pageWidth = window.innerWidth;
        },
    },
    components: { ButtonItem, LogoItem }
}
</script>

<template>
    <div class="form_control">
        <LogoItem />
        <form @submit.prevent="submitForm">
            <div v-if="Object.values(errorMessages).some(errorArray => errorArray.length > 0) & errorMessages['others'].length == 0"
                class="error_container">
                <div v-if="errorMessages.email.length > 0" class="error_messages" :key="'email'">
                    <font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages('email')" />
                    <p v-for="errorMessage in errorMessages.email" :key="errorMessage">{{ errorMessage }}</p>
                </div>
                <div v-if="errorMessages.username.length > 0" class="error_messages" :key="'username'">
                    <font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages('username')" />
                    <p v-for="errorMessage in errorMessages.username" :key="errorMessage">{{ errorMessage }}</p>
                </div>
                <div v-if="errorMessages.password.length > 0" class="error_messages" :key="'password'">
                    <font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages('password')" />
                    <p v-for="errorMessage in errorMessages.password" :key="errorMessage">{{ errorMessage }}</p>
                </div>
            </div>
            <div v-if="errorMessages.others.length > 0" class="error_messages">
                <font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages('others')" />
                <p v-for="errorMessage in errorMessages.others" :key="errorMessage">{{ errorMessage }}</p>
            </div>
            <div class="form_input">
                <label for="email">Email address</label>
                <input v-model="email" id="email" type="email"/>
            </div>
            <div class="form_input">
                <label for="username">Username</label>
                <input v-model="username" id="username"/>
            </div>
            <div class="form_input">
                <div class="label_password">
                    <label for="password">Password</label>
                    <font-awesome-icon icon="eye" :class="!password ? 'password_hidden' : ''"
                        @click.prevent="toggleShowPassword" />
                </div>
                <input v-model="password" id="password" :type="showPassword ? 'text' : 'password'"/>
            </div>
            <p style="font-size: 14px" v-if="pageWidth <= 600">Have an account? <span style="cursor: pointer; color: #2f81f7" @click="this.$router.push('/login')">Log In</span></p>
            <ButtonItem v-if="pageWidth > 600" title="Log In" />
            <div class="buttons" v-if="pageWidth <= 600">
                <ButtonItem type="button" @click="this.$router.push('/')" title="Home" />
                <ButtonItem type="submit" title="Log In" />
            </div>
        </form>
    </div>
</template>

<style scoped>
.error_container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.error_messages {
    position: relative;
    padding: 15px 25.5px 15px 12px;
    border-radius: 5px;
    background-color: rgba(146, 44, 44, .2);
    border: 1px solid rgb(163, 0, 0);
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.error_messages p {
    line-height: 20px;
    color: white;
    font-size: 14px;
    user-select: text;
    cursor: unset;
}

.close-button {
    cursor: pointer;
    position: absolute;
    top: 8px;
    right: 8px;
}

.form_control {
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 50px;
}

.logo {
    cursor: default;
    width: 150px;
}

form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form_input {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

form>div>div {
    display: flex;
    justify-content: space-between;
}

form>div>div>p {
    cursor: pointer;
    color: #2f81f7;
    font-size: 14px;
}

.label_password {
    display: flex;
    align-items: center;
}

.label_password svg {
    cursor: pointer;
}

.password_hidden {
    visibility: hidden;
}

label {
    font-size: 14px;
}

.show_password {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
}

.buttons {
	display: flex;
	flex-direction: row;
	gap: 12px;
}

.buttons > * {
	flex: 1;
}

.buttons > button:nth-child(1) {
	background-color: #468b46 !important;
}
</style>