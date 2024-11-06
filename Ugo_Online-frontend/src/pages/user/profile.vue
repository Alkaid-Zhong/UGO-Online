<template>
	<v-container>
		<v-card>
			<template #prepend>
				<v-chip
					class="mr-2"
					:color="user.role === 'CUSTOMER' ? 'green' : 'blue'"
					:text="user.role === 'CUSTOMER' ? '顾客' : '商家'"
				></v-chip>
			</template>
			<template #append>
				<v-btn
					prepend-icon="mdi-logout"
					@click="submitLogout"
					variant="text"
					color="red"
					:loading="loading"
				>注销</v-btn>
			</template>
			<template #title>
				{{ user.name }}
			</template>
			<template #subtitle>
				{{  user.email }}
			</template>
		</v-card>
	</v-container>
</template>
<script setup>
import { ref } from 'vue';
import { user } from '@/store/user';
import { logout } from '@/api/user';

const loading = ref(false);

const submitLogout = async () => {
	loading.value = true;
	await logout();
	loading.value = false;
};


</script>