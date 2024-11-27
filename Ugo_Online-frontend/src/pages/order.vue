<template>
    <v-container v-if="!loading">
        
        <v-row> <!-- customer -->
            <v-col cols="12">
            <v-list v-for="order in orders">
                <v-card>
                    <v-card-title v-if="isCustomer">
                        <v-btn
                            class="text-h6 font-weight-bold"
                            variant="text"
                            prepend-icon="mdi-store"
                            append-icon="mdi-chevron-right"
                            @click="router.push(`/shop/${order.shop_id}/`)"
                        >{{ ShopInfo(order.shop_id).name }} </v-btn>
                    </v-card-title>
                    <v-card-title v-else>

                        {{ order.address.recipient_name }} 的订单 
                        <v-spacer></v-spacer>
                        <small> 订单ID: {{ order.order_id    }}</small>
                    </v-card-title>
                    <v-card-subtitle class="font-weight-bold" >
                        <span> 共 {{ order.items.length }} 件商品，总价:</span> <span style="color:orangered;">￥{{ order.total_price }}</span> 
                        <span> 订单状态：<v-chip tile :color="orderStatusColor(order.status)">{{ formatStatus(order.status) }}</v-chip></span>
                    </v-card-subtitle>
                    
                    <v-list-item v-for="item in order.items" width="100%">
                        
                            <v-container width="100%" style="margin-left: auto;" >
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
                                    <!-- {{order.status}} {{  item.is_cancelled }} -->
                                    <v-btn text="退货" v-if="isCustomer && showRefundButton(order.status, item.is_cancelled)" @click="refund(order,item)"></v-btn> <!-- v-if="showRefuncButton(order)"  bug？-->

                                </v-col>
                            </v-row>
                            
                            </v-container>
                        
                        <!-- {{ item }} -->
                    </v-list-item>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="warning" v-if="isCustomer && order.status === 'Pending Payment'" class="font-weight-bold" @click="orderDialog('pay', order)">支付</v-btn> <!--payOrder(order)--> 
                        
                        
                        <v-btn color="success" v-if="isSeller && order.status === 'Payment Received' " @click="ship(order)">发货</v-btn>
                        <v-btn color="primary" @click="router.push(`/order/${order.order_id}/`)">查看详情</v-btn>
                    </v-card-actions>
                </v-card>
                
            </v-list>
            </v-col>
        </v-row> 

        <!-- <v-row v-else> 
            <v-col cols="12">
                <v-list>

                </v-list>
            </v-col>
        </v-row> -->

        <v-dialog width="40%" v-model="showDialog">

            <template v-if="dialogContent==='pay'" v-slot:default="{ isActive }">
                <v-card title="支付确认">
                <v-card-text>
                    <span>当前余额：￥{{ user.money }}元</span><br>
                    <span>支付金额：￥{{ curOrder.total_price }}元</span>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                    text="取消"
                    @click="isActive.value = false"
                    ></v-btn>
                    <v-btn color="warning" class="font-weight-bold" text="确认支付" @click="payOrder(curOrder), isActive.value = false">
                    </v-btn>
                </v-card-actions>
                </v-card>
            </template>

            <template v-else-if="dialogContent==='change address'" v-slot:default="{ isActive }">
                <v-card title="修改地址"> 
                <!-- <v-card-text> TODO
                    <span>当前余额：￥{{ user.money }}元</span><br>
                    <span>支付金额：￥{{ curOrder.total_price }}元</span>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                    text="取消"
                    @click="isActive.value = false"
                    ></v-btn>
                    <v-btn color="warning" class="font-weight-bold" text="确认修改" @click="payOrder(curOrder), isActive.value = false">
                    </v-btn>
                </v-card-actions> -->
                </v-card>
            </template>
        </v-dialog>
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
import snackbar from '@/api/snackbar';
import { sellerGetOrders, sellerShip, userGetOrders, userPayOrders, userRefund } from '@/api/order';
import { getShopInfo } from '@/api/shop';
import router from '@/router';
import { profile } from '@/api/user';

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
    profile().then(()=>{
        if (user.role === 'CUSTOMER') {
            console.log("haha");
            isCustomer.value = true;
            isSeller.value = false;
            userGetOrders().then(res => {
                //console.log(res.data.orders);
                orders.value = res.data.orders;
                fetchShopInfo().then(() => {
                    loading.value = false;
                    // console.log("loading false");
                });
            }).catch(err => {
                console.log(err);
            })
        } else {
            isCustomer.value = false;
            isSeller.value = true;
            sellerGetOrders().then(res => {
                //console.log(res.data.orders);
                orders.value = res.data.orders;
                // fetchCustomerInfo().then(() => {
                loading.value = false;
                // });
            }).catch(err => {
                console.log(err);
            })
        }
    });
    
    
})

const curOrder = ref();
const showDialog = ref(false);
const dialogContent = ref(''); // pay, change address, receive, cancel!   (refund?)

const orderDialog = (content, order) => {
    dialogContent.value = content;
    switch (content) {
        case 'pay':
            profile().then(() => {
                console.log(user);
                console.log("订单价格：" + order.total_price, "用户余额：" + user.money);
                if (parseInt(user.money) < parseInt(order.total_price)) {
                    snackbar.error("余额不足(当前余额 "+ user.money +"元), 请充值");
                    return;
                } else {
                    curOrder.value = order;
                    showDialog.value = true;
                    
                }
            });
            break;
        case 'change address':
            //changeAddressDialog(order);
            break;
        case 'receive':
            //receiveDialog(order);
            break;
        default:
            break;
    }
    console.log(order);
}

const orderStatusColor = (status)=> {
    switch (status) {
        case 'Pending Payment':
            return 'warning';
        case 'Payment Received':
            return 'primary';
        case 'Completed':
            return 'success';
        case 'Cancelled':
            return 'error';
        case 'Refund Requested':
            return 'error';
        case 'Refund Successful':
            return 'error';
        case 'Shipped':
            return 'primary';
        default:
            return 'grey';
    }

        // if (isCustomer.value) {
        //     // 用户
            
        // } else {
        //     // 商家
        //     return 'success';
        // }
};

const showRefundButton = ((orderStatus, isCancelled) => {
    return orderStatus === 'Payment Received' && isCancelled === false ; // || status === 'Completed'
});

const refund = async (order, item) => {
    const order_id = order.order_id;
    console.log(order_id, item);
    
    const response = await userRefund(order_id, [item.id]);
    if (response.success) {
        snackbar.success("退款申请成功");
        item.is_cancelled = true;
        if (order.items.every(item => item.is_cancelled)) {
            order.status = 'Refund Requested';
        }
    } else {
        snackbar.error("退款申请失败" + response.message);
    }
}

const payOrder = async (order) => {
    console.log(order);
    const response = await userPayOrders([order.order_id]);
    if (response.success) {
        snackbar.success("支付成功");
        order.status = 'Payment Received';
    } else {
        // console.log(response);
        snackbar.error("支付失败：" + response.data.message);
    }
}


const ship = async (order) => {
    console.log(order);
    const response = await sellerShip(order.order_id);
    if (response.success) {
        snackbar.success("发货成功");
        order.status = 'Completed';
    } else {
        snackbar.error("发货失败：" + response.message);
    }
}

const formatStatus = (status) => {
    switch (status) {
        case 'Pending Payment':
            return '待支付';
        case 'Payment Received':
            return '已支付，待发货';
        case 'Completed':
            return '已完成';
        case 'Cancelled':
            return '已取消';
        case 'Refund Requested':
            return '退款申请中';
        case 'Refund Successful':
            return '退款成功';
        case 'Shipped':
            return '商家已发货';
        default:
            return status;
    }
}

// for Sellers

// const fetchCustomerInfo = async () => {
//     for (let i = 0; i < orders.value.length; i++) {
//         await customerInfo(orders.value[i].user);
//     }
// }

// const customerInfoCache = ref({});
// const customerInfo = async (userId) => {
//   if (!customerInfoCache.value[userId]) {
//     const response = await  (userId);
//     customerInfoCache.value[userId] = response;
//   }
//   return customerInfoCache[userId];
// };

// const CustomerInfo = (userId) => {
//     // console.log(shop_id);
//     console.log(customerInfoCache.value[userId]);
//     return customerInfoCache.value[userId];
// }

// for customers

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