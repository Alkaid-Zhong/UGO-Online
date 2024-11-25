import server from "./server";

export const createOrder = async (data: any) => {
    const response = await server.post({ url: "/order/create/", data });
    if (response.success) {
        //console.log("创建订单成功");
    } else {
        //console.log("创建订单失败");
    }
    return response;
}

export const userGetOrders = async (page = 1, status?: string) => {
    return await server.get({ url: "/order/user_orders/", showSnackbar: false, params: { page, status } });
}

export const userPayOrders = async (order_ids: Array<Number>) => {
    return await server.post({ url: "/order/pay/", data: { order_ids } });
}

export const userRefund = async (order_id: Number, item_ids: Array<Number>) => {
    return await server.post({
        url: "/order/" + order_id + "/refund/",
        data: { item_ids: item_ids }
    });
}

export const sellerGetOrders = async (page = 1, status?: string) => {
    return await server.get({ url: "/order/seller_orders/", showSnackbar: false, params: { page, status } });
}