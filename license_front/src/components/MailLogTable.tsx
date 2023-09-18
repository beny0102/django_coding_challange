"use client";
import { getLastMailLogs } from "@/lib/services/mailLogService";
import { MailLog } from "@/lib/types/maillog";
import { useState } from "react";

const MailLogTable: React.FC = () => {
    const [mailLogs, setMailLogs] = useState<MailLog[]>([]);
    const [loading, setLoading] = useState(true);

    const [selectQty, setSelectQty] = useState(10);
    
    const fetchMailLogs = async () => {
        const _mailLogs = await getLastMailLogs(selectQty);
        setMailLogs(_mailLogs);
        setLoading(false);
    }

    if (loading) {
        fetchMailLogs();
    }

    return (
        <div className="w-full gap-10">
            <div className="flex flex-row justify-between">
                <div className="flex flex-row">
                    <label className="flex flex-row items-center">
                        <span className="text-gray-700 dark:text-white">Quantity</span>
                        <select className="form-select block w-full ml-2" defaultValue={25} onChange={(e) => setSelectQty(parseInt(e.target.value))}>
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="25">25</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                        </select>
                    </label>
                    <button className="ml-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => {setMailLogs([]); setSelectQty(selectQty); setLoading(true);}}>Refresh</button>
                </div>
            </div>

            <table className="table-auto w-full">
                <thead>
                    <tr>
                        <th className="px-4 py-2">License id</th>
                        <th className="px-4 py-2">Reason</th>
                        <th className="px-4 py-2">Date</th>
                    </tr>
                </thead>
                <tbody>
                    {mailLogs.map((mailLog, idx) => (
                        <tr key={idx}>
                            <td className="border px-4 py-2">{mailLog.license}</td>
                            <td className="border px-4 py-2">{mailLog.reason}</td>
                            <td className="border px-4 py-2">{mailLog.sent_datetime}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default MailLogTable;