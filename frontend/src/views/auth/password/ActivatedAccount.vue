<script>
import '@/assets/css/components/input.css';
import { notify } from 'notiwind';
import axios from 'axios';

export default {
	name: 'ActivatedAccount',
	data() {
		return {
			activated: false
		}
	},
	beforeCreate() {
		document.title = 'Activated Account - Kograph';
	},
	created() {
		this.activateAccount();
		const { uid, token } = this.$route.params;

		axios.get(`${process.env.VUE_APP_SERVER_URL}/validate_link/?uid=${uid}&token=${token}`).then(() => {
			notify({
				group: 'foo',
				title: 'Success',
				text: 'Account successfully activated. Log in has been allowed.',
				type: 'success',
			}, -1);
		}).catch(() => {
			notify({
				group: 'foo',
				title: 'Error',
				text: 'Invalid or expired activation link.',
				type: 'error',
			}, 5000);
		});
		this.$router.push('/login');
	},
	methods: {
		async activateAccount() {
			try {
				const { uid, token } = this.$route.params;
				await axios.post(`${process.env.VUE_APP_SERVER_URL}/auth/users/activation/`, { uid: uid, token: token });
			} catch (error) {
				// console.log(error);
			}
		},
	}
}
</script>