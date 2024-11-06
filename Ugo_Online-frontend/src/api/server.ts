import axios from "axios";

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
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

const post = async (url: string, data?: any): Promise<Response> => {
	try {
		const res = await server.post(url, data)
		return res.data
	} catch (error) {
		console.error(error);
		return {
			success: false,
			...error
		};
	}
};

export default {
	get,
	post,
};