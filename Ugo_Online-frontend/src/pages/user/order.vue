<template>
    <v-container v-if="!loading">
        <v-row v-if="isCustomer"> <!-- customer -->
            <v-col cols="12">
            <v-list v-for="order in orders">
                <v-card>
                    <v-card-title>
                        <v-btn
                            class="text-h6 font-weight-bold"
                            variant="text"
                            prepend-icon="mdi-store"
                            append-icon="mdi-chevron-right"
                            @click="router.push(`/shop/${order.shop_id}/`)"
                        >{{ ShopInfo(order.shop_id).name }} </v-btn>
                    </v-card-title>
                    <v-card-subtitle class="font-weight-bold" >
                        <span> 共 {{ order.items.length }} 件商品，总价:</span> <span style="color:orangered;">￥{{ order.total_price }}</span>
                    </v-card-subtitle>
                    
                    <v-list-item v-for="item in order.items" width="100%">
                        
                            <v-container width="100%" style="margin-left: auto;">
                            <v-row>
                                <v-col cols=3>
                                <v-img :src="item.product.image" height="96" width="96"></v-img>
                                </v-col>  
                                <v-col cols="3">
                                <strong>{{ item.product.name }}</strong>
                                </v-col>

                                <v-col cols="3" style="color:orangered" class="text-h6  text-center">
                                {{ currency(item.product.price) }}
                                </v-col>

                                <v-col cols="3" class="text-center">
                                    
                                    <b>x {{item.quantity}}</b><br><br>
                                    <v-btn text="退货" ></v-btn> <!-- v-if="showRefuncButton(order)"  bug？-->

                                </v-col>
                            </v-row>
                            
                            </v-container>
                        
                        <!-- {{ item }} -->
                    </v-list-item>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="router.push(`/order/${order.order_id}/`)">查看详情</v-btn>
                    </v-card-actions>
                </v-card>
                
            </v-list>
            </v-col>
        </v-row> 

        <v-row v-else> <!-- seller -->

        </v-row>
    </v-container>
    <v-container v-else class="d-flex justify-center align-center">
        <v-progress-circular
        
        style="height: 80vh;"
        indeterminate
        color="primary"
        ></v-progress-circular>
    </v-container>
    

</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { user } from '@/store/user';
import { snackbar } from '@/store/app';
import { userGetOrders } from '@/api/order';
import { getShopInfo } from '@/api/shop';
import router from '@/router';

const currency = (value) => {
  let val = parseFloat(value);
  if (val > 9999999) {
    return `￥${(val / 10000).toFixed(2)} 万`;
  } else {
    return `￥${parseFloat(value).toFixed(2)}`;
  }
};

const loading = ref(true);
const isCustomer = ref(false);
const isSeller = ref(false);

const orders = ref([]);

onMounted(() => {
    if (user.role === 'CUSTOMER') {
        isCustomer.value = true;
        userGetOrders().then(res => {
            console.log(res.data.orders);
            orders.value = res.data.orders;
            fetchShopInfo().then(() => {
                loading.value = false;
                console.log("loading false");
            });
        }).catch(err => {
            console.log(err);
        })
    } else {
        isSeller.value = true;
    }
    
})

const showRefuncButton = computed((order) => {
    return order.status === 'Payment Received' || order.status === 'Completed';
})

const fetchShopInfo = async () => {
    for (let i = 0; i < orders.value.length; i++) {
        await shopInfo(orders.value[i].shop_id);
    }
}

const shopInfoCache = ref({});
const shopInfo = async (shopId) => {
  if (!shopInfoCache.value[shopId]) {
    const response = await getShopInfo(shopId);
    shopInfoCache.value[shopId] = response;
  }
  return shopInfoCache[shopId];
};

const ShopInfo = (shop_id) => {
    // console.log(shop_id);
    console.log(shopInfoCache.value[shop_id]);
    return shopInfoCache.value[shop_id];
}

</script>

<style scoped>

</style>