"use client";
import { getAllLicenses } from "@/lib/services/licenseService";
import { License } from "@/lib/types/license";
import { useState } from "react";

const LicencesTable: React.FC = () => {
    const[licenses, setLicenses] = useState<License[]>([]);
    const [loading, setLoading] = useState(true);

    
    const fetchMailLogs = async () => {
        const _mailLogs = await getAllLicenses();
        setLicenses(_mailLogs);
        setLoading(false);
    }

    if (loading) {
        fetchMailLogs();
    }

    return (
        <div className="w-full gap-10">
            <table className="table-auto w-full">
                <thead>
                    <tr>
                        <th className="px-4 py-2">License id</th>
                        <th className="px-4 py-2">License Type</th>
                        <th className="px-4 py-2">Package</th>
                        <th className="px-4 py-2">Client</th>
                        <th className="px-4 py-2">Expiration Date</th>
                        <th className="px-4 py-2">Creation Date</th>
                    </tr>
                </thead>
                <tbody>
                    {licenses.map((license, idx) => (
                        <tr key={idx}>
                            <td className="border px-4 py-2">{license.id}</td>
                            <td className="border px-4 py-2">{license.license_type}</td>
                            <td className="border px-4 py-2">{license.package}</td>
                            <td className="border px-4 py-2">{license.client}</td>
                            <td className="border px-4 py-2">{license.expiration_datetime}</td>
                            <td className="border px-4 py-2">{license.created_datetime}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LicencesTable;