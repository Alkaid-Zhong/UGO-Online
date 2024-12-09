<template>
  <v-app :theme="theme">
    <v-app-bar title="UGO Online">
      <template v-slot:append>
        <!-- <v-btn icon="mdi-bell" @click="showNotify"> -->
        <v-menu
          
          :close-on-content-click="false"
          location="bottom"
        > 
          <template v-slot:activator="{ props }">
            <v-btn
              icon="mdi-bell"
              v-bind="props"
              @click="reloadMessage"
            ></v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h5">
              通知
            </v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-chip-group filter v-model="selectedNotifyStatus">
                <v-chip :value="true" selected-class="text-success">已读消息</v-chip>
                <v-chip :value="false" selected-class="text-warning">未读消息</v-chip>
              </v-chip-group>
                <v-tooltip
                  text="全部标记为已读"
                  location="bottom"
                >
                  <template  v-slot:activator="{ props }">
                    <v-btn icon="mdi-check-all" v-bind="props">
                    </v-btn>
                  </template>
                </v-tooltip> 

            </v-card-actions>
            
            <v-list>
              <v-list-item v-for="message in messages">
                  <v-list-item-title>{{ message.content }}</v-list-item-title>
                  <v-list-item-subtitle>{{formatDate(message.created_time)}}</v-list-item-subtitle>
              </v-list-item>
              <v-divider></v-divider>
            </v-list>
          </v-card>
        </v-menu>
        <!-- </v-btn> -->
        <v-btn 
          :icon="theme ==='light' ? 'mdi-weather-sunny' :'mdi-weather-night'" 
          @click="toggleTheme"
        ></v-btn>
        
      </template>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
    <v-bottom-navigation>
      <v-btn to="/">
        <v-icon>mdi-home</v-icon>
        <span>主页</span>
      </v-btn>

      <v-btn to="/shop">
        <v-icon>mdi-store</v-icon>
        <span>所有商铺</span>
      </v-btn>

      <v-btn to="/user/cart" v-if="user.login && user.role === 'CUSTOMER'">
        <v-icon>mdi-cart</v-icon>
        <span>购物车</span>
      </v-btn>

      <v-btn to="/order" v-if="user.login"> <!-- 商家和用户都用同一个 -->
        <v-icon>mdi-invoice-text-multiple-outline</v-icon>
        <span>订单</span>
      </v-btn>

      <v-btn to="/user/login" v-if="!user.login">
        <v-icon>mdi-login</v-icon>
        <span>登录</span>
      </v-btn>
      <v-btn to="/user/profile" v-else>
        <v-icon>mdi-account</v-icon>
        <span>个人中心</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
  <v-snackbar
    v-model="snackbar.show"
    :color="snackbar.color"
    :text="snackbar.text"
    :timeout="snackbar.timeout"
  >
    <template #actions>
      <v-btn
        variant="text"
        @click="snackbar.show = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import router from './router';
import { user } from './store/user'
import { snackbar } from './store/app';
import { profile, logout, getMessage, readMessage } from './api/user';
import { useRoute } from 'vue-router';

const route = useRoute();
const theme = ref('dark')
// 检测系统是否处于深色模式
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
// 根据系统深色模式设置主题
const setSystemTheme = () => {
  theme.value = prefersDark.matches ? 'dark' : 'light'
  localStorage.setItem('oo_theme', theme.value)
}
// 监听系统主题的变化
prefersDark.addEventListener('change', setSystemTheme)
const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('oo_theme', theme.value)
}


onMounted(async () => {
  const showSnackbar = route.path !== '/user/login';
  if (localStorage.getItem('oo_theme')) {
    theme.value = localStorage.getItem('oo_theme');
  } else {
    setSystemTheme();
  }
  await profile(showSnackbar);
});

watch(user, async (newVal) => {
  if (newVal.login) {
    if (route.path === '/user/login') {
      router.replace('/user/profile');
    }
  } else {
    router.replace('/user/login');
  }
});

const selectedNotifyStatus = ref(null);
const messages = ref([]);
const reloadMessage = async() => {
  console.log(selectedNotifyStatus.value);
  const response = await getMessage(selectedNotifyStatus.value);
  if (response.success) {
    messages.value = response.data.messages;
    console.log(messages.value);
  } else {
    snackbar.show = true;
    snackbar.text = response.message;
    snackbar.color = 'error';
  }
};

watch(selectedNotifyStatus, (newVal) => {
  console.log(newVal);
  reloadMessage();
});

const formatDate = (dateStr)=> {
  const date = new Date(dateStr);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hour = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}年${month}月${day}日 ${hour}:${min}:${seconds}`;
};

</script>
