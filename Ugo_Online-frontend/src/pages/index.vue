<template>
	<v-container>
		<v-infinite-scroll :items="items" :onLoad="fetchProducts">
			<template v-for="(item, index) in items" :key="item.id">
				<v-row v-if="index % 3 === 0" style="width: 100%;">
					<v-col cols="4">
						<product-card
							:product="item" 
							:shop-id="item.shop"
							:remove-product-callback="null"
						></product-card>
					</v-col>
					<v-col cols="4">
						<product-card
							v-if="index + 1 < items.length"
							:product="items[index + 1]" 
							:shop-id="items[index + 1].shop"
							:remove-product-callback="null"
						></product-card>
					</v-col>
					<v-col cols="4">
						<product-card
							v-if="index + 2 < items.length"
							:product="items[index + 2]" 
							:shop-id="items[index + 2].shop"
							:remove-product-callback="null"
						></product-card>
					</v-col>
				</v-row>
			</template>
		</v-infinite-scroll>
	</v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getAllProductList, getCategories } from '@/api/product';
import ProductCard from '@/components/ProductCard';

const latestProductList = ref(null)
const categoryList = ref(null)
const items = ref([])

const fetchProducts = async ({ done }) => {
	let page = 1;
	if (latestProductList.value) {
		if (latestProductList.value.next === null) {
			done('empty')
			return
		}
		page = latestProductList.value.cur_page + 1
	}
	const res = await getAllProductList({ page })
	latestProductList.value = res
	items.value.push(...res.products)
	console.log(items.value)

	done('ok')
}

onMounted(async () => {
	categoryList.value = await getCategories()
})


</script>