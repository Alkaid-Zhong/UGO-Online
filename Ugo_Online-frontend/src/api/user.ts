import server from "./server";
import { user } from "@/store/user";
import snackbar from "./snackbar";

export const login = async (email: string, password: string) => {
	const response = await server.post({ url: "/user/login/", data: { email, password } });
	if (response.success) {
		const res = await profile();
		if (res.success) {
			snackbar.success(`你好，${res.data.name}`);
		}
	} else {
		user.login = false;
	}
};

export const logout = async () => {
	if (await server.post({ url: "/user/logout/" })) {
		snackbar.success("退出成功");
		user.login = false;
		user.name = "";
		user.email = "";
		user.role = "CUSTOMER";
		user.shops = null;
		user.money = 0;
		user.phone = "";
	} else {
		snackbar.error("退出失败了...");
	}
};

export const registerCustomer = async (name: string, phone: string, email: string, password: string) => {
	return server.post({
		url: "/user/register/customer/",
		data: { name, phone, email, password },
	});
};

export const registerSeller = async (name: string, phone: string, email: string, password: string, businessName: string, businessAddress: string) => {
	return server.post({
		url: "/user/register/seller/",
		data: { name, phone, email, password, businessName, businessAddress }
	});
};

export const profile = async (showSnackbar = true) => {

	const response = await server.get({ url: "/user/profile/", showSnackbar: showSnackbar });
	if (response.success) {
		user.login = true;
		user.name = response.data.name;
		user.email = response.data.email;
		user.role = response.data.role;
		user.shops = response.data.shop;
		user.money = response.data.money;
		user.phone = response.data.phone;
	} else {
		user.login = false;
	}
	return response;
};

export const addMoney = async (money: number) => {
	const response = await server.post({ url: "/user/add-money/", data: { add_money: money } });
	if (response.success) {
		user.money = response.data.money;
		snackbar.success(`充值成功，余额${response.data.money}元`);
	} else {
		snackbar.error("充值失败了...");
	}
	return response;
};

export const getAddresses = async () => {
	return server.get({ url: "/user/address/list/", showSnackbar: false });
}

export const addAddress = async (data: any) => {
	// recipient_name: string, province: string, city: string, address: string, phone: string, is_default: boolean

	console.log(data);
	const response = await server.post({
		url: "/user/address/create/",
		data: data,
	});

	if (response.success) {
		snackbar.success("地址添加成功");
	} else {
		snackbar.error("地址添加失败：" + response.message);
	}
	return response;
}

export const getDefaultAddress = async () => {
	return server.get({ url: "/user/address/default/", showSnackbar: false });
}

export const deleteAddress = async (address_id: number) => {
	const response = await server._delete({ url: "/user/address/" + address_id + "/delete/" });
	if (response.success) {
		snackbar.success("地址删除成功");
	} else {
		snackbar.error("地址删除失败：" + response.message);
	}
	return response;
}

export const updateAddress = async (address_id: number, data: any) => {
	const response = await server.put({
		url: "/user/address/" + address_id + "/update/",
		data: {
			address_id: address_id,
			...data
		}
	});

	if (response.success) {
		snackbar.success("地址更新成功");
	} else {
		snackbar.error("地址更新失败：" + response.message);
	}
	return response;
}

export const changePassword = async (old_password: string, new_password: string) => {
	const response = await server.post({
		url: "/user/change-password/",
		data: {
			old_password,
			password: new_password,
			password_confirm: new_password
		}
	});
	return response;
}

export const getMessage = async (is_read: boolean) => {
	return server.get({ url: "/message/", params: { is_read: is_read } });
}

export const readMessage = async (message_id: number) => {
	return server.post({ url: "/message/" + message_id + "/" });
}