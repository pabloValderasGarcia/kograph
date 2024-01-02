<script>
import axios from 'axios';

export default {
	name: 'LogIn',
	data() {
		return {
			username: '',
			password: ''
		}
	},
	beforeMount() {
		document.title = 'LogIn - Kograph';
		if (this.$store.state.access !== '') {
			this.$router.push('/');
		}
	},
	methods: {
		submitForm() {
			this.$store.commit('removeAccess')

			const formData = {
				username: this.username,
				password: this.password,
			};

			axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/jwt/create/`, formData).then(response => {
				console.log(response);

				const access = response.data.access;
				const refresh = response.data.refresh;

				this.$store.commit('setAccess', access);
				this.$store.commit('setRefresh', refresh);

				this.$nextTick(() => {
					this.$router.push('/');
				});
			}).catch(error => {
				console.log(error);
			})
		}
	}
}
</script>

<template>
	<form @submit.prevent="submitForm">
		<input v-model="username" placeholder="Username" pattern="[a-zA-Z0-9_\.\-]{1,20}" @invalid="handleInvalidField"
			required />
		<!-- <input v-model="password" type="password" placeholder="Password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" @invalid="handleInvalidField" required /> -->
		<input v-model="password" type="password" placeholder="Password" required />
		<button type="submit">LOGIN</button>
	</form>
	<button @click="this.$router.push('/signup')">NOT LOGGED? REGISTER</button>
</template>