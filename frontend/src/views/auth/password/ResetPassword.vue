<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
import '@/assets/css/components/input.css';
import { notify } from 'notiwind';
import axios from 'axios';
import LogoItem from '@/components/nav/LogoItem.vue';

export default {
	name: 'ResetPassword',
	data() {
		return {
			password: '',
			confirmPassword: '',
			showPassword: false,
			showConfirmPassword: false,
			errorMessages: []
		};
	},
	beforeCreate() {
		document.title = 'Reset Password - Kograph';
	},
	created() {
		const { uid, token } = this.$route.params;

		axios.get(`${process.env.VUE_APP_SERVER_URL}/validate_link/?uid=${uid}&token=${token}`) .then(() => { })
			.catch(() => {
				notify({
					group: 'foo',
					title: 'Error',
					text: 'Invalid or expired reset link.',
					type: 'error',
				});
				this.$router.push('/login');
			});
	},
	methods: {
		resetPassword() {
			if (!this.confirmPassword) {
				this.errorMessages = ['All fields are required.'];
				return;
			}
			if (this.password !== this.confirmPassword) {
				this.errorMessages = ['Passwords do not match.'];
				return;
			}

			const { uid, token } = this.$route.params;

			axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/users/reset_password_confirm/`, {
				uid: uid,
				token: token,
				new_password: this.password,
				re_new_password: this.confirmPassword
			})
				.then(() => {
					this.errorMessages = [];
					notify({
						group: "foo",
						title: "Success",
						text: "Password reset successfully.",
						type: "success"
					}, 4000);
					this.$router.push('/login');
				})
				.catch((error) => {
					if (error.response.status === 429) {
						notify({
							group: "foo",
							title: "Warning",
							text: "Too many requests. Please, try again later.",
							type: "warning"
						}, 4000);
					} else {
						this.errorMessages = [];
						console.log(error.response)
						if (error.response.data.detail) {
							error.response.data.detail.forEach((e) => {
								this.errorMessages.push(e);
							});
						} else if (error.response.data.new_password) {
							error.response.data.new_password.forEach((e) => {
								if (e == 'This field may not be blank.') {
									this.errorMessages.push('All fields are required.');
									return;
								}
								this.errorMessages.push(e);
							});
						} else if (error.response.data.re_new_password) {
							error.response.data.re_new_password.forEach((e) => {
								if (e == 'This field may not be blank.') {
									this.errorMessages.push('All fields are required.');
									return;
								}
								this.errorMessages.push(e);
							});
						}
					}
				});
		},
		toggleShowPassword() {
			this.showPassword = !this.showPassword;
		},
		toggleShowConfirmPassword() {
			this.showConfirmPassword = !this.showConfirmPassword;
		},
		hideErrorMessages() {
			this.errorMessages = [];
		}
	},
	components: { ButtonItem, LogoItem }
}
</script>

<template>
	<form @submit.prevent="resetPassword">
		<LogoItem />
		<p>Reset Password</p>
		<div v-if="errorMessages.length > 0" class="error_messages">
			<font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages" />
			<p v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</p>
		</div>
		<div class="form_input">
			<div class="label_password">
				<label for="password">Password</label>
				<font-awesome-icon v-if="password" icon="eye" @click.prevent="toggleShowPassword" />
			</div>
			<input v-model="password" :type="showPassword ? 'text' : 'password'" id="password" name="password" />
		</div>
		<div class="form_input">
			<div class="label_password">
				<label for="confirmPassword">Confirm password</label>
				<font-awesome-icon v-if="confirmPassword" icon="eye" @click.prevent="toggleShowConfirmPassword" />
			</div>
			<input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword" name="confirmPassword" />
		</div>
		<div class="recovery_buttons">
			<ButtonItem type="button" @click="this.$router.push('/login')" title='Cancel' />
			<ButtonItem type="submit" title='Reset' />
		</div>
	</form>
</template>

<style scoped>
.logo {
	cursor: default;
	width: 150px;
	margin: 0 auto 50px auto;
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

.form_input {
	width: 100%;
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.form_input label {
	font-size: 14px;
}

form {
	width: 600px;
	padding: 50px;
	height: 100vh;
	display: flex;
	flex-direction: column;
	justify-content: center;
	margin: 0 auto;
}

form > *:not(:first-child, :last-child) {
	margin-bottom: 20px;
}

img {
	width: 600px;
}

form>p {
	font-size: 26px;
	font-weight: bold;
}

.recovery_buttons {
	width: 100%;
	display: flex;
	gap: 12px;
}

.recovery_buttons button {
	flex: 1;
}

.recovery_buttons button:last-child {
	background-color: rgb(79, 152, 79) !important;
}

.recovery_buttons button:last-child:hover {
	background-color: rgb(70, 139, 70) !important;
}

.label_password {
	font-size: 14px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.label_password svg {
	cursor: pointer;
}

@media screen and (max-width: 1000px) {
	form {
		width: 100%;
	}
}
</style>