<template>
	<v-container>
		<v-alert type="info" variant="tonal" class="mb-4" v-if="user.role === 'SELLER'">
			<template #text>
				作为卖家，您可以创建自己的店铺或加入店铺，为顾客提供优质的服务。
			</template>
			<template #append>
				<v-btn to="/shop/create" color="primary">创建/加入店铺</v-btn>
			</template>
		</v-alert>
		<v-row v-if="shops" lines="three">
			<v-col cols="12" md="4" class="text-center"  v-for="shop in shops.shops">
				<v-card
					:to="`/shop/${shop.id}`"
					style="height: 100%;"
					elevation="2"
				>
					<v-card-text>
						<p class="headline mt-2 font-weight-bold text-h5">{{ shop.name }}</p>
						<v-chip
							v-if="user.shops.includes(shop.id)"
							class="mt-2"
							prepend-icon="mdi-store"
							color="success"
							text="我的商铺"
						></v-chip>
					</v-card-text>
					<v-rating
						readonly
						density="compact"
						half-increments
						active-color="amber"
						color="amber-darken-1"
						:model-value="shop.average_rating"
					></v-rating>
					<v-card-text>
						<p class="mb-2 font-weight-bold">{{ `${shop.address}` }}</p>
						<p>{{ shop.description }}</p>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
		<v-pagination
			class="mt-4"
			v-if="shops"
			v-model="page"
			:length="shops.total_page"
		></v-pagination>
	</v-container>
</template>
<script setup>
import { onMounted, ref, watch } from 'vue'
import { getShops } from '@/api/shop';
import { user } from '@/store/user';

const shops = ref()
const page = ref(1)

onMounted(async () => {
	const res = await getShops(1)
	shops.value = res
})

watch(page, async (newPage) => {
	const res = await getShops(newPage)
	shops.value = res
})

</script>