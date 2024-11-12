<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <span class="headline">购物车</span>
          </v-card-title>
          <v-card-text v-if="!loading">

            <v-list-item v-if="shopLists.length === 0">
                <v-list-item-title>购物车空空如也，快去逛逛吧</v-list-item-title>
            </v-list-item>

            <v-list v-else>
                
                <v-list-item v-for="item in shopLists" :key="item.shop_id">
                  
                    <v-list-item-title>{{ item.shop_name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ currency(item.shop_id) }}</v-list-item-subtitle>
                  
                </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="checkout">结算</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref, onMounted, reactive } from 'vue';
import {getCart} from '@/api/cart';
import {cart} from '@/store/cart';
import {user} from '@/store/user';

const loading = ref(true);

const fetchCartItems = async () => {
  const response = await getCart();
  shopLists.value = response.data.shops;
  //console.log("shopLists:", shopLists.value);
  loading.value = false;
};

onMounted(() => {
  fetchCartItems();
});

const shopLists = ref([{ 
  shop_id: 0,
  shop_name: 'test',
  items: [],
}]);

// const removeItem = (id) => {
//   cartItems.value = cartItems.value.filter(item => item.id !== id);
// };

const checkout = () => {
  alert('还没写！');
};

const currency = (value) => {
  if (!value) {
    console.log("error!");
    return `undefined`;
  }
  return `${value.toFixed(2)}元`;
};

</script>

<style scoped>
.headline {
  font-weight: bold;
}
</style>