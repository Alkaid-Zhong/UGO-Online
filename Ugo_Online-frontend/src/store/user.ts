import { reactive } from "vue";

interface User {
    login: boolean;
    name: string;
    email: string;
    role: 'CUSTOMER' | 'SELLER' | null
    shops: number[]
    money: number
    phone: string
}

export const user = reactive<User>({
    login: false,
    name: '',
    email: '',
    role: null,
    shops: [],
    money: 0,
    phone: ''
})