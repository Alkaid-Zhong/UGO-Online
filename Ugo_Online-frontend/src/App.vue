<template>
  <v-app :theme="theme">
    <v-app-bar>
      <v-app-bar-title>
        <v-icon class="mr-2">mdi-store</v-icon>
        UGO Online
      </v-app-bar-title>
      <template v-slot:append>
        <!-- <v-btn icon="mdi-bell" @click="showNotify"> -->
        <v-menu
          v-model="showMessage"
          :close-on-content-click="false"
          location="bottom"
        > 
          <template v-slot:activator="{ props }">
            <v-btn
              icon="mdi-bell"
              v-bind="props"
            ></v-btn>
          </template>
          <v-card :min-width="$vuetify.display.smAndDown?'300px' :(minw===0?'420px':minw)" max-width="500px" max-height="400" id="first-card">
            <v-card-title class="text-h5">
              
            </v-card-title>
            <v-card-actions>
              <span class="text-h5 ml-2 font-weight-bold">消息</span>
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
                    <v-btn icon="mdi-check-all" v-bind="props" @click="readAll">
                    </v-btn>
                  </template>
                </v-tooltip> 

            </v-card-actions>
            
            <!-- <v-divider class="mb-0"></v-divider> -->
            <!-- <transition-group mode="out-in"> -->
            <v-list v-if="!messageLoading" key="messages">
              <v-infinite-scroll
                @load="nextPageMessage"
              > <!--height="300"-->
              <template #empty>
                <small v-if="messages.length!==0">到底了...</small>
                
                <v-card-text v-else class="text-center">
                  还没有{{selectedNotifyStatus === undefined? "":(selectedNotifyStatus===true?"已读":"未读")}}消息噢
                </v-card-text>
              </template>
              <v-divider ></v-divider>
                <template v-for="message in messages" :key="message.id">
                  <transition-group name="list" mode="out-in">
                  <v-list-item lines="two" @click="messageClick(message)" :key="message.id" class="customPrepend">
                    <template #prepend >
                      <v-icon :color="message.is_read?'black':'primary'" >mdi-circle-medium</v-icon>
                    </template>
                    <span :class="{'font-weight-bold':!message.is_read}">{{ message.content }}</span>
                    <v-list-item-subtitle>{{formatDate(message.created_time)}}</v-list-item-subtitle>
                    <template #append v-if="message.is_read === false">
                      <v-btn icon="mdi-check" @click.stop="readNotify(message)" class="rounded-0" elevation="0"></v-btn>
                    </template>
                  </v-list-item>
                  <v-divider ></v-divider>
              </transition-group>
                </template>
              </v-infinite-scroll>
              <!-- <transition-group name="list" mode="out-in">
                <div v-for="message in messages" :key="message.id">
                <v-list-item lines="two" @click="messageClick(message)">
                    
                <v-list-item-text>{{ message.content }}</v-list-item-text>
                <v-list-item-subtitle>{{formatDate(message.created_time)}}</v-list-item-subtitle>
                <template #append v-if="message.is_read === false">
                    <v-btn icon="mdi-check" @click.stop="readNotify(message)" class="rounded-0" elevation="0"></v-btn>
                  </template>
                </v-list-item>
                </div>
              </transition-group> -->
            
                
            </v-list>
            <v-skeleton-loader key="messageLoading" boilerplate v-else type="paragraph"></v-skeleton-loader>
            <!-- </transition-group> -->
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
import { profile, logout, getMessage, readMessage, readAllMessage } from './api/user';
import { useRoute } from 'vue-router';
import { id } from 'vuetify/locale';

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

const showMessage = ref(false);
const messageLoading = ref(true);
const selectedNotifyStatus = ref(undefined);
const messages = ref([]);
const minw = ref(0);
const curMessagePage = ref(1);
const maxMessagePages = ref(1);
const messageClick = async(message)=> {
  // console.log(message.order_id);
  if (message.is_read === false) {
    await readNotify(message);
  }
  if (message.order_id !== -1) {
    console.log(route.fullPath);
    if(route.path === '/order' && route.fullPath !== '/order?id='+message.order_id + '&shop='+message.shop_id) {
      router.push({path: `/order`,query:{id:message.order_id, shop:message.shop_id}}).then(() => {
        router.go(0);
      });
    } else {
      router.push({path: `/order`,query:{id:message.order_id, shop:message.shop_id}});
    }
    
  } else if (message.shop_id !== -1) {
    console.log(message.shop_id);
    if (route.fullPath !== '/shop/'+message.shop_id) {
      router.push({path: `/shop/${message.shop_id}`}).then(() => {
        router.go(0);
      });
    } else {
      router.push({path: `/shop/${message.shop_id}`});
    }
  }
}


const reloadMessage = async() => {
  
  const oneNotify = document.getElementById('first-card');
  if (oneNotify!==null) {
    console.log(oneNotify.offsetWidth);
    minw.value = minw.value > oneNotify.offsetWidth ? minw.value: oneNotify.offsetWidth;
  }
  messageLoading.value = true;
  // console.log(selectedNotifyStatus.value);
  const response = await getMessage(selectedNotifyStatus.value);
  if (response.success) {
    messages.value = response.data.messages;
    messageLoading.value = false;
    curMessagePage.value = 1;
    maxMessagePages.value = response.data.total_page;
    // console.log();
    
  } else {
    snackbar.show = true;
    snackbar.text = response.message;
    snackbar.color = 'error';
  }
};

const nextPageMessage = async({ done }) => {

  if (curMessagePage.value >= maxMessagePages.value) {
    done('empty');
    return;
  }
  const response = await getMessage(selectedNotifyStatus.value, curMessagePage.value+1);
  if (response.success) {
    messages.value = messages.value.concat(response.data.messages);
    // messages.value.push(response.data.messages);
    //messageLoading.value = false;
    curMessagePage.value += 1;
    done('ok');
  } else {
    snackbar.show = true;
    snackbar.text = response.message;
    snackbar.color = 'error';
  }
}

watch(selectedNotifyStatus, (newVal) => {
  // console.log(newVal);
  reloadMessage();
});

watch(showMessage, (newVal)=> {
  if (newVal === true) {
    reloadMessage();
  }
})

const readNotify = async(message)=>{
  const res = await readMessage(message.id);
  if (res.success) {
    messages.value = messages.value.filter(tmessage=> tmessage.id !== message.id);
    //message.is_read = true;
  }
}

const readAll = async()=> {
  const res = await readAllMessage();
  if (res.success) {
    if (selectedNotifyStatus.value === false) {

      messages.value = [];
    } else {
      messages.value = messages.value.map(message => {
        message.is_read = true;
        return message;
      });
    }
  }
}

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

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(0);
}

.animate_07s {
  transition: all 0.7s ease-in-out;
}

.customPrepend:deep(.v-list-item__prepend .v-list-item__spacer) {
  width: 16px;
}

</style>