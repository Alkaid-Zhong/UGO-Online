<template>
	<v-container>
		<v-sheet
      class="pa-6 rounded-lg"
    >
      <h2 class="headline mb-4">{{ joinMode? '加入店铺' : '创建店铺' }}</h2>
      <v-form>
				<v-expand-transition>
					<v-text-field
						v-show="!joinMode"
						label="店铺名称"
						v-model="name"
						required
					></v-text-field>
				</v-expand-transition>
				<v-expand-transition>
					<v-text-field
						v-show="!joinMode"
						label="地址"
						v-model="address"
					></v-text-field>
				</v-expand-transition>
				<v-expand-transition>
					<v-text-field
						v-show="!joinMode"
						label="描述"
						v-model="description"
					></v-text-field>
				</v-expand-transition>
				<v-expand-transition>
					<v-text-field
						v-show="joinMode"
						label="邀请码"
						v-model="inviteCode"
						required
					></v-text-field>
				</v-expand-transition>
        <v-btn
					v-if="!joinMode"
					class="mr-2"
					color="primary"
					@click="onclickSubmitCreate"
        >创建</v-btn>
				<v-btn
					v-else
					class="mr-2"
					color="primary"
					@click="onclickSubmitJoin"
        >加入</v-btn>
				<v-btn
					color="secondary"
					@click="joinMode = !joinMode"
				>{{ joinMode? '创建店铺' : '加入店铺' }}</v-btn>
      </v-form>
    </v-sheet>
	</v-container>
</template>
<script setup>
import { ref } from 'vue'
import snackbar from '@/api/snackbar';
import { createShop, joinShop } from '@/api/shop';
import router from '@/router';

const joinMode = ref(false);

const name = ref('');
const address = ref('');
const description = ref('');
const inviteCode = ref('');

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
		window.reload();
	}
}

const onclickSubmitJoin = async () => {
	if (!inviteCode.value || !inviteCode.value.trim()) {
		snackbar.error('邀请码不能为空');
		return;
	}
	const res = await joinShop(inviteCode.value);
	if (res.success) {
		snackbar.success('加入成功');
		window.reload();
	}
}

</script>