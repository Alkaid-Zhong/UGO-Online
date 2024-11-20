<template>
	<v-card height="100%">
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
				v-if="user.role === 'SELLER'"
				color="primary"
			>编辑商品</v-btn>
		</v-card-actions>
	</v-card>
</template>
<script setup>
import { addToCart } from '@/api/cart';
import snackbar from '@/api/snackbar';
import { user } from '@/store/user';

const props = defineProps({
	product: {
		type: Object,
		required: true
	}
})

const { product } = props

const onclickAdd2Card = async () => {
	const res = await addToCart(product.id, 1);
	if (res.success) {
		snackbar.success(`${product.name} 已加入购物车`);
	} else {
		snackbar.error('添加失败');
	}
}

</script>