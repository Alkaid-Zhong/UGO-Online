<template>
	<v-container>
		<v-skeleton-loader v-if="!shopInfo" type="image, article" />
		<div v-else>
			<v-card class="mb-4">
				<template #title>
					<div class="d-flex align-center mb-2">
						<h2 class="headline">{{ shopInfo.name }}</h2>
						<v-rating
							class="ml-2"
							readonly
							density="compact"
							half-increments
							active-color="amber"
							color="amber-darken-1"
							:model-value="shopInfo.average_rating"
						></v-rating>
					</div>
				</template>
				<template #subtitle>
					<p class="mb-2 font-weight-bold">{{ `地址：${shopInfo.address}` }}</p>
					<p>{{ shopInfo.description }}</p>
				</template>
				<template #append>
					<v-chip v-if="user.shops.includes(Number(shop_id))" color="green" prepend-icon="mdi-store">我的商铺</v-chip>
				</template>
				<template #prepend>
					<v-avatar size="100px" class="mr-2 rounded-lg" tile>
						<v-img :src="shopInfo.picture || '/logo.png'" aspect-ratio="1"></v-img>
					</v-avatar>
				</template>
				<v-card-actions v-if="user.shops.includes(Number(shop_id))">
					<v-btn color="primary" @click="showAddProduct = true" prepend-icon="mdi-plus">添加商品</v-btn>
					<v-btn color="primary" @click="showInvite = true" prepend-icon="mdi-account-plus">邀请加入商店</v-btn>
					<v-btn color="primary" @click="onclickShowFlow" prepend-icon="mdi-chart-line" :loading="loadingFlow">查看商店流水</v-btn>
					<v-btn color="primary" @click="onclickModifyShopInfo" prepend-icon="mdi-pencil">修改商店信息</v-btn>
				</v-card-actions>
			</v-card>
			<v-menu
				:close-on-content-click="false"
			>
				<template v-slot:activator="{ props }">
					<v-btn
						style="position: fixed; bottom: 120px; right:20px; z-index: 1000"
						color="primary"
						icon="mdi-magnify"
						v-bind="props"
					></v-btn>
				</template>
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
						class="my-2"
						v-model="chosenCategory"
						v-if="categoryList"
						column
					>
						<v-chip
							v-for="category in shopCategory"
							:key="category.id"
							filter
							color="primary"
						>{{ category.name }}</v-chip>
					</v-chip-group>
					<v-chip-group
						class="my-2"
						v-model="availableOnly"
						v-if="user.shops.includes(Number(shop_id))"
						column
					>
						<v-chip
							key="unavaliableOnly"
							filter
							color="red"
						>只看已下架</v-chip>
						<v-chip
							key="avaliableOnly"
							filter
							color="primary"
						>只看未下架</v-chip>
						<v-chip
							key="stockOnly"
							filter
							color="orange"
						>只看无库存</v-chip>
					</v-chip-group>
				</v-sheet>
			</v-menu>
			<v-row v-if="products">
				<v-col cols="12" sm="6" md="4" lg="3" v-for="product in products.products">
					<product-card 
						:product="product" 
						:category-list="categoryList" 
						:shop-id="Number(shop_id)"
						:remove-product-callback="removeProductCallback"
					/>
				</v-col>
			</v-row>
		</div>
    <v-pagination
      v-if="products"
			class="mt-4"
      v-model="page"
      :length="products.total_page"
    ></v-pagination>
	</v-container>
	<v-dialog v-model="showAddProduct" transition="dialog-bottom-transition">
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showAddProduct = false"
				></v-btn>
				<v-toolbar-title>添加商品</v-toolbar-title>
				<v-spacer></v-spacer>
				<v-toolbar-items>
					<v-btn
						text="上传"
						variant="text"
						@click="onclickAddProduct"
						prepend-icon="mdi-check"
					></v-btn>
				</v-toolbar-items>
			</v-toolbar>
			<v-card-item>
				<v-form>
					<v-text-field
						label="商品名称"
						v-model="productName"
						required
					></v-text-field>
					<div class="d-flex mb-2">
						<v-text-field
							label="商品描述"
							v-model="productDescription"
							required
						></v-text-field>
						<v-btn
							class="ml-4 mr-2 mt-2"
							size="large"
							:loading="loadingGenIntro"
							:prepend-icon="productDescription.trim() === '' ? 'mdi-pencil' : 'mdi-refresh'"
							@click="onclickGenIntro"
							:text="productDescription.trim() === '' ? '生成简介' : '润色简介'"
						></v-btn>
					</div>
					<v-text-field
						label="商品价格"
						v-model="productPrice"
						type="number"
						required
					></v-text-field>
					<v-select
						label="商品分类"
						v-model="productCategory"
						required
						:items="categoryList"
						item-title="name"
						item-value="id"
					></v-select>
					<v-text-field
						label="商品库存"
						v-model="productStock"
						type="number"
						required
					></v-text-field>
					<v-file-input
						label="商品图片"
						multiple
						accept="image/*"
						required
						@change="productImage = $event.target.files[0]"
					></v-file-input>
				</v-form>
			</v-card-item>
		</v-card>
	</v-dialog>
	
	<v-dialog v-model="showInvite" transition="dialog-bottom-transition" max-width="600px">
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showInvite = false"
				></v-btn>
				<v-toolbar-title>邀请加入{{ shopInfo.name }}</v-toolbar-title>
			</v-toolbar>
			<v-card-item v-if="!inviteInfo">
				<v-select
					v-model="never_expire"
					label="有效期"
					:items="[
						{ text: '永久', value: true },
						{ text: '自定义', value: false }
					]"
					item-title="text"
					item-value="value"
					:disabled="generateInviteCodeLoading"
				></v-select>
				<v-expand-transition>
					<v-text-field
						v-show="!never_expire"
						label="有效期(天)"
						v-model="expires_in_days"
						type="number"
						required
						:disabled="generateInviteCodeLoading"
					></v-text-field>
				</v-expand-transition>
				<v-text-field
					label="使用次数"
					v-model="usage_limit"
					type="number"
					required
					:disabled="generateInviteCodeLoading"
				></v-text-field>
				<v-btn
					color="primary"
					@click="onclickGenerateInviteCode"
					text="生成邀请码"
					:loading="generateInviteCodeLoading"
				></v-btn>
			</v-card-item>
			<div v-else>
				<v-card-item class="text-center">
					<v-sheet color="green" class="d-flex justify-center align-center rounded-xl ma-4">
						<v-icon size="36px" color="white" class="mr-2 my-2">mdi-check</v-icon>
						<span class="font-weight-bold text-h5">邀请码：{{ inviteInfo.code }}</span>
					</v-sheet>
					<v-card-text>创建日期：{{ new Date(inviteInfo.create_date).toLocaleString() }}</v-card-text>
					<v-card-text>有效期至：{{ inviteInfo.expires_at ? new Date(inviteInfo.expires_at).toLocaleString() : '永久' }}</v-card-text>
					<v-card-text>已用次数：{{ inviteInfo.usage_count }}</v-card-text>
					<v-card-text>剩余次数：{{ inviteInfo.usage_limit - inviteInfo.usage_count }}</v-card-text>
					<v-btn
						class="mb-2"
						color="red"
						@click="inviteInfo = null"
						variant="plain"
					>重新生成</v-btn>
				</v-card-item>
			</div>
		</v-card>
	</v-dialog>

	
	<v-dialog v-model="showShopFlow" transition="dialog-bottom-transition" fullscreen>
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showShopFlow = false"
				></v-btn>
				<v-toolbar-title>{{ shopInfo.name }}的流水</v-toolbar-title>
				<v-spacer></v-spacer>
			</v-toolbar>
			<v-card-item>
				<p class="mt-2 font-weight-bold text-h5">商店资金：
					<span class="text-h6" style="color: red;">￥</span>
					<span style="color: red;">{{ shopInfo.total_income }}</span>
				</p>
			</v-card-item>
			<v-card-item>
				<v-btn
					color="orange"
					@click="showSplitDialog = true"
					:prepend-icon="'mdi-cash-multiple'"
				>为商家分成</v-btn>
				<div class="d-flex align-center justify-space-between mb-4">
					<v-icon class="mr-4">mdi-filter</v-icon>
					<v-chip-group
						v-model="flowChoices"
						filter
					>
						<v-chip color="green">只看收入</v-chip>
						<v-chip color="red">只看退款</v-chip>
						<v-chip color="purple">只看分成</v-chip>
					</v-chip-group>
					<v-text-field
						class="mt-4"
						variant="outlined"
						label="搜索日期"
						v-model="flowDate"
						type="date"
						clearable 
					></v-text-field>
				</div>
				<v-data-table-server
					:headers="flowHeaders"
					:items="shopFlow.transactions"
					:items-length="shopFlow.count"
    			hide-default-footer
					@update:options="reloadFlow"
					:loading="loadingFlow"
				>
					<template v-slot:item.date="{ item }">
						{{ new Date(item.date).toLocaleString() }}
					</template>
					<template v-slot:item.transaction_type="{ item }">
						<v-chip v-if="item.transaction_type === 'Income'" color="green" small>收入</v-chip>
						<v-chip v-else-if="item.transaction_type === 'Refund'" color="red" small>退款</v-chip>
						<v-chip v-else color="purple" small>分成</v-chip>
					</template>
				</v-data-table-server>
				<v-pagination
					class="mt-4"
					v-model="flowPage"
					:length="shopFlow.total_page"
				></v-pagination>
			</v-card-item>
		</v-card>
	</v-dialog>

	<v-dialog
		v-model="showSplitDialog"
		transition="dialog-bottom-transition"
		max-width="600px"
	>
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showSplitDialog = false"
				></v-btn>
				<v-toolbar-title>分成商家</v-toolbar-title>
			</v-toolbar>
			<v-card-item>
				<v-text-field
					label="分成金额"
					v-model="splitAmount"
					type="number"
					required
				></v-text-field>
				<v-select
					label="分成商家"
					v-model="splitSeller"
					required
					:items="shopInfo.sellers"
					item-title="name"
					item-value="id"
				></v-select>
				<v-btn
					color="primary"
					@click="onclickSplit"
					text="确认分成"
					:loading="splitLoading"
				></v-btn>
			</v-card-item>
		</v-card>
	</v-dialog>
	
	<v-dialog
		v-model="showModifyShopInfo"
		transition="dialog-bottom-transition"
		max-width="600px"
	>
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showModifyShopInfo = false"
				></v-btn>
				<v-toolbar-title>编辑商店信息</v-toolbar-title>
			</v-toolbar>
			<v-card-item>
				<v-text-field
					label="商店名称"
					v-model="shopName"
					required
				></v-text-field>
				<v-text-field
					label="商店描述"
					v-model="shopDescription"
					required
				></v-text-field>
				<v-text-field
					label="商店地址"
					v-model="shopAddress"
					required
				></v-text-field>
				<v-file-input
					label="商店Logo"
					accept="image/*"
					@change="shopLogo = $event.target.files[0]"
				></v-file-input>
				<v-btn
					color="primary"
					@click="onclickSubmitModifyShopInfo"
					text="确认修改"
					:loading="splitLoading"
				></v-btn>
			</v-card-item>
		</v-card>
	</v-dialog>
	
</template>
<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { user } from '@/store/user';
import { getInviteCode, getShopFlow, getShopInfo, modifyShopInfo, splitToSeller } from '@/api/shop';
import { addProduct, generateProductIntro, getCategories, getProductList, getShopCategories } from '@/api/product';
import snackbar from '@/api/snackbar';
import productCard from '@/components/productCard.vue';

const route = useRoute()
const { shop_id } = route.params

const shopInfo = ref(null)
const categoryList = ref(null)
const shopCategory = ref(null)
const showAddProduct = ref(false)
const showInvite = ref(false)
const showShopFlow = ref(false)
const loadingFlow = ref(false)
const page = ref(1)

const chosenCategory = ref(null)
const priceRange_low = ref(null)
const priceRange_high = ref(null)
const searchName = ref('')
const orderBy = ref(null)

const availableOnly = ref(null)

const productName = ref('')
const productDescription = ref('')
const productPrice = ref('')
const productCategory = ref('')
const productStock = ref('')
const productImage = ref(null)
const products = ref(null)

const inviteInfo = ref(null)
const never_expire = ref(true)
const expires_in_days = ref(1)
const usage_limit = ref(1)
const generateInviteCodeLoading = ref(false)

const shopFlow = ref(null)
const flowPage = ref(1)
const flowChoices = ref(null)
const flowDate = ref('')

const showSplitDialog = ref(false)
const splitAmount = ref(0)
const splitSeller = ref(null)
const splitLoading = ref(false)

const showModifyShopInfo = ref(false)
const shopName = ref('')
const shopDescription = ref('')
const shopAddress = ref('')
const shopLogo = ref(null)

const loadingGenIntro = ref(false)
const genIntro = ref(null)

const onclickGenIntro = async () => {
	loadingGenIntro.value = true
	let res
	if (productDescription.value.trim() === '') {
		res = await generateProductIntro(productName.value)
	} else {
		res = await generateProductIntro(productName.value, productDescription.value)
	}
	productDescription.value = res.data.introduction
	loadingGenIntro.value = false
}

const onclickModifyShopInfo = async () => {
	showModifyShopInfo.value = true
	shopName.value = shopInfo.value.name
	shopDescription.value = shopInfo.value.description
	shopAddress.value = shopInfo.value.address
}

const onclickSubmitModifyShopInfo = async () => {
	const data = new FormData()
	data.append('name', shopName.value)
	data.append('description', shopDescription.value)
	data.append('address', shopAddress.value)
	if (shopLogo.value) {
		data.append('picture', shopLogo.value)
	}
	const res = await modifyShopInfo(shop_id, data)
	shopInfo.value = await getShopInfo(shop_id)
	showModifyShopInfo.value = false
}

const flowHeaders = [
	{ title: '流水号', key: 'id', sortable: false },
	{ title: '订单号', key: 'order_id', sortable: false },
	{ title: '交易金额', key: 'amount' },
	{ title: '交易类型', key: 'transaction_type', sortable: false },
	{ title: '交易时间', key: 'date' },
	{ title: '描述', key: 'description', sortable: false }
]

const onclickSplit = async () => {
	if (!splitAmount.value || splitAmount.value <= 0) {
		snackbar.error('分成金额必须大于0')
		return
	}
	if (!splitSeller.value) {
		snackbar.error('分成商家不能为空')
		return
	}
	splitLoading.value = true
	const res = await splitToSeller(shop_id, Number(splitSeller.value), Number(splitAmount.value))
	if (res.success) {
		snackbar.success('分成成功')
		showSplitDialog.value = false
		splitAmount.value = 0
		splitSeller.value = null
	}
	shopInfo.value = await getShopInfo(shop_id)
	await fetchFlow()
	splitLoading.value = false
}

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

onMounted(async () => {
	shopInfo.value = await getShopInfo(shop_id)
	categoryList.value = (await getCategories()).data.categories
	shopCategory.value = (await getShopCategories(shop_id)).data.categories
	products.value = await getProductList(shop_id)
})

watch([flowChoices, flowDate], async () => {
	flowPage.value = 1
	await fetchFlow()
})

watch(flowPage, async () => {
	await fetchFlow()
})

watch([chosenCategory, priceRange_low, priceRange_high, searchName, orderBy, availableOnly], async () => {
  page.value = 1
	await fetchProductList()
})

watch(page, async () => {
	await fetchProductList()
})

const removeProductCallback = async (product_id) => {
  await fetchProductList()
	page.value = products.value.total_page;
}

const fetchProductList = async () => {
	products.value = null
	const options = {
    page: page.value,
		category: chosenCategory.value !== null && chosenCategory.value !== undefined ? shopCategory.value[chosenCategory.value].id : null,
		price__gte: priceRange_low.value ? priceRange_low.value : null,
		price__lte: priceRange_high.value ? priceRange_high.value : null,
		search: searchName.value ? searchName.value : null,
		ordering: orderBy.value ? orderBy.value : null,
		status: availableOnly.value === null ? null : (availableOnly.value === 0 ? 'Unavailable' : availableOnly.value === 1 ? 'Available' : null),
		stock_quantity: availableOnly.value === 2 ? 0 : null
	}
	products.value = await getProductList(shop_id, options)
}

const reloadFlow = async ({ sortBy }) => {
	const sortOptions = {}
	if (sortBy.length > 0) {
		console.log(sortBy[0].order)
		console.log(sortBy[0].key)
		if (sortBy[0].order == 'desc') {
			sortOptions['ordering'] = `-${sortBy[0].key}`
		} else {
			sortOptions['ordering'] = sortBy[0].key
		}
	}
	await fetchFlow(sortOptions)
}

const onclickShowFlow = async () => {
	loadingFlow.value = true
	flowChoices.value = null
	await fetchFlow()
	loadingFlow.value = false
	showShopFlow.value = true
}

const fetchFlow = async ( sortOptions = {} ) => {
	loadingFlow.value = true
	const options = { ...sortOptions }
	if (flowChoices.value === 0) {
		options.transaction_type = 'Income'
	} else if (flowChoices.value === 1) {
		options.transaction_type = 'Refund'
	} else if (flowChoices.value === 2) {
		options.transaction_type = 'Divide'
	}
	if (flowDate.value && flowDate.value.trim() !== '') {
		options.date = flowDate.value
	}
	const res = await getShopFlow(shop_id, {
		page: flowPage.value,
		...options
	})
	if (res.success) {
		shopFlow.value = res.data
	} else {
		snackbar.error(res.message)
	}
	loadingFlow.value = false
}

const onclickGenerateInviteCode = async () => {
	generateInviteCodeLoading.value = true
	const res = await getInviteCode(shop_id, {
		expires_in_days: never_expire.value ? null : expires_in_days.value,
		usage_limit: usage_limit.value
	})
	if (res.success) {
		inviteInfo.value = res.data
		snackbar.success('邀请码已生成')
	} else {
		snackbar.error(res.message)
	}
	generateInviteCodeLoading.value = false
}

const onclickAddProduct = async () => {
	if (!productName.value || productName.value.trim() === '') {
		snackbar.error('商品名称不能为空')
		return
	}
	if (!productDescription.value || productDescription.value.trim() === '') {
		snackbar.error('商品描述不能为空')
		return
	}
	if (!productPrice.value || productPrice.value.trim() === '') {
		snackbar.error('商品价格不能为空')
		return
	}
	if (!productCategory.value) {
		snackbar.error('商品分类不能为空')
		return
	}
	if (!productStock.value || productStock.value.trim() === '') {
		snackbar.error('商品库存不能为空')
		return
	}
	if (!productImage.value || productImage.value.length === 0) {
		snackbar.error('商品图片不能为空')
		return
	}
	const res = await addProduct(shop_id, {
		name: productName.value,
		description: productDescription.value,
		price: productPrice.value,
		category: productCategory.value,
		stock_quantity: productStock.value,
		image: productImage.value
	})
	if (res.success) {
		snackbar.success('添加成功')
		window.location.reload()
	}
}


</script>