<template>
  <v-app>
    <v-app-bar title="UGO Online">
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
    <v-bottom-navigation>
      <v-btn to="/">
        <v-icon>mdi-home</v-icon>
        <span>主页</span>
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
import { onMounted, watch } from 'vue';
import router from './router';
import { user } from './store/user'
import { snackbar } from './store/app';
import { profile, logout } from './api/user';
import { useRoute } from 'vue-router';


onMounted(async () => {
  const route = useRoute();
  const showSnackbar = route.path !== '/user/login';
  await profile(showSnackbar);
});

watch(user, async (newVal) => {
  if (newVal.login) {
    router.replace('/user/profile');
  } else {
    router.replace('/user/login');
  }
});

</script>
