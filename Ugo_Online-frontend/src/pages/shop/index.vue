<template>
	<v-container>
		<v-alert type="info" variant="tonal" class="mb-4" v-if="user.role === 'SELLER'">
			<template #text>
				{{ user.shopId == null ? "作为卖家，您可以创建自己的店铺，为顾客提供优质的服务。但是您只能同时管理一个店铺。"
					:"您已经创建了店铺，请前往店铺管理页面进行管理。" }}
			</template>
			<template #append>
				<v-btn v-if="user.shopId == null" to="/shop/create" color="primary">创建店铺</v-btn>
				<v-btn v-else :to="`/shop/${user.shopId}`" color="primary">店铺管理</v-btn>
			</template>
		</v-alert>
		<v-row v-if="shops" lines="three">
			<v-col cols="12" md="4" class="text-center"  v-for="shop in shops.shops">
				<v-card
					:to="`/shop/${shop.id}`"
				>
					<v-card-title>
						<h2 class="headline mt-2">{{ shop.name }}</h2>
					</v-card-title>
					<v-rating
						readonly
						density="compact"
						half-increments
						active-color="amber"
						color="amber-darken-1"
						:model-value="shop.total_income"
					></v-rating>
					<v-card-text>
						<p class="mb-2 font-weight-bold">{{ `${shop.address}` }}</p>
						<p>{{ shop.description }}</p>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { getShops } from '@/api/shop';
import { user } from '@/store/user';

const shops = ref()

onMounted(async () => {
	const res = await getShops()
	shops.value = res
})

</script>