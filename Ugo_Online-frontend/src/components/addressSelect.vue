<template>
<v-card :elevation="cardElevator">

    <template #title>
        <h3>{{ !paying?title:'确认地址信息' }}</h3>

    </template>
    <template #append v-if="editable && !paying">
        <v-icon @click="showDialog('修改')"> mdi-pencil</v-icon>
        <v-icon @click="showDialog('添加')"> mdi-plus</v-icon>
    </template>

<v-divider></v-divider>
<v-card-text>
    <transition name="fade" mode="out-in">
    <v-row v-if="!paying" class="" key="'empty'">
        <!--@click="updateAddress"-->
        <v-skeleton-loader
            v-if="loading"
            type="card"
            class="mx-auto"
            width="100%"
        ></v-skeleton-loader>
        <v-item-group v-else v-model="selectedAddress"  :mandatory="mandatory" class="d-flex" style="flex-grow: 1;">
            <v-container>
                <v-row :style="{flexGrow:1, minHeight:minheight+'px' }" id="address-card" >
                    <v-col :cols="12/addressPerPage" style="flex-grow: 1;" v-for="address in paginatedAddresses" :key="address.id" > 
                        <v-item v-slot="{ isSelected, toggle }" :value="address">
                            
                            <v-card :class="[ { ['bg-primary']: isSelected }]" @click="toggle" height="100%">
                                <v-card-text>
                                    <v-row>
                                    <v-col cols="10">
                                    <div>
                                        <div><small>{{ address.recipient_name }} {{ address.phone }} 
                                                    
                                            </small>
                                            
                                        </div>
                                        <div><small>{{ address.province }} {{ address.city }}</small></div>
                                        <div class="font-weight-bold text-lg">{{ address.address }}</div>
                                    </div>
                                    </v-col>
                                    <v-col cols="2">
                                        <v-badge color="green" content="默认" v-if="address.is_default">
                                            
                                        </v-badge>
                                    </v-col>
                                </v-row>
                                </v-card-text>
                            </v-card>
                            
                        </v-item>
                    </v-col>
                    <v-col :cols="12/addressPerPage" v-if="isLastPage" :key="'empty'">
                        <v-card @click="showDialog('添加')" height="100%" class="d-flex align-center justify-center">
                            <v-card-text>
                                <div class="text-center">
                                
                                <v-icon>mdi-plus</v-icon>
                                <div>添加新地址</div>
                                
                                </div>
                            </v-card-text>
                        </v-card>

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
<v-card-actions class="animate_07s" v-if="!paying && !loading" key="'empty'" >
    <v-spacer></v-spacer>
    <v-btn @click="prevPage" :disabled="currentPage <= 0">上一页</v-btn>
    <v-btn @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</v-btn>
</v-card-actions>
</v-card>

<v-dialog v-model="showAddAddress" :width="$vuetify.display.smAndUp?'45%':'90%'">
    <!-- <template v-slot:activator="{props:activatorProps}">
        <v-card v-bind="activatorProps" height="100%" class="d-flex align-center justify-center">
        <v-card-text>
            <div class="text-center">
            
            <v-icon>mdi-plus</v-icon>
            <div>添加新地址</div>
            
            </div>
        </v-card-text>
        </v-card>

    </template> -->

    <template v-slot:default="{ isActive }">
        <v-card :title="showFor ==='添加'? '新建地址':'编辑地址'">
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
            <v-btn text="删除" color="error" @click="deleteAddr()"></v-btn>
            <v-btn color="primary" :text="showFor" @click="submitAddress(isActive)">

            </v-btn>
        </v-card-actions>
        </v-card>
    </template>
    </v-dialog>
</template>

<script setup>
import { getAddresses, addAddress, updateAddress, deleteAddress } from '@/api/user';
import { ref, onMounted, computed, watch } from 'vue';
import snackbar from '@/api/snackbar';



const props = defineProps(['paying', 'addressPerPage','title','cardElevator','preSelect', 'mandatory','editable']);
const emit = defineEmits(['updateSelectedAddress']);

onMounted(() => {
    fetchAddresses();
    //console.log($vuetify.display.mdAndUp);
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


const showFor = ref(''); // 添加 or 修改
const editable = props.editable !== undefined ? ref(props.editable): ref(true);
const showAddAddress = ref(false);
// const addressPerPage = 3;
const paying = ref(props.paying);
const mandatory = props.mandatory !== undefined ? ref(props.mandatory) : ref(true);
const title = ref(props.title);
const addressPerPage = ref(props.addressPerPage);
const cardElevator = props.cardElevator !== undefined ? ref(props.cardElevator) : 1;
const preSelect = props.preSelect !== undefined ? ref(props.preSelect) : ref(true);
// const { paying, userid, addressPerPage } = props
const addresses = ref([]);
const selectedAddress = ref({});
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
    emit('updateSelectedAddress', newVal);
});

const submitAddress = (isActive) => {
    if(showFor.value === '添加') {
        createAddress(isActive);
    } else {
        // showFor.value = '修改';
        editAddress(isActive);
    }
};

const deleteAddr = async () => {
    const response = await deleteAddress(selectedAddress.value.id);
    if (response.success) {
        snackbar.success("删除成功");
        fetchAddresses().then(() => {
            console.log(mandatory.value);
            selectedAddress.value = mandatory.value ? addresses.value[0] : null;
        });
    } else {
        snackbar.error("删除失败");
    }
};

const curAddrId = ref(0);
const showDialog = (use) => {
    // console.log("editAddr");
    // console.log(selectedAddress.value);
    showFor.value = use;
    if (use ==='修改') {
        if (selectedAddress.value === undefined || selectedAddress.value.id === undefined) {
            snackbar.error("请先选择一个地址");
            return;
        }
        curAddrId.value = selectedAddress.value.id;
        newAddress.value = {
            recipient_name: selectedAddress.value.recipient_name,
            phone: selectedAddress.value.phone,
            province: selectedAddress.value.province,
            city: selectedAddress.value.city,
            address: selectedAddress.value.address,
            is_default: selectedAddress.value.is_default
        };
    } else {
        newAddress.value = {
            recipient_name: '',
            phone: '',
            province: '',
            city: '',
            address: '',
            is_default: false
        };
    }
    
    showAddAddress.value = true;
};

const editAddress = async (isActive) => {
    // console.log("editAddr");
    // console.log(newAddress.value);
    const response = await updateAddress(curAddrId.value, newAddress.value);
    if (response.success) {
        snackbar.success("修改成功");
        newAddress.value = {
            recipient_name: '',
            phone: '',
            province: '',
            city: '',
            address: '',
            is_default: false
        };
        isActive.value = false;
        fetchAddresses().then(() => {
            selectedAddress.value = response.data;
        });
    } else {
        snackbar.error("修改失败");
    }
};

const createAddress = async (isActive) => {
    // console.log("newAddr");
    // console.log(newAddress.value);
    const response = await addAddress(newAddress.value);
    if (response.success) {
        snackbar.success("添加成功");
        newAddress.value = {
            recipient_name: '',
            phone: '',
            province: '',
            city: '',
            address: '',
            is_default: false
        };
        isActive.value = false;
        fetchAddresses().then(() => {
            if (newAddress.value.is_default) {
                currentPage.value = 0;
            } else {
                selectedAddress.value = response.data;
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
const loading = ref(true);
const minheight = ref(0);
const transitionName = ref('slide-left');

const nextPage = () => {
  transitionName.value = 'slide-right';
  const firstAddressCard = document.getElementById('address-card');
  if (firstAddressCard) {
    minheight.value = firstAddressCard.offsetHeight;
    // console.log("success", minheight.value);
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
//   console.log(addresses.value.length, response.data.length);
  addresses.value = response.data;
  if (addresses.value.length !== 0) {
    // console.log("hey: " + addresses.value);
    if (preSelect.value) {
        console.log(preSelect.value);
        console.warn(props.preSelect === undefined);
        selectedAddress.value = addresses.value[0];
    } else {

    }
    //selectedAddress.value = addresses.value[0];
    // console.log(selectedAddress.value);
    // console.log("total pages:", addresses.value.length);
    // emit('updateSelectedAddress', selectedAddress.value);
  }
  loading.value = false;
};

const dynamicWidth = computed(() => {
    switch ($vuetify.breakpoint.name) {
    case 'xs': return '90%';
    case 'sm': return '90%';
    case 'md': return '90%';
    case 'lg': return '40%';
    case 'xl': return '40%';
    }
});

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