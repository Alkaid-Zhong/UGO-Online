<template>
	<v-card height="100%" @click="onclickShowDetail">
		<div class="d-flex flex-column justify-space-between" style="height: 100%">
			<v-img :src="product.image" aspect-ratio="1" />
			<v-divider></v-divider>
			<v-card-item class="px-2 pb-0">
				<span style="font-size: 16px; color: red; font-weight: bold">￥</span>
				<span class="font-weight-bold text-h5" style="color: red;">
					{{ product.price }}
					<v-chip v-if="product.status === 'Unavailable'" size="x-small" color="red" class="mb-1">已下架</v-chip>
				</span>
			</v-card-item>
			<v-card-title class="py-0">
				{{ product.name }}
				<v-chip size="x-small" color="primary" class="mb-1">{{ product.category_name }}</v-chip>
			</v-card-title>
			<v-card-subtitle class="py-0">库存：{{ product.stock_quantity }}</v-card-subtitle>
			<v-card-text class="pt-2 pb-6">{{ product.description }}</v-card-text>
			<!-- <v-card-actions>
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
			</v-card-actions> -->
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
	
	<v-dialog v-model="showDetail" transition="dialog-bottom-transition">
		<v-card>
			<v-toolbar>
				<v-btn
					icon="mdi-close"
					@click="showDetail = false"
				></v-btn>
				<v-toolbar-title>{{ product.name }}</v-toolbar-title>
				<v-spacer></v-spacer>
				<v-toolbar-items>
					<v-btn
						v-if="user.role === 'CUSTOMER'"
						@click="onclickAdd2Card"
						variant="text"
						prepend-icon="mdi-cart"
            color="primary"
					>加入购物车</v-btn>
					<v-btn
						v-if="user.role === 'SELLER' && user.shops.includes(Number(shopId))"
						variant="text"
						prepend-icon="mdi-pencil"
						@click="showUpdateProduct = true"
            color="primary"
					>编辑商品</v-btn>
					<v-btn
						v-if="user.role === 'SELLER' && removeProductCallback !== null && product.status !== 'Unavailable'"
						color="red"
						variant="text"
						@click="onclickDeleteProduct"
						prepend-icon="mdi-delete"
					>下架商品</v-btn>
					<v-btn
						v-if="user.role === 'SELLER' && removeProductCallback !== null && product.status === 'Unavailable'"
						color="green"
						variant="text"
						@click="onclickOnsaleProduct"
						prepend-icon="mdi-upload"
					>重新上架商品</v-btn>
					<v-btn
						text="前往商店页"
						variant="text"
						@click="onclickGotoShopPage"
            color="orange"
						prepend-icon="mdi-store"
					></v-btn>
				</v-toolbar-items>
			</v-toolbar>
			<v-card-item>
				<v-row>
					<v-col>
						<v-img :src="product.image" aspect-ratio="1" />
						<v-divider class="my-4"></v-divider>
						<p class="text-h5 font-weight-bold mt-2">{{ product.name }}
							<v-chip size="x-small" color="primary" class="mb-1">{{ product.category_name }}</v-chip></p>
						<p class="ml-2 mt-2">
							<span style="font-size: 16px; color: red; font-weight: bold">￥</span>
							<span class="font-weight-bold text-h5" style="color: red;">
								{{ product.price }}
							</span>
						</p>
						<v-rating
							readonly
							density="compact"
							half-increments
							active-color="amber"
							color="amber-darken-1"
							:model-value="product.average_rating"
						></v-rating>
						<p class="ml-2">库存：{{ product.stock_quantity }}</p>
						<p class="ml-2">销量：{{ product.sales_volume }}</p>
						<p class="ml-2">发布时间：{{ new Date(product.create_date).toLocaleString() }}</p>
						<p class="mt-2" style="font-size: 14px; color: #aaa">{{ product.description }}</p>
					</v-col>
					<v-divider vertical></v-divider>
					<v-col cols="12" md="8">
            <v-sheet
              v-for="review in reviews"
              :key="review.id"
              class="mb-2 pa-4 rounded-lg"
              elevation="2"
            >
              <p class="text-h6 font-weight-bold">
                {{ review.user.name }}
                <span class="ml-2 text-caption font-weight-regular">发布于{{ new Date(review.create_date).toLocaleString() }}</span>
              </p>
              <p class="ml-2 mt-2" style="font-size: 14px; color: #aaa">{{ review.comment }}</p>
							<p v-if="review.merchant_reply" class="ml-2 mt-2 text-caption" style="font-size: 14px; color: #aaa">
								商家回复：{{ review.merchant_reply }}
								<span class="ml-2 text-caption font-weight-regular">发布于{{ new Date(review.reply_date).toLocaleString() }}</span>
							</p>
              <v-rating
                class="mt-2"
                readonly
                density="compact"
                half-increments
                active-color="amber"
                color="amber-darken-1"
                :model-value="review.rating"
              ></v-rating>
            </v-sheet>
            <v-pagination
              v-if="reviews"
              v-model="reviewsPage"
              :length="reviewsTotalPage"
            ></v-pagination>
					</v-col>
				</v-row>
			</v-card-item>
		</v-card>
	</v-dialog>
</template>
<script setup>
import { onMounted, ref, watch } from 'vue';
import { addToCart } from '@/api/cart';
import snackbar from '@/api/snackbar';
import { user } from '@/store/user';
import { deleteProduct, getReview, updateProduct } from '@/api/product';
import router from '@/router';

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
const showDetail = ref(false)

const productName = ref(product.name)
const productDescription = ref(product.description)
const productPrice = ref(product.price)
const productCategory = ref(product.category)
const productStock = ref(product.stock_quantity)
const productImage = ref(null)

const reviews = ref(null)
const reviewsPage = ref(1)
const reviewsTotalPage = ref(1)

watch(reviewsPage, async () => {
  await fetchReviews()
})

const onclickShowDetail = async () => {
  reviews.value = null
  reviewsPage.value = 1
  reviewsTotalPage.value = 1
  showDetail.value = true
  await fetchReviews()
}

const fetchReviews = async () => {
  const res = await getReview(product.id, reviewsPage.value)
  if (res.success) {
    reviews.value = res.data.reviews
    reviewsTotalPage.value = res.data.total_page
  }
}

const onclickGotoShopPage = () => {
	router.push(`/shop/${shopId}`)
}

const onclickDeleteProduct = async () => {
	if((await deleteProduct(shopId, product.id)).success) {
		removeProductCallback(product.id)
		snackbar.success('商品下架成功');
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

const onclickOnsaleProduct = async () => {
	const formData = new FormData();
	formData.append('product_id', product.id);
	formData.append('status', 'Available');
	const res = await updateProduct(shopId, formData);
	if (res.success) {
		snackbar.success('商品上架成功');
		removeProductCallback(product.id)
	} else {
		snackbar.error('商品上架失败');
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