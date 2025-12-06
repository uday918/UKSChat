import React, { useEffect, useState } from "react";
import {
    adminGetPlans,
    adminCreatePlan,
    adminUpdatePlan,
    adminTogglePlan,
} from "../api";

export default function AdminPlans() {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [editingId, setEditingId] = useState(null);
    const [form, setForm] = useState({
        name: "",
        description: "",
        price: "",
        currency: "INR",
        tokens_per_month: "",
        is_active: true,
    });

    const resetForm = () => {
        setEditingId(null);
        setForm({
            name: "",
            description: "",
            price: "",
            currency: "INR",
            tokens_per_month: "",
            is_active: true,
        });
    };

    const loadPlans = async () => {
        setLoading(true);
        setError("");
        try {
            const data = await adminGetPlans();
            setPlans(data);
        } catch (err) {
            setError(err.message || "Failed to load plans");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPlans();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        setSaving(true);
        try {
            const payload = {
                ...form,
                price: parseFloat(form.price),
                tokens_per_month: parseInt(form.tokens_per_month, 10),
            };

            if (editingId) {
                await adminUpdatePlan(editingId, payload);
                setSuccess("Plan updated successfully.");
            } else {
                await adminCreatePlan(payload);
                setSuccess("Plan created successfully.");
            }
            resetForm();
            await loadPlans();
        } catch (err) {
            setError(err.message || "Failed to save plan");
        } finally {
            setSaving(false);
        }
    };

    const handleEdit = (plan) => {
        setEditingId(plan.id);
        setForm({
            name: plan.name,
            description: plan.description || "",
            price: plan.price.toString(),
            currency: plan.currency,
            tokens_per_month: plan.tokens_per_month.toString(),
            is_active: plan.is_active,
        });
    };

    const handleToggle = async (id) => {
        setError("");
        setSuccess("");
        try {
            await adminTogglePlan(id);
            setSuccess("Plan status updated.");
            await loadPlans();
        } catch (err) {
            setError(err.message || "Failed to toggle plan");
        }
    };

    return (
        <div className="admin-page">
            <div className="admin-header">
                <div>
                    <h2>Plans & Pricing</h2>
                    <p>Create and manage pricing plans for your ChatGPT SaaS.</p>
                </div>
            </div>

            <div className="admin-layout">
                <div className="admin-main">
                    <div className="admin-card">
                        <div className="admin-card-header">
                            <h3>Available Plans</h3>
                            {loading && <span className="chip small">Loading...</span>}
                        </div>

                        {error && <div className="admin-error">{error}</div>}
                        {success && <div className="admin-success">{success}</div>}

                        <div className="table-wrapper">
                            <table className="plans-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Currency</th>
                                        <th>Price</th>
                                        <th>Tokens/Month</th>
                                        <th>Status</th>
                                        <th>Created</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {plans.length === 0 && !loading && (
                                        <tr>
                                            <td colSpan="8" style={{ textAlign: "center" }}>
                                                No plans created yet.
                                            </td>
                                        </tr>
                                    )}
                                    {plans.map((p) => (
                                        <tr key={p.id}>
                                            <td>{p.id}</td>
                                            <td>{p.name}</td>
                                            <td>{p.currency}</td>
                                            <td>
                                                {p.currency === "INR" ? "₹" : "$"}
                                                {p.price.toFixed(2)}
                                            </td>
                                            <td>{p.tokens_per_month}</td>
                                            <td>
                                                <span
                                                    className={
                                                        p.is_active ? "chip chip-active" : "chip chip-inactive"
                                                    }
                                                >
                                                    {p.is_active ? "Active" : "Inactive"}
                                                </span>
                                            </td>
                                            <td>{new Date(p.created_at).toLocaleDateString()}</td>
                                            <td>
                                                <div className="table-actions">
                                                    <button
                                                        type="button"
                                                        className="btn-small"
                                                        onClick={() => handleEdit(p)}
                                                    >
                                                        Edit
                                                    </button>
                                                    <button
                                                        type="button"
                                                        className="btn-small-outline"
                                                        onClick={() => handleToggle(p.id)}
                                                    >
                                                        {p.is_active ? "Deactivate" : "Activate"}
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div className="admin-side">
                    <div className="admin-card">
                        <div className="admin-card-header">
                            <h3>{editingId ? "Edit Plan" : "Create Plan"}</h3>
                        </div>

                        <form className="admin-form" onSubmit={handleSubmit}>
                            <label>
                                Name
                                <input
                                    type="text"
                                    value={form.name}
                                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                                    placeholder="Pro, Starter, Enterprise..."
                                    required
                                />
                            </label>

                            <label>
                                Description
                                <textarea
                                    rows="3"
                                    value={form.description}
                                    onChange={(e) =>
                                        setForm({ ...form, description: e.target.value })
                                    }
                                    placeholder="Short description of this plan..."
                                />
                            </label>

                            <div className="admin-form-row">
                                <label>
                                    Currency
                                    <select
                                        value={form.currency}
                                        onChange={(e) =>
                                            setForm({ ...form, currency: e.target.value })
                                        }
                                    >
                                        <option value="INR">INR (₹)</option>
                                        <option value="USD">USD ($)</option>
                                    </select>
                                </label>

                                <label>
                                    Price
                                    <input
                                        type="number"
                                        step="0.01"
                                        value={form.price}
                                        onChange={(e) =>
                                            setForm({ ...form, price: e.target.value })
                                        }
                                        placeholder="e.g. 299"
                                        required
                                    />
                                </label>
                            </div>

                            <label>
                                Tokens per month
                                <input
                                    type="number"
                                    value={form.tokens_per_month}
                                    onChange={(e) =>
                                        setForm({ ...form, tokens_per_month: e.target.value })
                                    }
                                    placeholder="e.g. 1000"
                                    required
                                />
                            </label>

                            <label className="checkbox-row">
                                <input
                                    type="checkbox"
                                    checked={form.is_active}
                                    onChange={(e) =>
                                        setForm({ ...form, is_active: e.target.checked })
                                    }
                                />
                                <span>Plan is active</span>
                            </label>

                            <div className="admin-form-actions">
                                {editingId && (
                                    <button
                                        type="button"
                                        className="btn-secondary"
                                        onClick={resetForm}
                                    >
                                        Cancel edit
                                    </button>
                                )}

                                <button type="submit" className="btn-primary" disabled={saving}>
                                    {saving
                                        ? editingId
                                            ? "Saving..."
                                            : "Creating..."
                                        : editingId
                                            ? "Save changes"
                                            : "Create plan"}
                                </button>
                            </div>
                        </form>

                        <p className="admin-hint">
                            Tip: Create separate plans for INR (Razorpay) and USD (Stripe).
                            Later hum payments ko in currencies se map karenge.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
