<template>
 <v-container v-if="!loading">
    <h1>Welcome to Ugo Online</h1>
    <transition name="ease">
    <v-card v-if="showLatestUpdate" key="'latest update'">
      <v-card-title class="text-h6">Latest update</v-card-title>
      <v-card-subtitle>最近更新时间： 12.04 16:00</v-card-subtitle>
      <v-list>
         <v-list-item>
               <v-list-item-title>1. 新增订单评价和简易查看</v-list-item-title>
         </v-list-item>
         <v-list-item>
               <v-list-item-title>2. 支持地址管理——修改和删除 </v-list-item-title>
         </v-list-item>
         <v-list-item>
               <v-list-item-title>3. 支持商家管理多个商铺 </v-list-item-title>
         </v-list-item>
      </v-list>
      <v-card-text class="text-body-1">
         TODO:
      </v-card-text>
      <v-list>
         <v-list-item>
               <strong>已知Bug：</strong> Profile页面 商家充值ban掉，商铺页面“编辑商品”只对该商铺管理者可见（而非所有Seller）
         </v-list-item>
         <v-list-item>
               <strong>完全没写：</strong>商品页、首页，消息系统
         </v-list-item>
         <v-list-item>
               <strong>正在完善：</strong> 商家订单页面：地址信息显示;订单状况筛选； 高亮样式：待付款（用户）& 待发货（商家） 购物车失效商品样式（UUQ）；<br/>
         </v-list-item>
      </v-list>
      <v-card-actions>
         <v-spacer></v-spacer>
         <v-btn><a class="text-decoration-none" style="color:red" href="mailto:liboqiao2004@buaa.edu.cn?subject=UGO Online bug反馈">bug反馈</a></v-btn>
         <v-btn color="success" @click="showLatestUpdate = false">知道了</v-btn>
      </v-card-actions>
    </v-card>
   </transition>
 </v-container>
</template>

<script setup>
import snackbar from '@/api/snackbar';
import { onMounted,ref } from 'vue';

const showLatestUpdate = ref(true);
const loading = ref(true);
onMounted(() => {
  loading.value = false;
});
</script>

<style scoped>
.ease-enter-active,
.ease-leave-active {
  transition: all 0.5s ease;
}
.ease-enter-from,
.ease-leave-to {
  opacity: 0;
  transform: translateX(0);
}

</style>