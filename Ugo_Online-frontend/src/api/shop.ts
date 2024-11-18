import server from "./server";

export const createShop = async (data: { name: string, address?: string, description?: string}) => {
    return await server.post({
        url: "/shop/create/",
        data
    });
}

interface IShops {
    count: number;
    shops: IShop[];
    total_count: number;
    total_page: number;
    cur_page: number;
}

interface IShop {
    id: number;
    name: string;
    address: string;
    description: string;
    create_date: string;
    sellers: {
        name: string;
        email: string;
        role: string;
    }[];
}

export const getShops = async (page: number = 1) => {
    const res = await server.get({
        url: `/shop/`,
        params: { page }
    });
    return res.data as IShops;
}

export const getShopInfo = async (id: number) => {
    const res = await server.get({
        url: `/shop/${id}/info/`
    });
    return res.data as IShop;
}