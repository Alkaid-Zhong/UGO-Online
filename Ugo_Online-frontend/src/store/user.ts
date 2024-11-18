import { reactive } from "vue";

interface User {
    login: boolean;
    name: string;
    email: string;
    role: 'CUSTOMER' | 'SELLER'
    shopId: number
}

export const user = reactive<User>({
    login: false,
    name: '',
    email: '',
    role: 'CUSTOMER',
    shopId: null,
})