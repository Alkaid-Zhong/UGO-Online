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
