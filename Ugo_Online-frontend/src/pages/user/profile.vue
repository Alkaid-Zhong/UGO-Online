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
					prepend-icon="mdi-lock-open-outline"
					@click="showChangePassword = true"
					variant="text"
					color="primary"
					:loading="loading"
				>修改密码</v-btn>
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
					<v-col cols="6">
						<v-icon>mdi-phone</v-icon>
						<p class="mt-2">{{ user.phone }}</p>
					</v-col>
					<v-divider vertical></v-divider>
					<v-col cols="6">
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
								v-if="user.role === 'CUSTOMER'"
							>充值</v-btn>
					</v-col>
				</v-row>
			</v-card-item>
		</v-card>
		
		<v-card v-for="shopInfo in shopInfo" class="mt-4" :to="`/shop/${shopInfo.id}`">
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

		<AddressSelect v-if="user.role==='CUSTOMER'" class="mt-5"
			:title=" '我的地址'"
			:addressPerPage="3"
			:paying="false"
			:preSelect="false"
		></AddressSelect>
		<!-- <v-card v-if="user.role==='CUSTOMER'" class="mt-4">
			<v-card-title class="text-h5 font-weight-bold">
				我的地址
			</v-card-title>
			
		</v-card> -->
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

	<v-dialog v-model="showChangePassword" max-width="500px">
		<v-card>
			<v-toolbar>
				<v-btn icon="mdi-close" @click="showChangePassword = false"></v-btn>
				<v-toolbar-title>修改密码</v-toolbar-title>
			</v-toolbar>
			<v-card-item>
				<v-text-field
					label="旧密码"
					type="password"
					v-model="oldPassword"
				></v-text-field>
				<v-text-field
					label="新密码"
					type="password"
					v-model="newPassword"
				></v-text-field>
				<v-text-field
					label="确认密码"
					type="password"
					v-model="confirmPassword"
				></v-text-field>
				<v-btn color="primary" @click="onclickSubmitChangePassword" variant="contained" :loading="loading">修改密码</v-btn>
			</v-card-item>
		</v-card>
	</v-dialog>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { user } from '@/store/user';
import { addMoney, changePassword, logout, profile } from '@/api/user';
import { getShopInfo } from '@/api/shop';
import AddressSelect from '@/components/addressSelect.vue';
import snackbar from '@/api/snackbar';

const shopInfo = ref([])
const loading = ref(false);
const showRecharge = ref(false);
const rechargeMoney = ref(0);
const showChangePassword = ref(false);

const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const onclickSubmitChangePassword = async () => {
	if (newPassword.value !== confirmPassword.value) {
		snackbar.error('两次输入的密码不一致');
		return;
	}
	loading.value = true;
	let res = await changePassword(oldPassword.value, newPassword.value);
	console.log(res);
	if (res.success) {
		showChangePassword.value = false;
		snackbar.success('修改密码成功');
	} else {
		snackbar.error('修改密码失败: ' + res.response.data.message);
	}
	loading.value = false;
};

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
	await profile();
	if (!(user.shops.length === 0)) {
		Promise.all(user.shops.map(async (shopId) => {
			const shop = await getShopInfo(shopId);
			shopInfo.value.push(shop);
		}));
	}
})

</script>