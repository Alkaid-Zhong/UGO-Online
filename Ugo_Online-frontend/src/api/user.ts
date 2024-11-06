import server from "./server";
import { user } from "@/store/user";
import snackbar from "./snackbar";

export const login = async (email: string, password: string) => {
  const response = await server.post("/user/login", { email, password });
	if (response.success) {
		const res = await profile();
		if (res.success) {
			snackbar.success(`Welcome ${res.data.name}!`)
		}
	} else {
		user.login = false;
	}
};

export const logout = async () => {
  if(await server.post("/user/logout")) {
		snackbar.success("退出成功!");
		user.login = false;
		user.name = "";
		user.email = "";
		user.role = "CUSTOMER";
	} else {
		snackbar.error("退出失败了...");
	}
};

export const registerCustomer = async (name: string, phone: string, email: string, password: string) => {
  return server.post("/user/register/customer", { name, phone, email, password });
};

export const registerSeller = async (name: string, phone: string, email: string, password: string, businessName: string, businessAddress: string) => {
  return server.post("/user/register/seller", { name, phone, email, password, businessName, businessAddress });
};

export const profile = async () => {
	const response = await server.get("/user/profile");
	if (response.success) {
		user.login = true;
		user.name = response.data.name;
		user.email = response.data.email;
		user.role = response.data.role;
	} else {
		user.login = false;
	}
	return response;
};