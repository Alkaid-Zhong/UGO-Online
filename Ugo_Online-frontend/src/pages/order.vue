<template>
    <v-container v-if="!loading">
      <v-sheet elevation="2" class="pa-4">
        <v-row class="mt-3 mb-1">
            <v-col cols="4" v-if="isSeller ">
                <v-select
                    v-if="sellerShops.length !== 0"
                    :disabled="orderLoading"
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
                    :disabled="orderLoading"
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
            
            <v-col cols="12" v-if="orders.length !== 0"  :class="{'px-0':$vuetify.display.xs}">
                <v-list v-for="order in orders">
                    <v-card>
                        <v-card-title v-if="isCustomer">
                            <v-btn class="text-h6 font-weight-bold" variant="text" prepend-icon="mdi-store"
                                append-icon="mdi-chevron-right" @click.stop="router.push(`/shop/${order.shop_id}/`)">{{
                                    ShopInfo(order.shop_id).name }} </v-btn>
                        </v-card-title>
                        <v-card-title v-else>

                            {{ order.address.recipient_name }} 的订单
                            <v-tooltip text="此处为订单的收货人姓名">
                                <template v-slot:activator="{ props }">
                                    <v-icon size="x-small" v-bind="props">mdi-help-circle-outline</v-icon>
                                </template>
                            </v-tooltip>
                            <v-spacer></v-spacer>
                            <small> 订单ID: {{ order.order_id }}</small>
                        </v-card-title>
                        <v-card-subtitle class="font-weight-bold">
                            <span> 共 {{ order.items.length }} 件商品，总价:</span> <span style="color:orangered;">￥{{
                                order.total_price }}</span>
                                <br v-if="$vuetify.display.xs">
                            <span> 订单状态：<v-chip tile :color="orderStatusColor(order.status)">{{
                                formatStatus(order.status) }}</v-chip></span>
                        </v-card-subtitle>

                        <v-list-item :class="{'px-0':$vuetify.display.xs}" v-for="item in order.items" width="100%" @click="showDetail(item.product.id)">

                            <v-container width="100%" style="margin-left: auto;">
                                <v-row>
                                    <v-col cols="3" :class="{'px-1':$vuetify.display.xs}">
                                        <v-img :src="item.product.image" height="96" width="96" min-width="48px"></v-img>
                                    </v-col>
                                    <v-col cols="5" md="3"  :class="[{'px-1':$vuetify.display.xs},'text-center']">
                                        <strong>{{ item.product.name }}</strong>
                                    </v-col>

                                    <v-col v-if="$vuetify.display.mdAndUp" md="3" :style="item.is_cancelled ? 'text-decoration: line-through; color: gray;' : 'color:orangered;'" class="text-h6  text-center">
                                        {{ currency(item.unit_price) }}
                                    </v-col>

                                    <v-col cols="4" md="3" class="text-center" :class="{'px-1':$vuetify.display.xs}">  
                                        <span v-if="$vuetify.display.smAndDown" :style="item.is_cancelled ? 'text-decoration: line-through; color: gray;' : 'color:orangered;'"
                                         class="text-h6  text-center"> 
                                         ￥{{ item.unit_price.toString().split('.')[0] }}{{ item.unit_price.toString().split('.')[1] ?'.':'' }}<small>{{ item.unit_price.toString().split('.')[1]  }}</small>
                                         <!-- {{ currency(item.unit_price) }} -->
                                        </span><br v-if="$vuetify.display.smAndDown">

                                        <b>x {{ item.is_cancelled ? 0 :item.quantity }} <br>{{ item.is_cancelled?'（已退货）':'' }}</b><br><br>
                                        <!-- {{order.status}} {{  item.is_cancelled }} -->
                                        <v-btn text="退货" color="warning"
                                            v-if="isCustomer && showRefundButton(order.status, item.is_cancelled)"
                                            @click.stop="refund(order, item)"></v-btn>

                                        <v-btn text="评价" color="primary"
                                            v-if="isCustomer && order.status === 'Completed' && !item.has_reviewed"
                                            @click.stop="review(order, item)"></v-btn>
                                        <v-btn text="查看评价" color="info"
                                            v-if="isCustomer && order.status ==='Completed' && item.has_reviewed"
                                            @click.stop="seeReview(order,item)"></v-btn>
                                        <v-btn :text="item.review_has_reply?'查看回复':'回复评价'" :color="item.review_has_reply?'primary':'warning'" 
                                            v-if="isSeller && order.status === 'Completed' && item.has_reviewed"
                                            @click.stop="reply(order,item)">
                                        </v-btn>
                                        <!-- v-if="showRefuncButton(order)"  bug？-->

                                    </v-col>
                                </v-row>

                            </v-container>

                            <!-- {{ item }} -->
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-card-text>
                            <v-row>
                                <v-col cols="12" sm="4" :class="{'pb-0':$vuetify.display.smAndDown}">
                                    <div :class="infoTitleSizeClass">下单时间：</div>
                                    <div class="ml-2 mt-1">
                                        <div><strong>{{formatDate(order.order_date)}}</strong></div>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="4" class="d-flex justify-center flex-column" :class="{'pb-0':$vuetify.display.smAndDown}">
                                    <div :class="infoTitleSizeClass">地址信息：</div>
                                    <div class="ml-2 mt-1">
                                        <div><strong>收件人姓名:</strong> {{ order.address.recipient_name }}</div>
                                        <div><strong>电话:</strong> {{ order.address.phone }}</div>
                                        <div><strong>省份:</strong> {{ order.address.province }}<strong> 城市:</strong>{{ order.address.city }}</div>
                                        <div><strong>具体地址:</strong> {{ order.address.address }}</div>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="4" :class="{'pb-0':$vuetify.display.smAndDown}">
                                    <div :class="infoTitleSizeClass">订单总价格：</div>
                                    <div class="ml-2 mt-1">
                                        <div style="color:orangered;" class="text-h5"><strong>￥{{ order.total_price }}</strong></div>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-card-text>
                        <v-card-actions v-if="isCustomer && (order.status === 'Pending Payment' || showChangeAddressButton(order.status) || order.status === 'Shipped') || isSeller && order.status === 'Payment Received'">
                            <v-spacer></v-spacer>
                            <v-btn color="red" v-if="isCustomer && order.status === 'Pending Payment'"
                                @click.stop="orderDialog('cancel', order)">取消订单</v-btn>
                            <v-btn color="" v-if="isCustomer && showChangeAddressButton(order.status)"
                                @click.stop="orderDialog('change address', order)">修改地址</v-btn>
                            <v-btn color="warning" v-if="isCustomer && order.status === 'Pending Payment'"
                                class="font-weight-bold" @click.stop="orderDialog('pay', order)">支付</v-btn>
                            <!--payOrder(order)-->
                            <v-btn color="success" v-if="isCustomer && order.status === 'Shipped'"
                                class="font-weight-bold" @click.stop="orderDialog('receive', order)">确认收货</v-btn>

                            <v-btn color="success" v-if="isSeller && order.status === 'Payment Received'"
                                @click.stop="ship(order)">发货</v-btn>
                            <!-- <v-btn color="primary" @click="router.push(`/order/${order.order_id}/`)">查看详情</v-btn> -->
                        </v-card-actions>
                        <!-- <br v-else> -->
                    </v-card>

                </v-list>
            </v-col>
            <v-col cols="12" v-else>
                <v-alert type="info" v-if="isSeller && sellerShops.length === 0" outlined>您还没有商铺呢 <v-btn class="ml-3 pt-0" color="yellow-lighten-3" @click="router.push('/shop/create')"> 立即创建 </v-btn></v-alert>
                <v-alert type="info" v-else outlined>{{ emptyOrderCaption }} </v-alert>
                
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

        <v-dialog v-model="showReview" :width="$vuetify.display.smAndDown?'90%':'50%'">
            <template v-slot:default="{isActive}">
                <v-card>
                    <v-card-title class="font-weight-bold">{{createReview?"":"查看"}}评价</v-card-title>
                    <v-card-text class="d-flex flex-column">
                        <div >
                            {{replying ? "买家":(createReview?'综合':'您的')}}评分:<br> 
                            <v-rating v-model="reviewRating" label="评分" color="amber" :disabled="!createReview"></v-rating>
                        </div>
                        <br>
                        <div>
                            <v-textarea prepend-inner-icon="mdi-comment" v-model="reviewContent" label="评价内容" rows="3" :readonly="!createReview"></v-textarea>
                        </div>
                        <div v-if="replying || alreadyReply">
                            <v-textarea v-model="replyContent" label="商家回复" rows="3" :readonly="alreadyReply"></v-textarea>
                        </div>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text @click="isActive.value = false">{{(createReview || replying && !alreadyReply)?'取消':'关闭'}}</v-btn>
                        <v-btn color="primary" v-if="createReview" class="font-weight-bold" text="确认评价"
                            @click="submitReview(isActive)"></v-btn>
                        <v-btn color="primay" v-if="replying && !alreadyReply" class="font-weight-bold" text="回复评价"
                            @click="submitReply(isActive)"></v-btn>
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
        <v-dialog :width="$vuetify.display.smAndDown?'90%':'50%'" v-model="showDialog">

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
                    <AddressSelect :addressPerPage="$vuetify.display.mdAndUp?3:($vuetify.display.xs?1:2)" :paying="false" :cardElevator="0" :preSelect="false"
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
            <v-col cols="12" class="">
                <v-pagination
                    v-model="currentPage"
                    :length="totalPages"
                    :total-visible="$vuetify.display.smAndUp?5:3"
                ></v-pagination>
                <!--@input="fetchOrders(currentPage)"-->
            </v-col>
        </v-row>
      </v-sheet>
    </v-container>
    
    <v-container v-else class="d-flex justify-center align-center">
        <v-progress-circular style="height: 80vh;" indeterminate color="primary"></v-progress-circular>
    </v-container>
    <product-card
    :product="showedItem" 
    :shop-id="showedShopId"
    :category-list="[]"
    :show="false"
    ref="itemCard"
  ></product-card>

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useDisplay } from 'vuetify';
import { user } from '@/store/user';
import snackbar from '@/api/snackbar';
import { getOrder,getReview, sellerGetOrders, sellerReplyComment, 
    sellerShip, userCancelOrder, userChangeAddress, userConfirmOrder, 
    userCreateReview, userGetOrders, userPayOrders, userRefund } from '@/api/order';
import { getShopInfo } from '@/api/shop';
import router from '@/router';
import { profile } from '@/api/user';
import AddressSelect from '@/components/addressSelect.vue';
import { useRoute } from 'vue-router';
import productCard from '@/components/productCard.vue';
import { getProductDetail } from '@/api/product';

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
const selectedStatus = ref(undefined);

watch(currentPage, (newVal, oldVal) => {
    orderLoading.value = true;
    fetchOrders(newVal, selectedStatus.value);
});
watch(selectedShop, (newVal, oldVal) => {
    if (loading.value === true) {
        return;
    }
    orderLoading.value = true;
    if (currentPage.value !== 1) {
        currentPage.value = 1;
    } else {
        fetchOrders(currentPage.value, selectedStatus.value);
    }
});
watch(selectedStatus, (newVal, oldVal) => {
    if(orderLoading.value === true){
        return;
    } 
    orderLoading.value = true;
    if (currentPage.value !== 1 ){
        currentPage.value = 1;
    }else {
        fetchOrders(currentPage.value, selectedStatus.value);
    } 
});
const route = useRoute();
const queryOrderId = ref(-1);
const queryShopId = ref(-1);
onMounted(() => {
    if (route.query.id) {
        queryOrderId.value = route.query.id;
    }
    if (route.query.shop) {
        queryShopId.value = route.query.shop;
    }
    profile().then(() => {
        
        if (user.role === 'CUSTOMER') {
            loading.value = false;
            isCustomer.value = true;
            isSeller.value = false;
            if (queryOrderId.value === -1) {
                userGetOrders().then(res => {
                    orders.value = res.data.orders;
                    totalPages.value = res.data.total_page;
                    fetchShopInfo(orders.value).then(() => {
                        orderLoading.value = false;
                    });
                }).catch(err => {
                    console.log(err);
                })
            } else {
                getSpecificOrder(queryOrderId.value).then(()=> {
                    fetchShopInfo(orders.value).then(() => {
                        orderLoading.value = false;
                    });
                })
            }
            
        } else {
            isCustomer.value = false;
            isSeller.value = true;
            shopIds.value = user.shops;
            
            if (shopIds.value.length !== 0) {
                fetchShopInfo(shopIds.value).then(() => {
                    
                    sellerShops.value = shopIds.value.map(id => shopInfoCache.value[id]).filter(shop => shop !== undefined);
                    
                    if (queryShopId.value !== -1) {
                        selectedShop.value = sellerShops.value.filter(shop=> shop.id == queryShopId.value)[0].id;
                        getSpecificOrder(queryOrderId.value).then(()=> {
                            orderLoading.value = false;
                            totalPages.value = 1;
                            loading.value=false;
                        })
                    } else {
                        selectedShop.value = shopIds.value[0];
                        sellerGetOrders(selectedShop.value).then(res => {
                            orders.value = res.data.orders;
                            totalPages.value = res.data.total_page;
                            orderLoading.value = false;
                            loading.value = false;
                        }).catch(err => {
                            console.log(err);
                        })
                    }
                    
                });
                
            } else {
                loading.value = false;
                orderLoading.value = false;
            }
        }
    });


})
const getSpecificOrder = async(order_id) => {
    const response = await getOrder(order_id);
    if (response.success) {
        orders.value = [response.data];
        totalPages.value = 1;
    } else if (response.response.data.message === '订单不存在' || 
        response.response.data.message === '您无权查看该订单'
    ) {
        router.push('/order').then(() => {
            router.go(0);
        });
    } else {
        console.log(response.response.data.message);
    }
}

const fetchOrders = async (page, status) => {
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

const itemCard = ref(null);
const showedItem = ref({});
const showedShopId = ref(0);
const showDetail = async(item_id) => {
  const response = await getProductDetail(item_id);
  if (response.success) {
    showedItem.value = response.data;
    showedShopId.value = response.data.shop;
  }
}


const curOrder = ref();
const showReview = ref(false);
const createReview = ref(false);
const replying = ref(false);
const reviewContent = ref('');
const review_id = ref();
const reviewRating = ref(0);
const replyContent = ref('');
const curItem = ref();
const submitReview = async (isActive) => {
    if (reviewRating.value === 0) {
        snackbar.error("请给商品评分");
        return;
    }
    const response = await userCreateReview(curItem.value.id, curItem.value.product.id, reviewRating.value, reviewContent.value);
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
    replying.value = false;
    curOrder.value = order;
    curItem.value = item;
    createReview.value = !item.has_reviewed;
    reviewContent.value = '';
    reviewRating.value = 0;
    alreadyReply.value = false;
    showReview.value = true;
}

const seeReview = async (order, item) => {
    // `/shop/order_item/<int:order_item_id>/review/`
    const response = await getReview(item.id);
    replying.value=false;
    if (response.success) {
        createReview.value = false;
        reviewContent.value = response.data.comment;
        reviewRating.value = response.data.rating;
        alreadyReply.value = response.data.merchant_reply !== null;
        if (alreadyReply.value) {
            replyContent.value = response.data.merchant_reply;
        } else {
            replyContent.value = '';
        }
        showReview.value = true;
        //snackbar.success("评价内容：" + response.data.comment + " 评分：" + response.data.rating);
    } else {
        snackbar.error("获取评价失败：" + response.message);
    }
    //snackbar.info("评价内容：" + item.review.content + " 评分：" + item.review.rating);
}
const alreadyReply = ref(false);
const reply = async(order, item) => {
    curOrder.value = order;
    curItem.value = item;
    const response = await getReview(item.id);
    if (response.success) {
        review_id.value = response.data.id;
        reviewContent.value = response.data.comment;
        reviewRating.value = response.data.rating;
        createReview.value = false;
        if (response.data.merchant_reply !== null) {
            replyContent.value = response.data.merchant_reply;
            alreadyReply.value = true;
        } else {
            replyContent.value = '';
            alreadyReply.value = false;
        }
        // reviewContent.value = item.review.content;
        // reviewRating.value = item.review.rating;
        replying.value = true;
        showReview.value = true;
    } else {
        snackbar.error("获取评价失败：" + response.message);
    }
}

const submitReply = async (isActive) => {
    const response = await sellerReply(review_id.value, replyContent.value);
    if (response.success) {
        snackbar.success("回复成功");
        curItem.value.review_has_reply = true;
        replyContent.value = '';
        isActive.value = false;
    } else {
        console.log(response);
        snackbar.error("回复失败：" + response.message);
    }
}



const showDialog = ref(false);
const dialogContent = ref(''); // pay, change address, receive, cancel!   (refund?)

const orderDialog = (content, order) => {
    dialogContent.value = content;
    curOrder.value = order;
    switch (content) {
        case 'pay':
            profile().then(() => {
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
    const response = await userPayOrders([order.order_id]);
    if (response.success) {
        snackbar.success("支付成功");
        order.status = 'Payment Received';
    } else {
        snackbar.error("支付失败：" + response.data.message);
    }
}

const userCancel = async (order) => {
    const response = await userCancelOrder(order.order_id);
    if (response.success) {
        snackbar.success("订单取消成功");
        order.status = 'Cancelled';
    } else {
        snackbar.error("订单取消失败：" + response.message);
    }
}

const userReceive = async (order) => {
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
    const response = await userChangeAddress(curOrder.value.order_id, selectedAddress.value.id);
    if (response.success) {
        snackbar.success("地址修改成功");
        curOrder.value.address = selectedAddress.value;
    } else {
        snackbar.error("地址修改失败：" + response.message);
    }
});

const ship = async (order) => {
    const response = await sellerShip(order.order_id);
    if (response.success) {
        snackbar.success("发货成功");
        order.status = 'Shipped';
    } else {
        snackbar.error("发货失败：" + response.message);
    }
}


const sellerReply = async (review_id, reply) => {
    const response = await sellerReplyComment(review_id, reply);
    if (response.success) {
        snackbar.success("回复成功");
        
    } else {
        snackbar.error("回复失败：" + response.message);
    }
    return response;
}

const formatStatus = (status) => {
    switch (status) {
        case 'Pending Payment':
            return '待支付';
        case 'Payment Received':
            return xs.value?'待发货':'已支付，待发货';
        case 'Completed':
            return '已完成';
        case 'Cancelled':
            return '已取消';
        case 'Shipped':
            return xs.value?'已发货':'商家已发货';
        default:
            return "";
    }
}

const fetchShopInfo = async (shopIdArray) => {
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
    return shopInfoCache.value[shop_id];
}

const emptyOrderCaption = computed(() => {
    if (isCustomer.value){
        if (selectedStatus.value === undefined || selectedStatus.value === ''){
            return "您还没有下单，快去逛逛吧";
        }
        return "没有符合条件的订单  (筛选条件： " + formatStatus(selectedStatus.value) + ")";
    } else {
        
        if(selectedStatus.value === undefined || selectedStatus.value === ''){
            return "该商铺暂无订单";
        }
        
        return "该商铺暂无符合要求的订单 (筛选条件： " + formatStatus(selectedStatus.value) + ")";
    }
});

function formatDate(dateStr) {
  const date = new Date(dateStr);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hour = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}年${month}月${day}日 ${hour}:${min}:${seconds}`;
}

const { xs, mdAndUp } = useDisplay();
const infoTitleSizeClass = computed(() => xs.value ? 'text-h6' : 'text-h6');


</script>

<style scoped></style>