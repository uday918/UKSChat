import React, { useEffect, useState } from "react";
import { adminGetPayments } from "../api";

export default function Billing() {
    const [payments, setPayments] = useState([]);

    useEffect(() => {
        (async () => {
            const data = await adminGetPayments();
            const userEmail = localStorage.getItem("email");
            setPayments(data.filter(p => p.user_email === userEmail));
        })();
    }, []);

    return (
        <div className="billing-page">
            <h2>Billing History</h2>
            <table className="plans-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Plan</th>
                        <th>Amount</th>
                        <th>Invoice</th>
                    </tr>
                </thead>
                <tbody>
                    {payments.map(p => (
                        <tr key={p.id}>
                            <td>{new Date(p.created_at).toLocaleDateString()}</td>
                            <td>{p.plan_name}</td>
                            <td>{p.currency} {p.amount.toFixed(2)}</td>
                            <td>
                                <a href={`${import.meta.env.VITE_API_BASE || "http://localhost:8000"}/payments/invoice/${p.id}`} target="_blank">
                                    Download
                                </a>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
