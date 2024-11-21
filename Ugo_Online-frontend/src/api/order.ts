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