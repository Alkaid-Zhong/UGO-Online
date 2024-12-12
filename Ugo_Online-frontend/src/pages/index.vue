<template>
	<v-container>
		<v-carousel
			:height="$vuetify.display.xs?'15vh':'calc(30vh - 64px)'"
			show-arrows="hover"
			cycle
			interval="5000"
			hide-delimiter-background
			hide-delimiters
		><!-- ['精选好物，尽在UGO', '价格实惠，值得信赖', '品质保证，放心选购', '全球直邮，轻松购物'] -->
			<v-carousel-item
				v-for="(slide, i) in bannerItems"
				:key="i"
				rounded="lg"

			>
				<v-sheet
					@click="() => router.push(slide.to)"
					class="banner_item"
					height="100%"
					:style="{'background-image': 'url('+slide.image+')',
					'background-position': 'center',
					   'background-size': 'auto 100% !important',
					   'overflow': 'hidden',
					   'background-repeat': 'no-repeat',
					   'background-size': 'cover' }"
				>
					<div class="d-flex fill-height justify-center align-center">
						<p :style="$vuetify.display.sm || $vuetify.display.md || $vuetify.display.lg || $vuetify.display.xl || $vuetify.display.xxl ? {fontSize: '3.6rem', fontWeight: 'lighter'} : { fontSize: '2.5rem', fontWeight: 'lighter' }">
							{{ slide.title }}
						</p>
					</div>
				</v-sheet>
			</v-carousel-item>
		</v-carousel>
		<v-menu
			:close-on-content-click="false"
		>
			<template v-slot:activator="{ props }">
				<v-btn
					style="position: fixed; bottom: 120px; right:20px; z-index: 1000;"
					color="primary"
					icon="mdi-magnify"
					v-bind="props"
				></v-btn>
			</template>
			<v-sheet
				class="mb-4 px-4 pt-6 rounded-lg pb-1"
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
					:prepend-icon="orderBy === 'create_date'? 'mdi-sort-descending' : orderBy === '-create_date' ? 'mdi-sort-ascending' : ''"
					@click="onclickOrderBy('create_date')"
					variant="text"
					:color="orderBy === 'create_date' || orderBy === '-create_date' ? 'green' : ''"
				>上架时间</v-btn>
				<v-btn
					:prepend-icon="orderBy === 'sales_volume'? 'mdi-sort-descending' : orderBy === '-sales_volume' ? 'mdi-sort-ascending' : ''"
					@click="onclickOrderBy('sales_volume')"
					variant="text"
					:color="orderBy === 'sales_volume' || orderBy === '-sales_volume' ? 'green' : ''"
				>销量</v-btn>
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
		</v-menu>
		<div v-if="!loading">
			<v-infinite-scroll :items="items" :onLoad="fetchProducts" class="pa-1">
				<template #empty>
					<p class="text-h6 font-weight-bold mt-4">没有更多的商品了</p>
				</template>
				<template v-for="(item, index) in items" :key="item.id">
					<div v-if="$vuetify.display.lg || $vuetify.display.xl || $vuetify.display.xxl">
						<v-row v-if="index % 4 === 0" style="width: 100%;" class="mt-2">
							<v-col cols="3">
								<product-card
									:product="item"
									:shop-id="item.shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="3">
								<product-card
									v-if="index + 1 < items.length"
									:product="items[index + 1]"
									:shop-id="items[index + 1].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="3">
								<product-card
									v-if="index + 2 < items.length"
									:product="items[index + 2]"
									:shop-id="items[index + 2].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="3">
								<product-card
									v-if="index + 3 < items.length"
									:product="items[index + 3]"
									:shop-id="items[index + 3].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
						</v-row>
					</div>
					<div v-else-if="$vuetify.display.md">
						<v-row v-if="index % 3 === 0" style="width: 100%;" class="mt-2">
							<v-col cols="4">
								<product-card
									:product="item"
									:shop-id="item.shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="4">
								<product-card
									v-if="index + 1 < items.length"
									:product="items[index + 1]"
									:shop-id="items[index + 1].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="4">
								<product-card
									v-if="index + 2 < items.length"
									:product="items[index + 2]"
									:shop-id="items[index + 2].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
						</v-row>
					</div>
					<div v-else-if="$vuetify.display.sm">
						<v-row v-if="index % 2 === 0" style="width: 100%;" class="mt-2">
							<v-col cols="6">
								<product-card
									:product="item"
									:shop-id="item.shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
							<v-col cols="6">
								<product-card
									v-if="index + 1 < items.length"
									:product="items[index + 1]"
									:shop-id="items[index + 1].shop"
									:category-list="categoryList"
								></product-card>
							</v-col>
						</v-row>
					</div>
					<div v-else>
						<div class="mb-2"></div>
						<product-card
							:product="item"
							:shop-id="item.shop"
							:category-list="categoryList"
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
import router from '@/router';

const latestProductList = ref(null)
const categoryList = ref(null)
const items = ref([])

const chosenCategory = ref(null)
const priceRange_low = ref(null)
const priceRange_high = ref(null)
const searchName = ref('')
const orderBy = ref(null)
const loading = ref(false)


const bannerItems = [
	{
		title: '',
		// color: '#4CAF50',
		image: '/apple.png',
		to: '/shop/3'
	},
	{
		title: '',
		// color: '#2196F3',
		image: '/new_12_1.png',
		to: '/shop/'
	},
	{
		title: '',
		// color: '#FF5722',
		image: '/black_monkey_short.png'
	},
	// {
	// 	title: '全球直邮，轻松购物',
	// 	color: '#9C27B0',
	// 	image: '/apple.png'
	// }
]
const onclickOrderBy = ( option ) => {
	const nowOption = orderBy.value
	if (nowOption === null) {
		orderBy.value = `-${option}`
	} else if (nowOption[0] === '-' && nowOption.slice(1) === option) {
		orderBy.value = option
	} else if (nowOption === option) {
		orderBy.value = null
	} else {
		orderBy.value = `-${option}`
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
	loading.value = true
	categoryList.value = (await getCategories()).data.categories
	loading.value = false
})


</script>

<style scoped>
/* .banner_item {
  background-size: auto 100% !important;
} */
</style>
