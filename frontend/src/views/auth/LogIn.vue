<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
import LogoItem from '@/components/nav/LogoItem.vue';
import '@/assets/css/components/input.css';
import { notify } from 'notiwind';
import axios from 'axios';
import qs from 'qs';

export default {
	name: 'LogIn',
	data() {
		return {
			pageWidth: window.innerWidth,
			username: '',
			password: '',
			showPassword: false,
			errorMessage: ''
		};
	},
	beforeMount() {
		document.title = 'LogIn - Kograph';
		if (this.$store.state.access !== '') {
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
		submitForm() {
			this.$store.commit('removeAccess');

			const formData = {
				email: this.username,
				username: this.username,
				password: this.password
			};

			const serializedData = qs.stringify(formData);

			axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/create/`, serializedData).then(response => {
				const access = response.data.access;
				const refresh = response.data.refresh;
				this.$store.commit('setAccess', access);
				this.$store.commit('setRefresh', refresh);
				this.$nextTick(() => {
					this.$router.push('/');
				});
				notify({
					group: "foo",
					title: "Success",
					text: "Successfully logged.",
					type: "success"
				}, 4000);
			}).catch((error) => {
				if (error.response.status === 429) {
						notify({
						group: "foo",
						title: "Warning",
						text: "Too many requests. Please, try again later.",
						type: "warning"
					}, 4000);
					return;
				} else {
					if (error.response.data['detail']) {
						this.errorMessage = error.response.data['detail'];
						return;
					}
					if (this.username != '' & this.password != '') this.errorMessage = "Account doesn't exist with these credentials.";
					else this.errorMessage = "All fields are required.";
				}
			});
		},
		toggleShowPassword() {
			this.showPassword = !this.showPassword;
		},
		hideErrorMessage() {
            this.errorMessage = '';
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
			<div v-if="errorMessage" class="error_message">
				<font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessage()" />
				<p>{{ errorMessage }}</p>
			</div>
			<div>
				<label for="username">Username or email address</label>
				<input v-model="username" id="username" name="username" autocomplete="username"/>
			</div>
			<!-- <input v-model="password" type="password" placeholder="Password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" @invalid="handleInvalidField" required /> -->
			<div>
				<div>
					<div class="label_password">
						<label for="password">Password</label>
						<font-awesome-icon v-if="password" icon="eye" @click.prevent="toggleShowPassword" />
					</div>
					<p @click="this.$router.push('/recovery')">Forgot password?</p>
				</div>
				<input v-model="password" id="password" :type="showPassword ? 'text' : 'password'" />
			</div>
			<p style="font-size: 14px" v-if="pageWidth <= 600">Don't have an account? <span style="cursor: pointer; color: #2f81f7" @click="this.$router.push('/signup')">Sign up</span></p>
			<ButtonItem v-if="pageWidth > 600" title="Log In" />
			<div class="buttons" v-if="pageWidth <= 600">
				<ButtonItem type="button" @click="this.$router.push('/')" title="Home" />
				<ButtonItem type="submit" title="Log In" />
			</div>
		</form>
	</div>
</template>

<style scoped>
.error_message {
	position: relative;
	padding: 15px 25.5px 15px 12px;
	border-radius: 5px;
	background-color: rgba(146, 44, 44, .8);
	border: 1px solid rgb(163, 0, 0);
	display: flex;
	flex-direction: column;
	gap: 5px;
}

body.dark-mode .error_message {
	background-color: rgba(146, 44, 44, .2) !important;
}

.error_message p {
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
	color: white !important;
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

form>div {
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
	font-size: 14px;
	display: flex;
	align-items: center;
	gap: 8px;
}

.label_password svg {
	cursor: pointer;
}

label {
	font-size: 14px;
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