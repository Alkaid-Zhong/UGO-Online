import server from "./server";

export const addProduct = async (
    shopId: number,
    data: {
        name: string;
        description: string;
        price: number;
        category: number;
        stock_quantity: number;
        image: File;
    }
) => {
    return server.post({
        url: `/shop/${shopId}/product/add/`,
        data,
        headers: {
            "Content-Type": "multipart/form-data"
        }
    });
};

export const updateProduct = async (
    shopId: number,
    data: {
        name: string;
        description: string;
        price: number;
        category: number;
        stock_quantity: number;
        image: File;
    }
) => {
    return server.put({
        url: `/shop/${shopId}/product/update/`,
        data,
        headers: {
            "Content-Type": "multipart/form-data"
        }
    });
};

export const getCategories = async () => {
    return await server.get({
        url: "/shop/category_list/",
    });
}

export const getShopCategories = async (shopId: number) => {
    return await server.get({
        url: `/shop/${shopId}/category_list/`,
    });
}

export const getProductList = async (
    shopId: number,
    params: {
        page: number;
        category: number;
        price__gte: number;
        price__lte: number;
    } = {page: 1, category: null, price__gte: null, price__lte: null}
) => { 
    return (await server.get({
        url: `/shop/${shopId}/products/`,
        params
    })).data;
};

export const getProductDetail = async (id: number) => {
    return await server.get({
        url: "/shop/product/" + id + "/",
    });
}