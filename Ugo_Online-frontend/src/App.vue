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
</template>

<script setup>
import { onMounted } from 'vue';
import { user } from './store/user'
import { profile, logout } from './api/user';

onMounted(async () => {
  await profile();
});

</script>
