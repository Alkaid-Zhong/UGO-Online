<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-list v-if="!loading" class="pt-4 rounded-lg">
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-cart" size="x-large"></v-icon>
            </template>
            <v-list-item-title class="text-h4 font-weight-bold">购物车</v-list-item-title>
          </v-list-item>

          <v-list-item class="mb-2">
            <template #prepend>
              <v-list-item-action start>
                <v-checkbox 
                  v-model="selectAll" 
                  class="d-flex align-items-center" 
                  :label="`全部商品 (${cartCount})`"
                ></v-checkbox>
              </v-list-item-action>
            </template>
            <template v-slot:append>
                <v-btn @click="deleteSelectedItem()" class="mr-2"> 删除所选 </v-btn>
                <v-btn @click="deleteDisabeldItem()"> 一键删除无货/失效商品 </v-btn>
            </template>
          </v-list-item>

          <v-divider></v-divider>
          
          <transition-group name="list">
            <v-list-item v-if="shopLists.length === 0">
              <v-list-item-title>购物车空空如也，快去逛逛吧</v-list-item-title>
            </v-list-item>
          
            <v-list-item v-for="shop in shopLists" v-else>
              <v-card elevation="0">
                <v-card-title class="mt-2 pa-2">
                  <v-btn
                    class="text-h5 font-weight-bold"
                    variant="text"
                    prepend-icon="mdi-store"
                    append-icon="mdi-chevron-right"
                    @click="router.push(`/shop/${shop.shop_id}`)"
                  >{{ shop.shop_name }}</v-btn>
                </v-card-title>
                <v-card-text class="px-0">
                  
                  <v-list lines="2">
                  <transition-group name="list">
                    
                    <v-list-item class="pl-0 pt-2 pb-3 pr-0" v-for="item in shop.items" :key="item.item_id">

                      <!-- <template #default="{ active }"> -->
                        <v-list-item-action class="d-inline-flex" style="width:100%">
                          <v-checkbox v-model="itemSelected" :value="item" class="d-flex" :disabled="item.product_stock_quantity < item.quantity"></v-checkbox>
                        
                          <v-img :src="item.image" height="96" width="96"></v-img>
                          <v-container width="100%" style="margin-left: auto;">
                            <v-row>
                              <v-col cols="4" class="pt-0">
                                <strong>{{ item.product_name }}</strong>
                              </v-col>
                                <v-col cols="4" :style="{ color: item.product_stock_quantity >= item.quantity ? 'orangered' : 'grey' }" class="text-h6 pt-0">
                                {{ currency(item.price) }}
                                </v-col>
                              <v-col cols="4" class="d-flex">
                                <v-row >
                                  <v-col cols="3" class="pa-0">
                                    <v-responsive aspect-ratio="1" width="100%">
                                      <v-btn @click="decreaseQuantity(item)" class="w-100 h-100" block tile 
                                      style=" border: 1px solid #d6d6d6">
                                      <v-icon size="midium">mdi-minus</v-icon>
                                    </v-btn>
                                    </v-responsive>
                                    
                                  </v-col>
                                  <v-col cols="6" class="pa-0">
                                  <v-responsive aspect-ratio="2" width="100%">
                                    <input type="number" v-model="item.quantity" @click="saveOldValue(item.quantity)" @blur="changeQuantity($event, item)" class="w-100 h-100" 
                                    style="text-align: center; border-top: 1px solid #d6d6d6;
                                    border-bottom: 1px solid #d6d6d6;
                                    border-left: 0;
                                    border-right: 0;"></input>
                              </v-responsive>
                                  </v-col>
                                  <v-col cols="3" class="pa-0">
                                  <v-responsive aspect-ratio="1" width="100%">
                                    <v-btn @click="increaseQuantity(item)" block class="w-100 h-100" tile
                                    style=" border: 1px solid #d6d6d6">
                                  <v-icon>mdi-plus</v-icon>
                                </v-btn>
                              </v-responsive>
                                  </v-col>
                                </v-row>
                                <!-- <v-btn @click="decreaseQuantity(item)" style="width: 40px; height: 40px;">
                                  <v-icon size="small">mdi-minus</v-icon>
                                </v-btn> -->

                              </v-col>
                            </v-row>
                            
                          </v-container>
                        </v-list-item-action>
                        
                      <!-- </template> -->
                    </v-list-item>
                  </transition-group>
                </v-list>
              </v-card-text>

            </v-card>

            <v-divider></v-divider>
          </v-list-item>
          
          </transition-group>
        </v-list>

        

        
      </v-col>
      <v-col cols="12" md="4">
        <v-card style="position: sticky; top: 84px;">
          <v-card-title>
            <span class="font-weight-bold">明细</span>
          </v-card-title>
          <v-container v-if="selectedNotEmpty">
            <v-row>
              <v-hover v-slot:default="{ isHovering }">
                <v-col cols="3" v-for="item in itemSelected.slice(0,4)" >
                  <v-img :src="item.image" aspect-ratio="1">
                    
                    <v-overlay :value="isHovering" absolute opacity="0.7" @click="handleClick()" class="test">
                      <v-row class="fill-height" align="center" justify="center">
                        <v-btn color="primary" @click="handleClick()">点击我</v-btn>
                      </v-row>
                    </v-overlay>
                
                  </v-img>
                </v-col>
              </v-hover>
            </v-row>
          </v-container>
          <v-container v-else>
            <v-row>
              <v-col>
                <v-list-item>
                  <v-list-item-title>请在左侧选中商品后查看价格明细</v-list-item-title>
                </v-list-item>
              </v-col>
            </v-row>
          </v-container>

          <v-card-text v-if="selectedNotEmpty" class="text-right" style="color:orangered;">
            合计：￥{{ totalSum }}<br/>
            优惠：{{ discount }}<br/>
            <span class="text-h5">实付：￥{{ actualSum }}</span>
          </v-card-text>

          <v-card-actions>
            <v-btn block border color="red-lighten-1" @click="checkout">结算</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { deleteItem, getCart, updateCart } from '@/api/cart';
import snackbar from '@/api/snackbar';
import router from '@/router';
import { cart } from '@/store/cart';

const loading = ref(true);

const fetchCartItems = async () => {
  const response = await getCart();
  shopLists.value = response.data.shops;
  cart.items = shopLists.value.flatMap(shop => shop.items);
  if (cart.selectedItems.length !== 0) {
    itemSelected.value = cart.selectedItems;
  } 
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

const queryRemove = (item) => {
  
}


const increaseQuantity = async(item) => {
  if (item.quantity >= item.product_stock_quantity) {
    snackbar.error("库存不足");
    return;
  }
  const success = await updateQuantity(item.item_id, item.quantity+1);
  if (success){
      
  } else {
    snackbar.error("网络不佳，请稍后再试");
  }
}

const decreaseQuantity = async(item) => {
  if (item.quantity > 0) {
    const success = await updateQuantity(item.item_id, item.quantity-1);
    if (success){
      if (item.quantity === 0) {
        itemSelected.value = itemSelected.value.filter(i => i.item_id !== item.item_id);
        const shop = shopLists.value.find(shop => shop.items.includes(item));
        if (shop) {
          shop.items = shop.items.filter(i => i.item_id !== item.item_id);
          if (shop.items.length === 0) {
            shopLists.value = shopLists.value.filter(s => s.shop_id !== shop.shop_id);
          }
        }
      }
    } else {
      snackbar.error("网络不佳，请稍后再试");
    }
  } 
}


const oldValue = ref(0);
var end = true;
const saveOldValue = (value) => {
  if (!end) {
    return;
  }
  end = false;
  oldValue.value = value;
}
const changeQuantity = (event, item) => {
  end = true;
  const newValue = parseInt(event.target.value, 10);
  if (newValue === oldValue.value) {
    return;
  }
  if (newValue >= 0 && newValue <= item.product_stock_quantity) {
    // item.quantity = newValue;
    updateQuantity(item.item_id, newValue);
  } else {
    item.quantity = oldValue.value;
    snackbar.error("库存不足，请重试");
  }
};

const updateQuantity = async (id, newQuantity) => {
  const response = await updateCart(id, newQuantity);
  console.log(response);
  if (response.success) {
    const item = shopLists.value.flatMap(shop => shop.items).find(item => item.item_id === id);
    if (item) {
      console.log(response.data.product);
      item.quantity = newQuantity;
      item.product_stock_quantity = response.data.product.stock_quantity;
    }
    return true;
  }
  return false;
}

const deleteSelectedItem = async() => {
  itemSelected.value.forEach(async item => {
    const success = await deleteItem(item.item_id);
    if (success) {
      itemSelected.value = itemSelected.value.filter(i => i.item_id !== item.item_id);
      const shop = shopLists.value.find(shop => shop.items.includes(item));
      if (shop) {
        shop.items = shop.items.filter(i => i.item_id !== item.item_id);
        if (shop.items.length === 0) {
          shopLists.value = shopLists.value.filter(s => s.shop_id !== shop.shop_id);
        }
      }
    } else {
      snackbar.error("网络不佳，请稍后再试");
    }
  });
}

const cartCount = computed(() => {
  return shopLists.value.reduce((acc, shop) => acc + shop.items.length, 0);
});
const totalSum = computed(() => {
  return itemSelected.value.reduce((acc, item) => acc + item.price * item.quantity, 0).toFixed(2);
});

const discount = ref(0);
const actualSum = computed(() => totalSum.value - discount.value);
const itemSelected = ref([]);
const selectedNotEmpty = computed(() => itemSelected.value.length > 0);
const selectAll = ref(false);

watch(selectAll, (value) => {
  if (value) {
    itemSelected.value = shopLists.value.reduce((acc, shop) => acc.concat(shop.items.filter(item => item.quantity <= item.product_stock_quantity)), []);
  } else {
    itemSelected.value = [];
  }
});


const checkout = () => {
  // alert('还没写！');
  if (selectedNotEmpty.value) {
    cart.actualSum = actualSum;
    cart.discount = discount;
    cart.totalSum = totalSum;
    cart.selectedItems = itemSelected.value;
    router.push('/user/checkout/');
  } else {
    // TODO shake animation and alert
    snackbar.warning("请选择商品后再结算");
  }
};

const currency = (value) => {
  let val = parseFloat(value);
  if (val > 9999999) {
    return `￥${(val / 10000).toFixed(2)} 万`;
  } else {
    return `￥${parseFloat(value).toFixed(2)}`;
  }
};
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* 隐藏 Firefox 中的上下增减按钮 */
input[type="number"] {
  -moz-appearance: textfield;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(0);
}

.v-overlay__scrim {
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
}

</style>
