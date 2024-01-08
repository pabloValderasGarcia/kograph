<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
import '@/assets/css/components/input.css';
import { notify } from 'notiwind';
import axios from 'axios';
import LogoItem from '@/components/nav/LogoItem.vue';

export default {
	name: 'RecoveryPassword',
	data() {
		return {
			email: '',
			errorMessages: []
		};
	},
	beforeCreate() {
		document.title = 'Recovery Password - Kograph';
	},
	methods: {
		recoveryPassword() {
			notify({
				group: 'foo',
				title: 'Reset',
				text: 'Trying to send email...',
				type: 'info',
			}, 2000);
			axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/users/reset_password/`, { email: this.email }).then(() => {
				this.errorMessages = [];

				// Check if email exists
				axios.get(`${process.env.VUE_APP_SERVER_URL}/auth/users/check_email/?email=${this.email}`).then((response) => {
					notify({
						group: "foo",
						title: response.data ? "Success" : "Warning",
						text: response.data ? "An email has been sent to your inbox." : "Email doesn't registered.",
						type: response.data ? "success" : "warning"
					}, 4000);
				}).catch(() => { });
			}).catch((error) => {
				if (error.response.status === 429) {
					if (error.response.data.detail == "Please, wait approximately 5 minutes from your last request.") {
						notify({
							group: "foo",
							title: "Warning",
							text: "Please, wait approximately 5 minutes from your last request.",
							type: "warning"
						}, 4000);
					} else {
						notify({
							group: "foo",
							title: "Warning",
							text: "Too many requests. Please, try again later.",
							type: "warning"
						}, 4000);
					}
				} else {
					this.errorMessages = [];
					if (error.response.data.email) {
						error.response.data.email.forEach((e) => {
							this.errorMessages.push(e);
						});
					}
				}
			});
		},
		hideErrorMessages() {
			this.errorMessages = [];
		}
	},
	components: { ButtonItem, LogoItem }
}
</script>

<template>
	<form @submit.prevent="recoveryPassword">
		<LogoItem />
		<p>Recovery Password</p>
		<div v-if="errorMessages.length > 0" class="error_messages">
			<font-awesome-icon icon="xmark" class="close-button" @click="hideErrorMessages" />
			<p v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</p>
		</div>
		<div class="form_input">
			<label for="email">Email address</label>
			<input v-model="email" id="email" name="email" />
		</div>
		<div class="recovery_buttons">
			<ButtonItem type="button" @click="this.$router.push('/login');" title='Cancel' />
			<ButtonItem type="submit" title='Send Email' />
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
	height: 100svb;
	display: flex;
	flex-direction: column;
	justify-content: center;
	margin: 0 auto;
}

form>*:not(:first-child, :last-child) {
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

@media screen and (max-width: 1000px) {
	form {
		width: 100%;
	}
}
</style>