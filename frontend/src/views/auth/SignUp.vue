<script>
import axios from 'axios'

export default {
	name: 'SignUp',
	data() {
		return {
			email: '',
			username: '',
			password: '',
			showPassword: false
		}
	},
	beforeMount() {
		document.title = 'SignUp - Kograph';
		if (this.$store.state.access != '') {
			this.$router.push('/')
		}
	},
	methods: {
		submitForm() {
			const formData = {
				email: this.email,
				username: this.username,
				password: this.password,
			};

			axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/users/`, formData).then(response => {
				console.log(response)
				this.$router.push('/login')
			}).catch(error => {
				console.log(error)
			})
		},
		toggleShowPassword() {
			this.showPassword = !this.showPassword;
		}
	}
}
</script>

<template>
	<form @submit.prevent="submitForm">
		<input v-model="email" type="email" placeholder="Email" required />
		<input v-model="username" placeholder="Username" pattern="[a-zA-Z0-9_\.\-]{1,20}" required />
		<input v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="Password" required />
		<button @click.prevent="toggleShowPassword">
			{{ showPassword ? 'Hide' : 'Show' }} password
		</button>
		<button type="submit">REGISTER</button>
	</form>
	<button @click="this.$router.push('/login')">HAVE AN ACCOUNT? LOGIN</button>
</template>