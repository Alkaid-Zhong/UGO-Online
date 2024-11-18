<template>
	<v-container>
		<v-sheet
      class="pa-6 rounded-lg"
    >
      <h2 class="headline mb-4">创建店铺</h2>
      <v-form>
				<v-text-field
					label="店铺名称"
					v-model="name"
					required
				></v-text-field>
				<v-text-field
					label="地址"
					v-model="address"
				></v-text-field>
				<v-text-field
					label="描述"
					v-model="description"
				></v-text-field>
        <v-btn
					color="primary"
					@click="onclickSubmitCreate"
        >创建</v-btn>
      </v-form>
    </v-sheet>
	</v-container>
</template>
<script setup>
import { ref } from 'vue'
import snackbar from '@/api/snackbar';
import { createShop } from '@/api/shop';
import router from '@/router';

const name = ref('');
const address = ref('');
const description = ref('');

const onclickSubmitCreate = async () => {
	if (!name.value) {
		snackbar.error('店铺名称不能为空');
		return;
	}
	const res = await createShop({
		name: name.value,
		address: address.value,
		description: description.value
	});
	if (res.success) {
		snackbar.success('创建成功');
		router.replace('/shop');
	}
}

</script>