<script>
import ButtonItem from '@/components/others/ButtonItem.vue';
export default {
	name: 'NotFoundView',
	beforeCreate() {
		document.title = 'Not Found - Kograph';
	},
	components: { ButtonItem }
}
</script>

<template>
	<div class="notFound">
		<img class="gif" src="@/assets/svg/errors/notFound.svg"/>
		<p>NOT FOUND</p>
		<div>
			<ButtonItem @click="this.$router.push('/');" title='Home' />
			<ButtonItem @click="this.$router.back();" title='Go Back' />
		</div>
	</div>
</template>

<style scoped>
.notFound {
	padding: 50px;
	height: 100vh;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	gap: 30px;
}

img {
	width: 600px;
}

.notFound p {
	font-weight: bold;
}

.notFound div {
	display: flex;
	gap: 12px;
}

.notFound button:first-child {
	background-color: rgb(79, 152, 79) !important;
}

.notFound button:first-child:hover {
	background-color: rgb(70, 139, 70) !important;
}
</style>