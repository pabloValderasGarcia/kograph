<script setup>
import '@/assets/css/main.css';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();
const username = ref('');
const password = ref('');

onMounted(() => {
	if (localStorage.getItem('token')) {
		router.push('/');
	}
});

const login = async () => {
	try {
		const response = await axios.post(`${process.env.VUE_APP_SERVER_URL}/api-token-auth/`, {
			username: username.value,
			password: password.value
		});
		
		if (response.data.status === 'OK') {
			const token = response.data.token;
			localStorage.setItem('token', token);
			store.commit('login', response.data.user);
			router.push('/');
		} else {
			console.error('Error trying to login:', response.data.message);
		}
	} catch (error) {
		console.error('Error trying to login:', error);
	}
}

const handleInvalidField = (event) => {
	event.preventDefault();
};
</script>

<template>
	<form @submit.prevent="login">
		<input v-model="username" placeholder="Username" pattern="[a-zA-Z0-9_\.\-]{1,20}" @invalid="handleInvalidField"
			required />
		<!-- <input v-model="password" type="password" placeholder="Password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" @invalid="handleInvalidField" required /> -->
		<input v-model="password" type="password" placeholder="Password" required />
		<button type="submit">LOGIN</button>
	</form>
	<button @click="router.push('/register')">NOT LOGGED? REGISTER</button>
</template>