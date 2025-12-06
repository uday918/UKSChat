import React, { useEffect, useState } from "react";
import { adminGetPayments } from "../api";

export default function AdminPayments() {
    const [payments, setPayments] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        (async () => {
            try {
                const data = await adminGetPayments();
                setPayments(data);
            } catch (e) {
                setError(e.message);
            }
        })();
    }, []);

    return (
        <div className="admin-page">
            <div className="admin-header">
                <div>
                    <h2>Payments & Billing</h2>
                    <p>All Razorpay & Stripe transactions made by users.</p>
                </div>
            </div>

            <div className="admin-card">
                {error && <div className="admin-error">{error}</div>}

                <div className="table-wrapper">
                    <table className="plans-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>User</th>
                                <th>Plan</th>
                                <th>Gateway</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Txn ID</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {payments.length === 0 && (
                                <tr>
                                    <td colSpan="8" style={{ textAlign: "center" }}>
                                        No payments yet.
                                    </td>
                                </tr>
                            )}
                            {payments.map((p) => (
                                <tr key={p.id}>
                                    <td>{p.id}</td>
                                    <td>{p.user_email}</td>
                                    <td>{p.plan_name}</td>
                                    <td>{p.gateway}</td>
                                    <td>
                                        {p.currency === "INR" ? "₹" : "$"}
                                        {p.amount.toFixed(2)}
                                    </td>
                                    <td>
                                        <span
                                            className={
                                                p.status === "success"
                                                    ? "chip chip-active"
                                                    : "chip chip-inactive"
                                            }
                                        >
                                            {p.status}
                                        </span>
                                    </td>
                                    <td>{p.transaction_id}</td>
                                    <td>{new Date(p.created_at).toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
