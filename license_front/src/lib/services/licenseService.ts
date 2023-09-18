import api from "@/api/Api";
import { License } from "../types/license";

const getAllLicenses = async () => {
    const response = await api.get<License[]>("/licenses/");
    return response.data;
}

const getLicense = async (id: number) => {
    const response = await api.get<License>(`/licenses/${id}`);
    return response.data;
}

export {
    getAllLicenses,
    getLicense
}