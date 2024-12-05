<template>
    <v-container v-if="!loading">
        <v-row class="mt-3 mb-1">
            <v-col cols="4" v-if="isSeller">
                <v-select
                    v-model="selectedShop"
                    :items="sellerShops"
                    item-title="name"
                    item-value="id"
                    label="选择商铺"
                ></v-select>
            </v-col>
            <v-col :cols="isSeller?8:12" class="d-flex align-center pt-0">
                
                <div><span>订单状态：</span></div>
                
                <v-chip-group
                    v-model="selectedStatus"
                    column
                    filter
                    :selected-class="'text-'+orderStatusColor(selectedStatus)"
                    class="mx-1"
                >
                <!-- @change="fetchOrders(currentPage.value)" -->
                    <v-chip v-for="status in orderStatuses" :key="status" :value="status">
                        {{ formatStatus(status) }}
                    </v-chip>
                </v-chip-group>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row v-if="!orderLoading" class="mt-1"> 
            
            <v-col cols="12" v-if="orders.length !== 0">
                <v-list v-for="order in orders">
                    <v-card>
                        <v-card-title v-if="isCustomer">
                            <v-btn class="text-h6 font-weight-bold" variant="text" prepend-icon="mdi-store"
                                append-icon="mdi-chevron-right" @click="router.push(`/shop/${order.shop_id}/`)">{{
                                    ShopInfo(order.shop_id).name }} </v-btn>
                        </v-card-title>
                        <v-card-title v-else>

                            {{ order.address.recipient_name }} 的订单
                            <v-spacer></v-spacer>
                            <small> 订单ID: {{ order.order_id }}</small>
                        </v-card-title>
                        <v-card-subtitle class="font-weight-bold">
                            <span> 共 {{ order.items.length }} 件商品，总价:</span> <span style="color:orangered;">￥{{
                                order.total_price }}</span>
                            <span> 订单状态：<v-chip tile :color="orderStatusColor(order.status)">{{
                                formatStatus(order.status) }}</v-chip></span>
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

                                        <b>x {{ item.quantity }}</b><br><br>
                                        <!-- {{order.status}} {{  item.is_cancelled }} -->
                                        <v-btn text="退货" color="warning"
                                            v-if="isCustomer && showRefundButton(order.status, item.is_cancelled)"
                                            @click="refund(order, item)"></v-btn>

                                        <v-btn text="评价" color="primary"
                                            v-if="isCustomer && order.status === 'Completed' && !item.has_reviewed"
                                            @click="review(order, item)"></v-btn>
                                        <v-btn text="查看评价" color="info"
                                            v-if="isCustomer && order.status ==='Completed' && item.has_reviewed"
                                            @click="seeReview(order,item)"></v-btn>
                                        <!-- v-if="showRefuncButton(order)"  bug？-->

                                    </v-col>
                                </v-row>

                            </v-container>

                            <!-- {{ item }} -->
                        </v-list-item>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="red" v-if="isCustomer && order.status === 'Pending Payment'"
                                @click="orderDialog('cancel', order)">取消订单</v-btn>
                            <v-btn color="" v-if="isCustomer && showChangeAddressButton(order.status)"
                                @click="orderDialog('change address', order)">修改地址</v-btn>
                            <v-btn color="warning" v-if="isCustomer && order.status === 'Pending Payment'"
                                class="font-weight-bold" @click="orderDialog('pay', order)">支付</v-btn>
                            <!--payOrder(order)-->
                            <v-btn color="success" v-if="isCustomer && order.status === 'Shipped'"
                                class="font-weight-bold" @click="orderDialog('receive', order)">确认收货</v-btn>

                            <v-btn color="success" v-if="isSeller && order.status === 'Payment Received'"
                                @click="ship(order)">发货</v-btn>
                            <!-- <v-btn color="primary" @click="router.push(`/order/${order.order_id}/`)">查看详情</v-btn> -->
                        </v-card-actions>
                    </v-card>

                </v-list>
            </v-col>
            <v-col cols="12" v-else>
                <v-alert type="info" outlined>该商铺暂无订单</v-alert>
                <br><br><br>
            </v-col>
        </v-row>

        <v-skeleton-loader v-else type="image, article" />
        <!-- <v-row v-else> 
            <v-col cols="12">
                <v-list>

                </v-list>
            </v-col>
        </v-row> -->

        <v-dialog v-model="showReview" width="50%">
            <template v-if="createReview" v-slot:default="{isActive}">
                <v-card>
                    <v-card-title class="font-weight-bold">评价</v-card-title>
                    <v-card-text class="d-flex flex-column ">
                        <div class="d-flex align-center">
                            综合评分:<v-rating v-model="reviewRating" label="评分" color="amber"></v-rating>
                        </div>
                        <br>
                        <div>
                            <v-textarea v-model="reviewContent" label="评价内容" rows="3"></v-textarea>
                        </div>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text @click="isActive.value = false">取消</v-btn>
                        <v-btn color="primary" class="font-weight-bold" text="确认评价"
                            @click="submitReview(isActive)"></v-btn>
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
        <v-dialog width="50%" v-model="showDialog">

            <template v-if="dialogContent === 'pay'" v-slot:default="{ isActive }">
                <v-card title="支付确认">
                    <v-card-text>
                        <span>当前余额：￥{{ user.money }}元</span><br>
                        <span>支付金额：￥{{ curOrder.total_price }}元</span>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="取消" @click="isActive.value = false"></v-btn>
                        <v-btn color="warning" class="font-weight-bold" text="确认支付"
                            @click="payOrder(curOrder), isActive.value = false">
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </template>

            <template v-else-if="dialogContent === 'change address'" v-slot:default="{ isActive }">
                <v-card title="修改地址">
                    <AddressSelect :addressPerPage="3" :paying="false" :cardElevator="0" :preSelect="false"
                        @updateSelectedAddress="updateSelectedAddress">

                    </AddressSelect>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="取消" @click="isActive.value = false"></v-btn>
                        <v-btn color="warning" class="font-weight-bold" text="确认修改"
                            @click="changeAddress(), isActive.value = false">
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </template>
            <template v-else-if="dialogContent === 'cancel'" v-slot:default="{ isActive }">
                <v-card title="取消订单">
                    <v-card-text>
                        <span>确定取消订单吗？</span>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="我再想想" @click="isActive.value = false"></v-btn>
                        <v-btn color="warning" class="font-weight-bold" text="确认取消"
                            @click="userCancel(curOrder), isActive.value = false">
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </template>
            <template v-else-if="dialogContent === 'receive'" v-slot:default="{ isActive }">
                <v-card title="确认收货">
                    <v-card-text>
                        <span>您确定已经收到货物了吗？</span>
                        <br>
                        <small>确认收货后将无法退款</small>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="我再想想" @click="isActive.value = false"></v-btn>
                        <v-btn color="success" class="font-weight-bold" text="确认收货"
                            @click="userReceive(curOrder), isActive.value = false">
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
        <v-row>
            <v-col cols="12" class="d-flex justify-center">
                <v-pagination v-model="currentPage" :length="totalPages" total-visible="5"></v-pagination>
                <!--@input="fetchOrders(currentPage)"-->
            </v-col>
        </v-row>
    </v-container>
    <v-container v-else class="d-flex justify-center align-center">
        <v-progress-circular style="height: 80vh;" indeterminate color="primary"></v-progress-circular>
    </v-container>


</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { user } from '@/store/user';
import snackbar from '@/api/snackbar';
import { getReview, sellerGetOrders, sellerShip, userCancelOrder, userChangeAddress, userConfirmOrder, userCreateReview, userGetOrders, userPayOrders, userRefund } from '@/api/order';
import { getShopInfo } from '@/api/shop';
import router from '@/router';
import { profile } from '@/api/user';
import AddressSelect from '@/components/addressSelect.vue';

const currency = (value) => {
    let val = parseFloat(value);
    if (val > 9999999) {
        return `￥${(val / 10000).toFixed(2)} 万`;
    } else {
        return `￥${parseFloat(value).toFixed(2)}`;
    }
};

const loading = ref(true);
const orderLoading = ref(true);
const isCustomer = ref(false);
const isSeller = ref(false);

const shopIds = ref([]);
const orders = ref([]);
const totalPages = ref(1);
const currentPage = ref(1);
const selectedShop = ref({});
const sellerShops = ref([]);
const orderStatuses = ['Pending Payment', 'Payment Received', 'Shipped', 'Completed', 'Cancelled'];
const selectedStatus = ref('');

watch(currentPage, (newVal, oldVal) => {
    orderLoading.value = true;
    fetchOrders(newVal);
});
watch(selectedShop, (newVal, oldVal) => {
    orderLoading.value = true;
    sellerGetOrders(newVal, currentPage.value).then(res => {
        orders.value = res.data.orders;
        orderLoading.value = false;
        totalPages.value = res.data.total_page;
    }).catch(err => {
        console.log(err);
    })
});
watch(selectedStatus, (newVal, oldVal) => {
    orderLoading.value = true;
    fetchOrders(currentPage.value,selectedStatus.value);
});

onMounted(() => {
    profile().then(() => {
        if (user.role === 'CUSTOMER') {
            loading.value = false;
            isCustomer.value = true;
            isSeller.value = false;
            userGetOrders().then(res => {
                //console.log(res.data.orders);
                orders.value = res.data.orders;
                totalPages.value = res.data.total_page;
                fetchShopInfo(orders.value).then(() => {
                    
                    orderLoading.value = false;
                });
            }).catch(err => {
                console.log(err);
            })
        } else {
            isCustomer.value = false;
            isSeller.value = true;
            shopIds.value = user.shops;
            console.log("获取商家管理的店铺ID：");
            console.log(shopIds.value);
            if (shopIds.value.length !== 0) {
                fetchShopInfo(shopIds.value).then(() => {
                    selectedShop.value = shopIds.value[0];
                    sellerShops.value = shopIds.value.map(id => shopInfoCache.value[id]).filter(shop => shop !== undefined);
                    console.log(sellerShops.value);

                    loading.value = false;
                    sellerGetOrders(selectedShop.value).then(res => {
                        orders.value = res.data.orders;
                        // loading.value = false;
                        totalPages.value = res.data.total_page;
                        orderLoading.value = false;
                    }).catch(err => {
                        console.log(err);
                    })
                });
                
            } else {
                loading.value = false;
                orderLoading.value = false;
            }
        }
    });


})

const fetchOrders = async (page, status) => {
    console.log(page);
    if (isCustomer.value) {
        userGetOrders(currentPage.value, status).then(res => {
            orders.value = res.data.orders;
            totalPages.value = res.data.total_page;
            fetchShopInfo(orders.value).then(() => {
                orderLoading.value = false;
            });
        }).catch(err => {
            snackbar.error("获取订单失败" );
            console.log(err);
        })
    } else {
        sellerGetOrders(selectedShop.value , currentPage.value, status).then(res => {
            orders.value = res.data.orders;
            totalPages.value = res.data.total_page;
            console.log("获取到总页数"+totalPages.value);
            orderLoading.value = false;
        }).catch(err => {
            console.log(err);
            snackbar.error("获取订单失败" + err);
        })
    }
}

/* 
Pending Payment, Payment Received, Completed, 
Cancelled, Shipped
*/


const curOrder = ref();
const showReview = ref(false);
const createReview = ref(false);
const reviewContent = ref('');
const reviewRating = ref(0);
const curItem = ref();
const submitReview = async (isActive) => {
    console.log("评价内容：" + reviewContent, "评分：" + reviewRating);
    console.log(curItem.value);
    if (reviewRating.value === 0) {
        snackbar.error("请给商品评分");
        return;
    }
    const response = await userCreateReview(curItem.value.id, curItem.value.product.id, reviewRating.value, reviewContent.value).response;
    if (response.success) {
        snackbar.success("评价成功");
        
        curOrder.value.items.forEach(item => {
            if (item.id === curItem.value.id) {
                item.has_reviewed = true;
            }
        });
        isActive.value=false;
    } else {
        console.log(response);
        snackbar.error("评价失败：" + response.message);
    }
}
const review = (order, item) => {
    curOrder.value = order;
    curItem.value = item;
    createReview.value = !item.has_reviewed;
    console.log(createReview.value);
    showReview.value = true;
}

const seeReview = async (order, item) => {
    // `/shop/order_item/<int:order_item_id>/review/`
    const response = await getReview(item.id);
    if (response.success) {
        snackbar.success("评价内容：" + response.data.comment + " 评分：" + response.data.rating);
    } else {
        snackbar.error("获取评价失败：" + response.message);
    }
    //snackbar.info("评价内容：" + item.review.content + " 评分：" + item.review.rating);
}



const showDialog = ref(false);
const dialogContent = ref(''); // pay, change address, receive, cancel!   (refund?)

const orderDialog = (content, order) => {
    dialogContent.value = content;
    curOrder.value = order;
    switch (content) {
        case 'pay':
            profile().then(() => {
                console.log(user);
                console.log("订单价格：" + order.total_price, "用户余额：" + user.money);
                if (parseInt(user.money) < parseInt(order.total_price)) {
                    snackbar.error("余额不足(当前余额 " + user.money + "元), 请充值");
                    return;
                } else {
                    showDialog.value = true;

                }
            });
            break;
        case 'change address':
            showDialog.value = true;
            console.log("修改地址");
            //changeAddressDialog(order);
            break;
        case 'cancel':
            showDialog.value = true;

            break;
        case 'receive':
            showDialog.value = true;

            //receiveDialog(order);
            break;
        default:
            break;
    }
    //console.log(order);
}

const orderStatusColor = (status) => {
    switch (status) {
        case 'Pending Payment':
            return 'warning';
        case 'Payment Received':
            return 'primary';
        case 'Completed':
            return 'success';
        case 'Cancelled':
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
    return orderStatus === 'Payment Received' && isCancelled === false; // || status === 'Completed'
});

const showChangeAddressButton = ((status) => {
    return status === 'Payment Received' || status === 'Pending Payment';
})

const refund = async (order, item) => {
    const order_id = order.order_id;
    console.log(order_id, item);

    const response = await userRefund(order_id, [item.id]);
    if (response.success) {
        snackbar.success("退款申请成功");
        item.is_cancelled = true;
        if (order.items.every(item => item.is_cancelled)) {
            order.status = 'Cancelled';
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

const userCancel = async (order) => {
    console.log(order);
    const response = await userCancelOrder(order.order_id);
    if (response.success) {
        snackbar.success("订单取消成功");
        order.status = 'Cancelled';
    } else {
        snackbar.error("订单取消失败：" + response.message);
    }
}

const userReceive = async (order) => {
    console.log(order);
    const response = await userConfirmOrder(order.order_id);
    if (response.success) {
        snackbar.success("确认收货成功");
        order.status = 'Completed';
    } else {
        snackbar.error("确认收货失败：" + response.message);
    }
}


const selectedAddress = ref({});
const updateSelectedAddress = (newAddress) => {
    selectedAddress.value = newAddress;
};

const changeAddress = (async () => {
    //console.log("为订单" + curOrder.value.order_id + "修改地址为" + selectedAddress.value.id);
    const response = await userChangeAddress(curOrder.value.order_id, selectedAddress.value.id);
    if (response.success) {
        snackbar.success("地址修改成功");
        curOrder.value.address = selectedAddress.value;
    } else {
        snackbar.error("地址修改失败：" + response.message);
    }
});

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
        case 'Shipped':
            return '商家已发货';
        default:
            return status;
    }
}

const fetchShopInfo = async (shopIdArray) => {
    console.log("Trying to get shop info");
    console.log(shopIdArray[0]);
    if (shopIdArray.length === 0) {
        return;
    } else if (shopIdArray[0].shop_id!== undefined) {
        
        shopIdArray = shopIdArray.map(item => item.shop_id);
    }
    for (let i = 0; i < shopIdArray.length; i++) {
        await shopInfo(shopIdArray[i]);
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
    //console.log(shopInfoCache.value[shop_id]);
    return shopInfoCache.value[shop_id];
}


</script>

<style scoped></style>