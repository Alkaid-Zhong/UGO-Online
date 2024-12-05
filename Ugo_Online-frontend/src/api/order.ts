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

export const userChangeAddress = async (order_id: Number, address_id: Number) => {
    return await server.post({ url: "/order/" + order_id + "/update_address/", data: { address_id } });
}

export const userCancelOrder = async (order_id: Number) => {
    return await server.post({ url: "/order/" + order_id + "/cancel/" });
}

export const userConfirmOrder = async (order_id: Number) => {
    return await server.post({ url: "/order/" + order_id + "/complete/" });
}

export const userRefund = async (order_id: Number, item_ids: Array<Number>) => {
    return await server.post({
        url: "/order/" + order_id + "/refund/",
        data: { item_ids: item_ids }
    });
}

export const userCreateReview = async (order: Number, product: Number, rating: Number, comment: string) => {
    return await server.post({
        url: "/shop/review/create/",
        data: { order, product, rating, comment }
    });
}

export const getReview = async (order_item_id: Number) => {
    // `/shop/order_item/<int:order_item_id>/review/`
    return await server.get({ url: "/shop/order_item/" + order_item_id + "/review/" });
}

export const sellerGetOrders = async (shop_id: number, page = 1, status?: string) => {
    return await server.get({ url: "/order/seller_orders/" + shop_id + '/', showSnackbar: false, params: { page, status } });
}

export const sellerShip = async (order_id: Number) => {
    return await server.post({ url: "/order/" + order_id + "/ship/" });
}