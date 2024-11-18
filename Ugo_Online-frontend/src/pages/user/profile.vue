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
		
		<v-card v-if="shopInfo" class="mt-4" :to="`/shop/${shopInfo.id}`">
			<template #title>
				<h2 class="headline mb-1">{{ shopInfo.name }}</h2>
			</template>
			<template #subtitle>
				<p class="mb-2 font-weight-bold">{{ `地址：${shopInfo.address}` }}</p>
				<p>{{ shopInfo.description }}</p>
			</template>
			<template #append>
				<v-chip color="green" prepend-icon="mdi-store">我的商铺</v-chip>
			</template>
		</v-card>
	</v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { user } from '@/store/user';
import { logout } from '@/api/user';
import { getShopInfo } from '@/api/shop';

const shopInfo = ref(null)
const loading = ref(false);

const submitLogout = async () => {
	loading.value = true;
	await logout();
	loading.value = false;
};

onMounted(async () => {
	if (user.shopId) {
		shopInfo.value = await getShopInfo(user.shopId);
	}
})

</script>