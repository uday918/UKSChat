import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { adminGetUsageSummary } from "../api";

export default function AdminDashboard() {
    const email = localStorage.getItem("email") || "";
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                const s = await adminGetUsageSummary();
                setSummary(s);
            } catch { }
        })();
    }, []);

    return (
        <div className="admin-page">
            <div className="admin-header">
                <div>
                    <h2>Admin Dashboard</h2>
                    <p>Manage your SaaS business: plans, billing & usage.</p>
                </div>
                <div className="admin-badge">
                    <span>Admin</span>
                    <small>{email}</small>
                </div>
            </div>

            <div className="admin-grid">
                <div className="admin-card highlight">
                    <h3>Plans & Pricing</h3>
                    <p>Create, edit and activate/inactivate plans with different currencies.</p>
                    <Link to="/admin/plans" className="btn-primary">
                        Manage Plans
                    </Link>
                </div>

                <div className="admin-card">
                    <h3>Payments & Billing</h3>
                    <p>View Razorpay & Stripe transactions, amount & status.</p>
                    <Link to="/admin/payments" className="btn-primary">
                        View Payments
                    </Link>
                </div>

                <div className="admin-card">
                    <h3>Usage & Analytics</h3>
                    {summary ? (
                        <>
                            <p>Total revenue (success): ₹ / $ {summary.total_revenue.toFixed(2)}</p>
                            <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>
                                Top users by usage:
                            </p>
                            <ul className="usage-list">
                                {summary.top_users.slice(0, 5).map((u) => (
                                    <li key={u.email}>
                                        <strong>{u.email}</strong> — {u.tokens} msgs
                                    </li>
                                ))}
                            </ul>
                        </>
                    ) : (
                        <p>(Usage data will appear once users start chatting.)</p>
                    )}
                </div>
            </div>
        </div>
    );
}
