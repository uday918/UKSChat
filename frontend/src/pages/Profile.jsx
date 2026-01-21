import React, { useEffect, useState } from "react";
import { getMySubscription } from "../api";

export default function Profile() {
    const [sub, setSub] = useState(null);
    const email = localStorage.getItem("email");

    useEffect(() => {
        (async () => {
            const s = await getMySubscription();
            setSub(s);
        })();
    }, []);

    const cancelSubscription = async () => {
        await fetch(`${import.meta.env.VITE_API_BASE || "http://localhost:8000"}/subscription/cancel`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        });
        window.location.reload();
    };

    return (
        <div className="profile-page">
            <h2>My Account</h2>
            <p>{email}</p>

            {sub && sub.active ? (
                <>
                    <h3>Current Plan: {sub.plan_name}</h3>
                    <p>
                        Remaining: {sub.remaining_tokens} / {sub.tokens_per_month}
                    </p>

                    <a href="/pricing" className="btn-primary">
                        Change Plan
                    </a>

                    {/* Hide cancel button if plan is FREE */}
                    {sub.price > 0 && (
                        <button className="btn-danger" onClick={cancelSubscription}>
                            Cancel Subscription
                        </button>
                    )}
                </>
            ) : (
                <a href="/pricing" className="btn-primary">
                    Purchase a Plan
                </a>
            )}
        </div>
    );
}
