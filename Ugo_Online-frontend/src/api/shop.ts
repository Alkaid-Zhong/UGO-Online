import { options } from "node_modules/axios/index.cjs";
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

export const joinShop = async (code: string) => {
    return await server.post({
        url: `/shop/join_by_code/`,
        data: { invitation_code: code }
    });
}

export const getShopFlow = async (
    id: number,
    options: {
        page: number, transaction_type?: 'Income' | 'Refund', date?: string, ordering?: 'data' | 'amount' | '-data' | '-amount'
    } = { page: 1 }
) => {
    return await server.get({
        url: `/shop/${id}/transactions/`,
        params: {
            page: options.page,
            transaction_type: options.transaction_type,
            date: options.date,
            ordering: options.ordering
        }
    });
}

export const splitToSeller = async (shop_id: number, given_id: number, money: number) => {
    return await server.post({
        url: `/shop/${shop_id}/split/`,    
        data: { given_id, money }
    });
}