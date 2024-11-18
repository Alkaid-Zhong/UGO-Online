import server from "./server";

const addProduct = (
    shopId: number, 
    data: {
        name: string;
        description: string;
        price: number;
        category: number;
        stock_quantity: number;
        image: string;
    }
) => {
    return server.post({
        url: `shop/${shopId}/product/add`,
        data,
    });
};
