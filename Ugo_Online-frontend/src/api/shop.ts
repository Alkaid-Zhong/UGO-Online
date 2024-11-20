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

interface IInviteInfo {
    code: string;
    shop: number;
    creater: number;
    is_active: boolean;
    created_at: string;
    expires_at: string;
    usage_limit: number;
    usage_count: number;
}

export const getInviteCode = async (
    id: number, 
    params: { expires_in_days?: number, usage_limit?: number } = {expires_in_days: null, usage_limit: 1}
) => {
    const res = await server.post({
        url: `/shop/${id}/create_invitation_code/`,
        data: params.expires_in_days ? {
            expires_in_days: params.expires_in_days, 
            usage_limit: params.usage_limit
        } : {
            usage_limit: params.usage_limit
        }
    });
    return {
        ...res,
        data: res.data as IInviteInfo
    }
}