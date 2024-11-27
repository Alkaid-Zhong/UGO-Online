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
							:model-value="shopInfo.total_income"
						></v-rating>
					</div>
				</template>
				<template #subtitle>
					<p class="mb-2 font-weight-bold">{{ `地址：${shopInfo.address}` }}</p>
					<p>{{ shopInfo.description }}</p>
				</template>
				<template #append>
					<v-chip v-if="shop_id == user.shopId" color="green" prepend-icon="mdi-store">我的商铺</v-chip>
				</template>
				<v-card-actions v-if="shop_id == user.shopId">
					<v-btn color="primary" @click="showAddProduct = true" prepend-icon="mdi-plus">添加商品</v-btn>
					<v-btn color="primary" @click="showInvite = true" prepend-icon="mdi-account-plus">邀请加入商店</v-btn>
					<v-btn color="primary" @click="onclickShowFlow" prepend-icon="mdi-chart-line" :loading="loadingFlow">查看商店流水</v-btn>
				</v-card-actions>
			</v-card>
			<v-row v-if="products">
				<v-col cols="12" md="4" v-for="product in products.products">
					<product-card :product="product" />
				</v-col>
			</v-row>
		</div>
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
					<v-text-field
						label="商品描述"
						v-model="productDescription"
						required
					></v-text-field>
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
					<v-card-text>创建日期：{{ new Date(inviteInfo.created_at).toLocaleString() }}</v-card-text>
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
				<div class="d-flex align-center justify-space-between mb-4">
					<v-icon class="mr-4">mdi-filter</v-icon>
					<v-chip-group
						v-model="flowChoices"
						filter
					>
						<v-chip color="green">只看收入</v-chip>
						<v-chip color="red">只看退款</v-chip>
					</v-chip-group>
					<v-text-field
						class="mt-4"
						variant="outlined"
						label="搜索日期"
						v-model="flowDate"
						type="date"
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
						<v-chip v-else color="red" small>退款</v-chip>
					</template>
				</v-data-table-server>
				<v-pagination
					v-model="flowPage"
					:length="shopFlow.total_pages"
				></v-pagination>
			</v-card-item>
		</v-card>
	</v-dialog>
	
</template>
<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { user } from '@/store/user';
import { getInviteCode, getShopFlow, getShopInfo } from '@/api/shop';
import { addProduct, getCategories, getProductList } from '@/api/product';
import snackbar from '@/api/snackbar';
import productCard from '@/components/productCard.vue';

const route = useRoute()
const { shop_id } = route.params

const shopInfo = ref(null)
const categoryList = ref(null)
const showAddProduct = ref(false)
const showInvite = ref(false)
const showShopFlow = ref(false)
const loadingFlow = ref(false)

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

const flowHeaders = [
	{ title: '流水号', key: 'id', sortable: false },
	{ title: '订单号', key: 'order_id', sortable: false },
	{ title: '交易金额', key: 'amount' },
	{ title: '交易类型', key: 'transaction_type', sortable: false },
	{ title: '交易时间', key: 'date' },
	{ title: '描述', key: 'description', sortable: false }
]

onMounted(async () => {
	shopInfo.value = await getShopInfo(shop_id)
	products.value = await getProductList(shop_id)
	categoryList.value = (await getCategories()).data.categories
})

watch(flowChoices, async () => {
	flowPage.value = 1
	await fetchFlow()
})

watch(flowDate, async () => {
	flowPage.value = 1
	await fetchFlow()
})

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
		products.value = await getProductList(shop_id)
		showAddProduct.value = false
		productName.value = ''
		productDescription.value = ''
		productPrice.value = ''
		productCategory.value = ''
		productStock.value = ''
		productImage.value = null
	}
}


</script>