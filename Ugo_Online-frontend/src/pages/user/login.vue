<template>
  <v-container>
    <v-sheet
      class="pa-6 rounded-lg mx-auto"
      elevation="2"
      :style="{ marginTop: register ? 'calc((100vh - 638px) / 3)' : 'calc((100vh - 388px) / 3)', transition: 'all 0.3s ease-in-out' }"
      max-width="500"
    >
      <h2 class="headline mb-4">{{ register? `注册成为${registerRole === 'CUSTOMER' ? '顾客' : '商家'}` : '登录' }}</h2>
      <v-form>
        <v-expand-transition>
          <v-text-field
            v-show="register"
            label="用户名"
            v-model="name"
            required
            type="username"
          ></v-text-field>
        </v-expand-transition>
        <v-expand-transition>
          <v-text-field
            v-show="register"
            label="电话号码"
            v-model="phone"
            required
            type="tel"
          ></v-text-field>
        </v-expand-transition>
        <v-text-field
          label="邮箱"
          v-model="email"
          required
          type="email"
          name="email"
          autocomplete="email"
        ></v-text-field>
        <v-text-field
          label="密码"
          v-model="password"
          type="password"
          name="password"
          required
          autocomplete="password"
        ></v-text-field>
        <v-expand-transition>
          <v-text-field
            v-show="register"
            label="确认密码"
            v-model="passwordConfirm"
            type="password"
            required
          ></v-text-field>
        </v-expand-transition>
        <v-expand-transition>
          <v-row
            class="mb-4"
            v-show="register"
          >
            <v-col cols="6">
              <v-btn
                block
                :color="registerRole === 'CUSTOMER' ? 'green' : ''"
                @click="registerRole = 'CUSTOMER'"
                :prepend-icon="registerRole === 'CUSTOMER' ? 'mdi-checkbox-marked-circle-outline' : ''"
              >我要成为顾客</v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn
                block
                :color="registerRole === 'SELLER' ? 'green' : ''"
                @click="registerRole = 'SELLER'"
                :prepend-icon="registerRole === 'SELLER' ? 'mdi-checkbox-marked-circle-outline' : ''"
              >我要成为商家
              </v-btn>
            </v-col>
          </v-row>
        </v-expand-transition>
        <v-btn
          v-show="!register"
          color="primary"
          @click="submitLogin"
          :loading="loading"
        >登录</v-btn>
        <v-btn
          v-show="register"
          color="primary"
          @click="submitRegister"
          :loading="loading"
        >注册并登录</v-btn>
        <v-btn
          class="ml-4"
          @click="register = !register"
          :disabled="loading"
        >{{ register ? '已有账号？去登录' : '还没有账号？去注册' }}</v-btn>
      </v-form>
    </v-sheet>
  </v-container>
</template>
<script setup>
import { ref } from 'vue'
import { login, registerCustomer, registerSeller } from '@/api/user'
import snackbar from '@/api/snackbar';
import { ca } from 'vuetify/locale';

const name = ref('')
const phone = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')

const register = ref(false)
const registerRole = ref('CUSTOMER')

const loading = ref(false)

const submitLogin = async () => {
  loading.value = true
  await login(email.value, password.value)
  loading.value = false
}
const submitRegister = async () => {
  if (name.value.trim() === '') {
    snackbar.error('用户名不能为空')
    return
  }
  if (phone.value.trim() === '') {
    snackbar.error('电话号码不能为空')
    return
  }
  if (email.value.trim() === '') {
    snackbar.error('邮箱不能为空')
    return
  }
  if (password.value.trim() === '') {
    snackbar.error('密码不能为空')
    return
  }
  if (password.value !== passwordConfirm.value) {
    snackbar.error('两次输入的密码不一致')
    return
  }
  loading.value = true
  if (registerRole.value === 'CUSTOMER') {
    if ((await registerCustomer(name.value, phone.value, email.value, password.value)).success) {
      await login(email.value, password.value)
    }
  } else {
    if ((await registerSeller(name.value, phone.value, email.value, password.value)).success) {
      await login(email.value, password.value)
    }
  }
  loading.value = false
}
</script>