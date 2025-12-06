import React, { useEffect, useState } from "react";
import { getActivePlans, getMySubscription } from "../api";
import { createRazorpayOrder, createStripeCheckout } from "../payments";
import { useNavigate } from "react-router-dom";

export default function Pricing() {
    const [plans, setPlans] = useState([]);
    const [sub, setSub] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    useEffect(() => {
        (async () => {
            try {
                const p = await getActivePlans();
                setPlans(p);

                if (token) {
                    const s = await getMySubscription();
                    setSub(s);
                } else {
                    setSub(null);
                }
            } catch (e) {
                setError(e.message);
            }
        })();
    }, [token]);

    const handleBuy = async (plan) => {
        if (!token) {
            navigate("/login");
            return;
        }

        // Prevent selecting same active plan
        if (sub?.active && sub?.plan_id === plan.id) return;

        if (plan.currency === "INR") {
            await createRazorpayOrder(plan.id);
        } else {
            await createStripeCheckout(plan.id);
        }
    };

    return (
        <div className="pricing-page">
            <h2>Plans & Pricing</h2>
            <p className="pricing-subtitle">
                Choose the plan that fits your usage. You can upgrade anytime.
            </p>

            {sub?.active && (
                <div className="current-plan-banner">
                    <span>
                        Current plan: <strong>{sub.plan_name}</strong> —{" "}
                        {sub.remaining_tokens} / {sub.tokens_per_month} messages left
                    </span>
                </div>
            )}

            {error && <div className="admin-error">{error}</div>}

            <div className="plan-grid">
                {plans.map((p) => {
                    const isCurrentPlan = sub?.active && sub.plan_id === p.id;

                    return (
                        <div className="plan-card" key={p.id}>
                            <h3>{p.name}</h3>
                            <p className="plan-description">{p.description}</p>
                            <div className="plan-price">
                                <span className="price">
                                    {p.currency === "INR" ? "₹" : "$"}
                                    {p.price.toFixed(2)}
                                </span>
                                <span className="per">per month</span>
                            </div>
                            <ul className="plan-features">
                                <li>{p.tokens_per_month} AI messages/month</li>
                                <li>Email support</li>
                                <li>Secure billing</li>
                            </ul>

                            {!token ? (
                                <button
                                    className="btn-secondary wide"
                                    onClick={() => navigate("/login")}
                                >
                                    Sign in to Activate
                                </button>
                            ) : isCurrentPlan ? (
                                <button className="btn-active wide" disabled>
                                    Default Plan Activated
                                </button>
                            ) : (
                                <button
                                    className="btn-primary wide"
                                    onClick={() => handleBuy(p)}
                                >
                                    {p.currency === "INR"
                                        ? "Pay with Razorpay"
                                        : "Pay with Stripe"}
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
