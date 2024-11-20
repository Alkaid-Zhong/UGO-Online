import { reactive, ref, Ref } from "vue";


interface CartItem {
    productId: string;
    quantity: number;
    price: number;
}

interface Cart {
    items: CartItem[];
    selectedItems: CartItem[];
    totalSum: number;
    discount: number;
    actualSum: number;
}

export const cart = reactive<Cart>({
    items: [],
    selectedItems: [],
    totalSum: 0,
    discount: 0,
    actualSum: 0
});
