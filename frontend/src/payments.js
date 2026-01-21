const API_URL = `${import.meta.env.VITE_API_BASE || "http://localhost:8000"}/payments`;

export async function createRazorpayOrder(planId) {
    const token = localStorage.getItem("token");

    try {
        const res = await fetch(`${API_URL}/razorpay/create-order/${planId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            alert(data.detail || "Failed to create Razorpay order");
            return;
        }

        if (!window.Razorpay) {
            alert("Razorpay SDK not loaded");
            return;
        }

        const options = {
            key: data.key,
            amount: data.amount,
            currency: data.currency,
            name: "UKSChat",
            description: data.plan_name,
            order_id: data.order_id,

            handler: async function (response) {
                try {
                    const verifyRes = await fetch(`${API_URL}/razorpay/verify`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({
                            order_id: data.order_id,
                            payment_id: response.razorpay_payment_id,
                            signature: response.razorpay_signature,
                        }),
                    });

                    const verifyData = await verifyRes.json().catch(() => ({}));
                    if (!verifyRes.ok) {
                        alert(verifyData.detail || "Payment verification failed");
                    } else {
                        alert("Payment success! Subscription activated.");
                        window.location.reload();
                    }
                } catch (err) {
                    alert("Payment verification failed");
                    console.error(err);
                }
            },

            modal: {
                ondismiss: function () {
                    alert("Payment cancelled!");
                },
            },

            theme: { color: "#4f46e5" },
        };

        const rzp = new window.Razorpay(options);
        rzp.open();
    } catch (err) {
        alert("Razorpay checkout error: " + err.message);
        console.error(err);
    }
}



export async function createStripeCheckout(planId) {
    const token = localStorage.getItem("token");

    try {
        const res = await fetch(`${API_URL}/stripe/checkout/${planId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            alert(data.detail || "Failed to create Stripe checkout");
            return;
        }

        // Redirect to Stripe Checkout
        window.location.href = data.checkout_url;

    } catch (err) {
        alert("Stripe checkout failed");
        console.error(err);
    }
}
