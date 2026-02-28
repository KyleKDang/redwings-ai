import axios from "axios"

export async function getDataFromBackend(route, paramsInit) {
    const params = new URLSearchParams(paramsInit);
	const {data} = await axios.get(`/api/${route}?${params}`);

	return data;
}