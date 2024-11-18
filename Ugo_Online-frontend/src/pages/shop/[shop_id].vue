<template>
	<v-container>
		<v-skeleton-loader v-if="!shopInfo" type="image, article" />
		<div v-else>
				<v-card>
					<template #title>
						<h2 class="headline mb-1">{{ shopInfo.name }}</h2>
					</template>
					<template #subtitle>
						<p class="mb-2 font-weight-bold">{{ `地址：${shopInfo.address}` }}</p>
						<p>{{ shopInfo.description }}</p>
					</template>
					<template #append>
					</template>
				</v-card>
		</div>
	</v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getShopInfo } from '@/api/shop';

const route = useRoute()
const { shop_id } = route.params

const shopInfo = ref(null)

onMounted( async () => {
	shopInfo.value = await getShopInfo(shop_id)
})

</script>