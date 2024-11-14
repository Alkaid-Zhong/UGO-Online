import server from "./server";
import { user } from "@/store/user";
import { cart } from "@/store/cart";
import snackbar from "./snackbar";

export const getCart = async () => {


    const response = await server.get({ url: "/cart/" });
    //console.log("cart info:", response);
    if (response.success) {
        //console.log("获取购物车成功");
    } else {
        //console.log("获取购物车失败");
    }
    return response;
}

export const addToCart = async (productId: string, quantity: number) => {
    const response = await server.post({ url: "/cart/add/", data: { productId, quantity } });
    if (response.success) {
        //console.log("添加购物车成功");
    } else {
        //console.log("添加购物车失败");
    }
    return response;
}

export const updateCart = async (itemId: string, quantity: number) => {

    const response = await server.put({ showSnackbar: false, url: "/cart/update/", data: { itemId, quantity } });
    if (response.success) {
        //console.log("更新购物车成功");
    } else {
        //console.log("更新购物车失败");
    }
    return response;
}

export const deleteItem = async (itemId: string) => {
    const response = await server._delete({ showSnackbar: false, url: "/cart/delete/", data: { itemId } });
    if (response.success) {
        //console.log("删除商品成功");
    } else {
        //console.log("删除商品失败");
    }
    return response;
}