import axios from "axios";
import snackbar from "./snackbar";
import router from "@/router";

interface Response {
	success: boolean;
	code?: number;
	data?: any;
	message?: string;
}

const server = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

const get = async ({ url, params, showSnackbar = true }: { url: string, params?: any, showSnackbar?: boolean }): Promise<Response> => {
	try {
  	const res = await server.get(url, { params })
		return res.data
	} catch (error) {
		errorHandler(error, showSnackbar);
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

const post = async ({url, data , showSnackbar = true}:{url: string, data?: any, showSnackbar?: boolean}): Promise<Response> => {
	let headers = {};
	if (document.cookie.includes('csrftoken=')) {
		headers = { 'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0] }
	}
	try {
		const res = await server.post(
			url, 
			data, 
			{ headers }
		)
		if (!res.data.success) {
			throw new Error(res.data.message);
		}
		return res.data
	} catch (error) {
		errorHandler(error, showSnackbar);
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

const errorHandler = (error: any, showSnackbar = true) => {
	if (error.response) {
		const { code, message } = error.response.data;
		if (showSnackbar) {
			snackbar.error(message);
		}
		if (code === 401) {
			router.push("/user/login");
		}
	} else {
		snackbar.error("Network Error");
	}
}

export default {
	get,
	post,
};