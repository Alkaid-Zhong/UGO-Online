<template>
	<v-container>
		<v-sheet
			class="mb-4 px-4 pt-4 rounded-lg pb-1"
			elevation="2"
		>
			<v-text-field class="mx-2" v-model="searchName" label="搜索商品" variant="solo" clearable></v-text-field>
			<v-row no-gutters>
				<v-col cols="6">
					<v-text-field class="mx-2" v-model="priceRange_low" label="最低价格" variant="solo" clearable type="number"></v-text-field>
				</v-col>
				<v-col cols="6">
					<v-text-field class="mx-2" v-model="priceRange_high" label="最高价格" variant="solo" clearable type="number"></v-text-field>
				</v-col>
			</v-row>
			<v-icon>mdi-filter-variant</v-icon>
			<v-btn 
				:prepend-icon="orderBy === 'price'? 'mdi-sort-descending' : orderBy === '-price' ? 'mdi-sort-ascending' : ''" 
				@click="onclickOrderBy('price')"
				variant="text"
				:color="orderBy === 'price' || orderBy === '-price' ? 'green' : ''"
			>价格</v-btn>
			<v-btn 
				:prepend-icon="orderBy === 'name' ? 'mdi-sort-descending' : orderBy === '-name' ? 'mdi-sort-ascending' : ''" 
				@click="onclickOrderBy('name')"
				variant="text"
				:color="orderBy === 'name' || orderBy === '-name' ? 'green' : ''"
			>名称</v-btn>
			<v-btn 
				:prepend-icon="orderBy === 'rating'? 'mdi-sort-descending' : orderBy === '-rating' ? 'mdi-sort-ascending' : ''" 
				@click="onclickOrderBy('rating')"
				variant="text"
				:color="orderBy === 'rating' || orderBy === '-rating' ? 'green' : ''"
			>评分</v-btn>
			<v-btn 
				:prepend-icon="orderBy === 'created_at'? 'mdi-sort-descending' : orderBy === '-created_at' ? 'mdi-sort-ascending' : ''" 
				@click="onclickOrderBy('created_at')"
				variant="text"
				:color="orderBy === 'created_at' || orderBy === '-created_at' ? 'green' : ''"
			>上架时间</v-btn>
			<v-chip-group
				class="mb-2 mt-1"
				v-model="chosenCategory"
				v-if="categoryList"
				column
			>
				<v-chip
					v-for="category in categoryList"
					:key="category.id"
					filter
					color="primary"
				>{{ category.name }}</v-chip>
			</v-chip-group>
		</v-sheet>
		<div v-if="!loading">
			<v-infinite-scroll :items="items" :onLoad="fetchProducts" >
				<template #empty>
					<p class="text-h6 font-weight-bold mt-4">没有更多的商品了</p>
				</template>
				<template v-for="(item, index) in items" :key="item.id">
					<div v-if="$vuetify.display.md || $vuetify.display.lg || $vuetify.display.xl || $vuetify.display.xxl">
						<v-row v-if="index % 3 === 0" style="width: 100%;" class="mt-2">
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
					</div>
					<div v-else>
						<div style="height: 8px;"></div>
						<product-card
							:product="item" 
							:shop-id="item.shop"
							:remove-product-callback="null"
						></product-card>
					</div>
				</template>
			</v-infinite-scroll>
		</div>
	</v-container>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { getAllProductList, getCategories } from '@/api/product';
import productCard from '@/components/productCard';

const latestProductList = ref(null)
const categoryList = ref(null)
const items = ref([])

const chosenCategory = ref(null)
const priceRange_low = ref(null)
const priceRange_high = ref(null)
const searchName = ref('')
const orderBy = ref(null)
const loading = ref(false)

const onclickOrderBy = ( option ) => {
	const nowOption = orderBy.value
	if (nowOption === null) {
		orderBy.value = option
	} else if (nowOption[0] === '-' && nowOption.slice(1) === option) {
		orderBy.value = null
	} else if (nowOption === option) {
		orderBy.value = `-${option}`
	} else {
		orderBy.value = option
	}
}

watch([chosenCategory, priceRange_low, priceRange_high, searchName, orderBy], async () => {
	console.log('watch')
	loading.value = true
	await async function() {
		latestProductList.value = null
		items.value = []
	}()
	loading.value = false
})

const fetchProducts = async ({ done }) => {
	let page = 1;
	if (latestProductList.value) {
		if (latestProductList.value.next === null) {
			done('empty')
			return
		}
		page = latestProductList.value.cur_page + 1
	}
	const options = {
    page: page,
		category: chosenCategory.value !== null && chosenCategory.value !== undefined ? categoryList.value[chosenCategory.value].id : null,
		price__gte: priceRange_low.value ? priceRange_low.value : null,
		price__lte: priceRange_high.value ? priceRange_high.value : null,
		search: searchName.value ? searchName.value : null,
		ordering: orderBy.value ? orderBy.value : null
	}
	const res = await getAllProductList(options)
	latestProductList.value = res
	items.value.push(...res.products)

	done('ok')
}

onMounted(async () => {
	categoryList.value = (await getCategories()).data.categories
})


</script>