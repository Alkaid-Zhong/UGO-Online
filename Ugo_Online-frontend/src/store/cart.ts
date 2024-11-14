import { reactive } from "vue";


interface CartItem {
    productId: string;
    quantity: number;
    price: number;
}

interface Cart {
    items: CartItem[];
    totalQuantity: number;
    totalPrice: number;
}

export const cart = reactive<Cart>({
    items: [],
    totalQuantity: 0,
    totalPrice: 0
});
