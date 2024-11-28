<template>
<v-card>

<v-card-title>
    <h3>{{ paying ? "地址信息" : "选择地址" }}</h3>
    <template v-slot:prepend>
        <v-icon v-if="paying" @click="editAddress">mdi-pencil</v-icon>
    </template>
</v-card-title>

<v-divider></v-divider>
<v-card-text>
    <transition name="fade" mode="out-in">
    <v-row v-if="!paying" class="" key="'empty'">
        <!--@click="updateAddress"-->
        <v-item-group :value="selectedAddress"  mandatory class="d-flex" style="flex-grow: 1;">
            <v-container>
                <v-row :style="{flexGrow:1, minHeight:minheight+'px' }" id="address-card" >
                    <v-col cols="4" style="flex-grow: 1;" v-for="address in paginatedAddresses" :key="address.id" > 
                        <v-item v-slot="{ isSelected, toggle }" :value="address">

                            <v-card :class="[ { ['bg-primary']: isSelected }]" @click="toggle" height="100%">
                                <v-card-text>
                                <div>
                                    <div><small>{{ address.recipient_name }} {{ address.phone }}</small></div>
                                    <div><small>{{ address.province }} {{ address.city }}</small></div>
                                    <div class="font-weight-bold text-lg">{{ address.address }}</div>
                                </div>
                                </v-card-text>
                            </v-card>
                        </v-item>
                    </v-col>
                    <v-col cols="4" v-if="isLastPage" :key="'empty'">
                        <v-dialog width="40%">
                        <template v-slot:activator="{props:activatorProps}">
                            <v-card v-bind="activatorProps" height="100%" class="d-flex align-center justify-center">
                            <v-card-text>
                                <div class="text-center">
                                
                                <v-icon>mdi-plus</v-icon>
                                <div>添加新地址</div>
                                
                                </div>
                            </v-card-text>
                            </v-card>
            
                        </template>

                        <template v-slot:default="{ isActive }">
                            <v-card title="新建地址">
                            <v-card-actions>
                                <v-form style="width: 100%;">
                                <v-text-field width="100%"
                                    v-model="newAddress.recipient_name"
                                    label="收件人姓名"
                                    prepend-inner-icon="mdi-account"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="newAddress.phone"
                                    label="电话"
                                    prepend-inner-icon="mdi-phone"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="newAddress.province"
                                    label="省份"
                                    prepend-inner-icon="mdi-map-marker-minus-outline"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="newAddress.city"

                                    prepend-inner-icon="mdi-map-marker"
                                    label="城市"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="newAddress.address"
                                    label="具体地址"
                                    prepend-inner-icon="mdi-home"
                                    required
                                ></v-text-field>
                                <v-radio-group v-model="newAddress.is_default" row>
                                    <v-radio label="设为默认地址" :value="true"></v-radio>
                                    <v-radio label="不设为默认地址" :value="false"></v-radio>
                                </v-radio-group>
                                </v-form>
                            </v-card-actions>

                            <v-card-actions>
                                <v-spacer></v-spacer>

                                <v-btn
                                text="取消"
                                @click="isActive.value = false"
                                ></v-btn>
                                <v-btn color="primary" text="添加" @click="createAddress(isActive)">

                                </v-btn>
                            </v-card-actions>
                            </v-card>
                        </template>
                        </v-dialog>
                    </v-col>

                <v-spacer></v-spacer>
                </v-row>
            </v-container>
        </v-item-group>
    </v-row>
    <v-row v-else class="" key="'empty1'">
        <v-col cols="12">
            <div  class="text-body-1">
                <div><strong>收件人姓名:</strong> {{ selectedAddress.recipient_name }}</div>
                <div><strong>电话:</strong> {{ selectedAddress.phone }}</div>
                <div><strong>省份:</strong> {{ selectedAddress.province }}</div>
                <div><strong>城市:</strong> {{ selectedAddress.city }}</div>
                <div><strong>具体地址:</strong> {{ selectedAddress.address }}</div>
            </div>
        </v-col>
    </v-row>
    </transition>
</v-card-text>
<v-card-actions class="animate_07s" v-if="!paying" key="'empty'">
    <v-spacer></v-spacer>
    <v-btn @click="prevPage" :disabled="currentPage <= 0">上一页</v-btn>
    <v-btn @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</v-btn>
</v-card-actions>
</v-card>

</template>

<script setup>
import { getAddresses, addAddress } from '@/api/user';
import { ref, onMounted, computed, watch } from 'vue';
import snackbar from '@/api/snackbar';



const props = defineProps(['paying', 'addressPerPage'])
const emit = defineEmits(['updateSelectedAddress']);

onMounted(() => {
    fetchAddresses();
});

// const updateAddress = (newAddress) => {
//     console.log("inside update to:");
//     console.log(selectedAddress.value);
//     // selectedAddress.value = newAddress;
//     emit('updateSelectedAddress', selectedAddress.value);
// };

watch(() => props.paying, (newVal) => {
    paying.value = newVal;
});

watch(() => props.addressPerPage, (newVal) => {
    addressPerPage.value = newVal;
});




// const addressPerPage = 3;
const paying = ref(props.paying);
const addressPerPage = ref(props.addressPerPage);
// const { paying, userid, addressPerPage } = props
const addresses = ref([]);
const selectedAddress = ref({

});
const newAddress = ref({
    recipient_name: '',
    phone: '',
    province: '',
    city: '',
    address: '',
    is_default: false
});
const currentPage = ref(0);

watch(() => selectedAddress.value, (newVal) => {
    console.log("selected address changed");
    console.log(newVal);
    emit('updateSelectedAddress', newVal);
});

const createAddress = async (isActive) => {
    console.log("newAddr");
  console.log(newAddress.value);
    const response = await addAddress(newAddress.value);
    if (response.success) {
        snackbar.success("添加成功");
        isActive.value = false;
        fetchAddresses().then(() => {
            if (newAddress.value.is_default) {
                currentPage.value = 0;
                //console.log("新增默认地址");
                //console.log(paginatedAddresses.value[0]===selectedAddress.value);
            } else {
                selectedAddress.value = newAddress.value;
            }
        });
        
    } else {
        snackbar.error("添加失败");
    }
};


const isLastPage = computed(() => {
    return currentPage.value === totalPages.value - 1;
});

const paginatedAddresses = computed(() => {
    const start = currentPage.value * addressPerPage.value;
    const end = start + addressPerPage.value;
    // console.log(addresses.value);
    return addresses.value.slice(start, end);
});

const minheight = ref(0);
const transitionName = ref('slide-left');

const nextPage = () => {
  transitionName.value = 'slide-right';
  const firstAddressCard = document.getElementById('address-card');
  if (firstAddressCard) {
    minheight.value = firstAddressCard.offsetHeight;
    console.log("success", minheight.value);
  }
//   const tmp = currentPage.value*addressPerPage
//   console.log(addresses.value.slice());
  currentPage.value++;
};

const prevPage = () => {
  transitionName.value = 'slide-left';
  currentPage.value--;
};

const totalPages = computed(() => {
    return Math.ceil((addresses.value.length + 1) / addressPerPage.value);
});

const fetchAddresses = async () => {
  const response = await getAddresses();
  console.log(addresses.value.length, response.data.length);
  addresses.value = response.data;
  if (addresses.value.length !== 0) {
    console.log("hey: " + addresses.value);
    selectedAddress.value = addresses.value[0];
    console.log(selectedAddress.value);
    console.log("total pages:", addresses.value.length);
    // emit('updateSelectedAddress', selectedAddress.value);
  }
};


</script>

<style scoped>
.slide-left-enter-active, .slide-left-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}
.slide-left-enter, .slide-left-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.slide-right-enter-active, .slide-right-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}
.slide-right-enter, .slide-right-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.animate_07s {
  transition: all 0.7s ease-in-out;
}
</style>