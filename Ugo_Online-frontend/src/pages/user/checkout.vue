<template>
    <v-container>
        <v-row v-if="!loading">
            <v-col cols="12" md="8">
                <v-card>
                    <v-card-title>
                        <h3>选择地址</h3>
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-item-group v-model="selectedAddress" mandatory class="d-flex" style="flex-grow: 1;">
                                <v-container>
                                  <transition-group name="slide-fade" tag="div"> 
                                  <v-row style="flex-grow: 1;">
                                        <v-col cols="4" style="flex-grow: 1;" v-for="(address, index) in paginatedAddresses" :key="index">
                                            <v-item v-slot= "{ isSelected, toggle }" :value="address">
                                                <v-card :class="[ { ['bg-primary']: isSelected }]" @click="toggle">
                  
                                                
                                                  <v-card-text>
    
                                                    <div >
                                                    <div ><small>{{ address.recipient_name }} {{ address.phone }}</small></div>
                                                    <div><small>{{ address.province }} {{ address.city }}</small></div>
                                                    <div class="font-weight-bold text-lg">{{ address.address }}</div>
                                                
                                                    <!-- {{ address }} -->
                  
                                                  </div>
                  
                                                  </v-card-text>


                                                </v-card>
                                            </v-item>
                                        </v-col>
                                        <v-spacer></v-spacer>
                                    </v-row>
                                  </transition-group> 
                                </v-container>
                            </v-item-group>
                        </v-row>
                        
          
                        <!-- <v-text-field
                            label="输入地址"
                            prepend-inner-icon="mdi-map-marker"
                            append-inner-icon="mdi-check"
                        ></v-text-field> -->
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="currentPage--" :disabled="currentPage <= 0">上一页</v-btn>
                        <v-btn @click="currentPage++" :disabled="currentPage >= totalPages - 1">下一页</v-btn>
                    </v-card-actions>
                </v-card>
                <br>
                <v-card>
                    <v-card-title>
                        <h3>商品列表</h3>
                    </v-card-title>
                    <v-list>
                        <v-list-item v-for="item in items" :key="item.item_id">
                            <v-list-item-action class="d-inline-flex" style="width:100%">                        
                              <v-img :src="item.image" height="96" width="96"></v-img>
                              <v-container width="100%" style="margin-left: auto;">
                                <v-row>
                                  <v-col cols="3" class="pt-0 ">
                                    <strong>{{ item.product_name }}</strong>
                                  </v-col>
                                  
                                  <v-col cols="3" class="pt-0 text-center">
                                    <a class="font-weight-bold text-decoration-none" @click="router.push(`/shop/${getShopId(item.product_id)}`)">{{ getShopName(item.product_id) }}</a>
                                    
                                  </v-col>

                                  <v-col cols="4" style="color:orangered" class="text-h6 pt-0 text-center">
                                    {{ currency(item.price) }}
                                  </v-col>

                                  <v-col cols="2" class="text-center pt-0">
                                    <b>x {{item.quantity}}</b>

                                  </v-col>
                                </v-row>
                                
                              </v-container>
                          </v-list-item-action>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card style="position: sticky; top: 78px;">
                <v-card-title>
                    <span class="font-weight-bold">本单合计 共 {{ quantityAll }} 件商品</span>
                </v-card-title>
                <v-container>
                    <v-row>
                        <!-- 商品名 * 件数 （展开）？ -->
                    </v-row>
                </v-container>

                <v-card-text class="text-right" style="color:orangered;">
                    合计：￥{{ cart.totalSum }}<br/>
                    优惠：{{ cart.discount }}<br/>
                    <span class="text-h5">实付：￥{{ cart.actualSum }}</span>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="router.push('/user/cart/')">返回修改</v-btn>
                    <v-btn color="red-lighten-1" @click="createOrder" class="font-weight-bold">立即下单</v-btn>
                </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { getAddresses } from '@/api/user';
import { cart } from '@/store/cart';
import { useRouter } from 'vue-router';
import snackbar from '@/api/snackbar';
import { getShopInfo } from '@/api/shop';
import { getProductDetail } from '@/api/product';

const loading = ref(true);
const addresses = ref([]);
const selectedAddress = ref(null);
const router = useRouter();
const items = ref([]);

const currency = (value) => {
  let val = parseFloat(value);
  if (val > 9999999) {
    return `￥${(val / 10000).toFixed(2)} 万`;
  } else {
    return `￥${parseFloat(value).toFixed(2)}`;
  }
};

const fetchOrderItems = async () => {
  if (cart.selectedItems.length === 0) {
    snackbar.error("您还未选中商品");
    router.push('/user/cart/');
    return;
  }
  items.value = cart.selectedItems;
  for (const item of items.value) {
    await shopInfo(item);
  }
  loading.value = false;
};

const quantityAll = computed(() => {
  return cart.selectedItems.reduce((acc, item) => acc + item.quantity, 0);
});


const currentPage = ref(0);
const addressPerPage = 3;

const paginatedAddresses = computed(() => {
    const start = currentPage.value * addressPerPage;
    const end = start + addressPerPage;
    return addresses.value.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(addresses.value.length / addressPerPage);
});

const fetchAddresses = async () => {
  const response = await getAddresses();
  addresses.value = response.data;
  selectedAddress.value = addresses.value[0];
};


const shopInfoCache = {};
const product_shop = {};

const shopInfo = async (product) => {
  let productId = product.product_id;
  const shopId = (await getProductDetail(productId)).data.shop;
  if (!shopInfoCache[shopId]) {
    const response = await getShopInfo(shopId);
    shopInfoCache[shopId] = response;
  }
  product_shop[productId] = shopId;
  return shopInfoCache[shopId];
};

const getShopName = (productId) => {
  const shopId = product_shop[productId];
  return shopInfoCache[shopId].name;
};

const getShopId = (productId) => {
  return product_shop[productId];
};




onMounted(() => {
  fetchAddresses();
  fetchOrderItems();
});

const createOrder = async () => {
  if (!selectedAddress.value) {
    snackbar.error("请选择地址");
    return;
  }
  // const response = await create;
  // if (response.status === 201) {
  //   snackbar.success("下单成功");
  //   router.push('/user/order/');
  // } else {
  //   snackbar.error("下单失败");
  // }
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

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.5s ease;
}
.slide-fade-enter, .slide-fade-leave-to /* .slide-fade-leave-active in <2.1.8 */ {
  transform: translateX(100%);
  opacity: 0;
}

</style>