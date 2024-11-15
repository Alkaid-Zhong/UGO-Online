<template>
  <v-app :theme="theme">
    <v-app-bar title="UGO Online">
      <template v-slot:append>
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

      <v-btn to="/user/cart" v-if="user.login && user.role === 'CUSTOMER'">
        <v-icon>mdi-cart</v-icon>
        <span>购物车</span>
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
import { profile, logout } from './api/user';
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

</script>
