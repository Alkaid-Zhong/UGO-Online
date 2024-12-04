<template>
	<v-card height="100%">
		<div class="d-flex flex-column justify-space-between" style="height: 100%">
			<v-img :src="product.image" aspect-ratio="1" />
			<v-divider></v-divider>
			<v-card-item class="px-2 pb-0">
				<span style="font-size: 16px; color: red; font-weight: bold">￥</span>
				<span class="font-weight-bold text-h5" style="color: red;">
					{{ product.price }}
				</span>
			</v-card-item>
			<v-card-title class="py-0">
				{{ product.name }}
				<v-chip size="x-small" color="primary" class="mb-1">{{ product.category_name }}</v-chip>
			</v-card-title>
			<v-card-subtitle class="py-0">库存：{{ product.stock_quantity }}</v-card-subtitle>
			<v-card-text class="pt-2 pb-0">{{ product.description }}</v-card-text>
			<v-card-actions>
				<v-btn
					v-if="user.role === 'CUSTOMER'"
					color="primary"
					@click="onclickAdd2Card"
					prepend-icon="mdi-cart"
				>加入购物车</v-btn>
				<v-btn
					v-if="user.role === 'SELLER' && user.shops.includes(Number(shopId))"
					color="primary"
					@click="showUpdateProduct = true"
				>编辑商品</v-btn>
				<v-btn
					v-if="user.role === 'SELLER' && removeProductCallback !== null"
					color="red"
					@click="onclickDeleteProduct"
				>删除商品</v-btn>
			</v-card-actions>
		</div>
	</v-card>
	
	<v-dialog v-model="showUpdateProduct" transition="dialog-bottom-transition">
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showUpdateProduct = false"
				></v-btn>
				<v-toolbar-title>编辑{{ product.name }}</v-toolbar-title>
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
import { ref } from 'vue';
import { addToCart } from '@/api/cart';
import snackbar from '@/api/snackbar';
import { user } from '@/store/user';
import { deleteProduct, updateProduct } from '@/api/product';

const props = defineProps({
	shopId: {
		type: Number,
		required: true
	},
	product: {
		type: Object,
		required: true
	},
	categoryList: {
		type: Array,
		required: true
	},
	removeProductCallback: {
		type: Function,
		required: true
	}
})

const { product, shopId, removeProductCallback } = props

const showUpdateProduct = ref(false)

const productName = ref(product.name)
const productDescription = ref(product.description)
const productPrice = ref(product.price)
const productCategory = ref(product.category)
const productStock = ref(product.stock_quantity)
const productImage = ref(null)

const onclickDeleteProduct = async () => {
	if((await deleteProduct(shopId, product.id)).success) {
		removeProductCallback(product.id)
		snackbar.success('商品删除成功');
	}
}

const onclickAdd2Card = async () => {
	const res = await addToCart(product.id, 1);
	if (res.success) {
		snackbar.success(`${product.name} 已加入购物车`);
	} else {
		snackbar.error('添加失败');
	}
}

const onclickAddProduct = async () => {
	const formData = new FormData();
	formData.append('name', productName.value);
	formData.append('description', productDescription.value);
	formData.append('price', productPrice.value);
	formData.append('category', productCategory.value);
	formData.append('stock_quantity', productStock.value);
	if (productImage.value) {
		formData.append('image', productImage.value);
	}
	formData.append('product_id', product.id);
	const res = await updateProduct(shopId, formData);
	if (res.success) {
		snackbar.success('商品信息更新成功');
		showUpdateProduct.value = false;
		product.name = res.data.name;
		product.description = res.data.description;
		product.price = res.data.price;
		product.category = res.data.category;
		product.stock_quantity = res.data.stock_quantity;
		product.image = res.data.image;
		product.category_name = res.data.category_name;
	} else {
		snackbar.error('商品信息更新失败');
	}
}

</script>