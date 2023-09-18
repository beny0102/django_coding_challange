import api from "@/api/Api";
import { MailLog } from "../types/maillog";

const getLastMailLogs = async (qty: number) => {
    const response = await api.get<MailLog[]>(`/maillogs/${qty}/`);
    return response.data;
}


export {
    getLastMailLogs
}