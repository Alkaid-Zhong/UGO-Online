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
			<v-divider></v-divider>
			<v-card-item class="text-center">
				<v-row>
					<v-col cols="12" md="6">
						<v-icon>mdi-phone</v-icon>
						<p class="mt-2">{{ user.phone }}</p>
					</v-col>
					<v-divider vertical></v-divider>
					<v-col cols="12" md="6">
						<v-icon>mdi-wallet</v-icon>
						<div class="mt-2">
							<span style="font-size: 12px;">￥</span>
							<span>{{ user.money }}</span>
						</div>
						<v-btn 
								class="font-weight-bold ml-1 mb-1" 
								color="primary"
								@click="showRecharge = true"
								variant="text"
								size="small"
							>充值</v-btn>
					</v-col>
				</v-row>
			</v-card-item>
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
	<v-dialog v-model="showRecharge" max-width="500px">
		<v-card>
			<v-toolbar>
				<v-btn icon="mdi-close" @click="showRecharge = false"></v-btn>
				<v-toolbar-title>充值</v-toolbar-title>
			</v-toolbar>
			<v-card-item>
				<v-text-field
					label="充值金额（元）"
					type="number"
					v-model="rechargeMoney"
				></v-text-field>
				<v-btn color="primary" @click="recharge" variant="contained" :loading="loading">充值</v-btn>
			</v-card-item>
		</v-card>
	</v-dialog>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { user } from '@/store/user';
import { addMoney, logout } from '@/api/user';
import { getShopInfo } from '@/api/shop';

const shopInfo = ref(null)
const loading = ref(false);
const showRecharge = ref(false);
const rechargeMoney = ref(0);

const submitLogout = async () => {
	loading.value = true;
	await logout();
	loading.value = false;
};

const recharge = async () => {
	loading.value = true;
	const res = await addMoney(rechargeMoney.value);
	loading.value = false;
}

onMounted(async () => {
	if (user.shopId) {
		shopInfo.value = await getShopInfo(user.shopId);
	}
})

</script>