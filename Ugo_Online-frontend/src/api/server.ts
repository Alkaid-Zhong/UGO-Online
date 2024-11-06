import axios from "axios";
import snackbar from "./snackbar";

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

const get = async (url: string, params?: any): Promise<Response> => {
	try {
  	const res = await server.get(url, { params })
		return res.data
	} catch (error) {
		errorHandler(error);
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

const post = async (url: string, data?: any): Promise<Response> => {
	try {
		const res = await server.post(
			url, 
			data, 
			{ headers: { 'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0] } }
		)
		if (!res.data.success) {
			throw new Error(res.data.message);
		}
		return res.data
	} catch (error) {
		errorHandler(error);
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

const errorHandler = (error: any) => {
	if (error.response) {
		const { code, message } = error.response.data;
		snackbar.error(message);
	} else {
		snackbar.error("Network Error");
	}
}

export default {
	get,
	post,
};