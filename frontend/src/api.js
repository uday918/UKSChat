const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// ---------- AUTH ----------

export async function register(email, password) {
    const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Registration failed");
    return data;
}

export async function login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Login failed");
    return data;
}

// ---------- CHAT ----------

export async function sendMessage(message) {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Chat failed");
    return data;
}

// ---------- PLANS (PUBLIC) ----------

export async function getActivePlans() {
    const res = await fetch(`${API_BASE}/plans`);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to load plans");
    return data;
}

// ---------- SUBSCRIPTION ----------

export async function getMySubscription() {
    const token = localStorage.getItem("token");
    if (!token) return null;

    const res = await fetch(`${API_BASE}/subscription/me`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    if (res.status === 401) return null;
    return res.json().catch(() => null);
}

export async function cancelSubscription() {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_BASE}/subscription/cancel`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Cancel failed");
    return data;
}

// ---------- ADMIN HELPERS ----------

function authHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

// Plans
export async function adminGetPlans() {
    const res = await fetch(`${API_BASE}/admin/plans`, {
        headers: authHeaders(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to load plans");
    return data;
}

export async function adminCreatePlan(plan) {
    const res = await fetch(`${API_BASE}/admin/plans`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(plan),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to create plan");
    return data;
}

export async function adminUpdatePlan(id, plan) {
    const res = await fetch(`${API_BASE}/admin/plans/${id}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify(plan),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to update plan");
    return data;
}

export async function adminTogglePlan(id) {
    const res = await fetch(`${API_BASE}/admin/plans/${id}/toggle`, {
        method: "PATCH",
        headers: authHeaders(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to toggle plan");
    return data;
}

// Billing
export async function adminGetPayments() {
    const res = await fetch(`${API_BASE}/admin/billing/payments`, {
        headers: authHeaders(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to load payments");
    return data;
}

export async function adminGetUsageSummary() {
    const res = await fetch(`${API_BASE}/admin/billing/usage-summary`, {
        headers: authHeaders(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Failed to load usage summary");
    return data;
}
