<template>
	<v-container>
		<v-skeleton-loader v-if="!shopInfo" type="image, article" />
		<div v-else>
			<v-card class="mb-4">
				<template #title>
					<h2 class="headline mb-1">{{ shopInfo.name }}</h2>
				</template>
				<template #subtitle>
					<p class="mb-2 font-weight-bold">{{ `地址：${shopInfo.address}` }}</p>
					<p>{{ shopInfo.description }}</p>
				</template>
				<template #append>
					<v-chip v-if="shop_id == user.shopId" color="green" prepend-icon="mdi-store">我的商铺</v-chip>
				</template>
				<v-card-actions v-if="shop_id == user.shopId">
					<v-btn color="primary" @click="showAddProductDialog" prepend-icon="mdi-plus">添加商品</v-btn>
				</v-card-actions>
			</v-card>
			<v-row v-if="products">
				<v-col cols="12" md="4" v-for="product in products.products">
					<v-card>
						<v-img :src="product.image" aspect-ratio="1" class="mb-2" />
						<v-card-title>{{ product.name }}</v-card-title>
						<v-card-text>{{ product.description }}</v-card-text>
					</v-card>
				</v-col>
			</v-row>
		</div>
	</v-container>
	<v-dialog v-model="showAddProduct" fullscreen transition="dialog-bottom-transition">
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
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { user } from '@/store/user';
import { getShopInfo } from '@/api/shop';
import { addProduct, getCategories, getProductList } from '@/api/product';
import snackbar from '@/api/snackbar';

const route = useRoute()
const { shop_id } = route.params

const shopInfo = ref(null)
const categoryList = ref(null)
const showAddProduct = ref(false)

const productName = ref('')
const productDescription = ref('')
const productPrice = ref('')
const productCategory = ref('')
const productStock = ref('')
const productImage = ref(null)
const products = ref(null)

onMounted(async () => {
	shopInfo.value = await getShopInfo(shop_id)
	products.value = await getProductList(shop_id)
})

const showAddProductDialog = async () => {
	const res = await getCategories()
	if (res.success) {
		categoryList.value = res.data.categories
	} else {
		snackbar.error(res.message)
	}
	showAddProduct.value = true
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