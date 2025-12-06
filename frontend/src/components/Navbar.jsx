import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

export default function Navbar({ onLogout }) {
    const location = useLocation();
    const navigate = useNavigate();
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    const email = localStorage.getItem("email") || "";

    const isAuthPage =
        location.pathname === "/login" || location.pathname === "/register";

    const navLinkClass = (path) =>
        location.pathname === path
            ? "nav-link nav-link-primary"
            : "nav-link";

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <span
                    className="app-logo"
                    onClick={() => navigate(token ? "/chat" : "/")}
                    style={{ cursor: "pointer" }}
                >
                    🤖 UKSChat
                </span>

                {/* Public menu */}
                <Link to="/pricing" className={navLinkClass("/pricing")}>
                    Pricing
                </Link>

                {/* Logged-in User menus */}
                {token && (
                    <>
                        <Link to="/chat" className={navLinkClass("/chat")}>
                            Chat
                        </Link>

                        <Link to="/billing" className={navLinkClass("/billing")}>
                            Billing
                        </Link>

                        <Link to="/profile" className={navLinkClass("/profile")}>
                            Profile
                        </Link>
                    </>
                )}

                {/* Admin only */}
                {role === "admin" && token && (
                    <Link
                        to="/admin"
                        className={
                            location.pathname.startsWith("/admin")
                                ? "nav-link nav-link-primary"
                                : "nav-link"
                        }
                    >
                        Admin
                    </Link>
                )}
            </div>

            <div className="navbar-right">
                {!isAuthPage && token && (
                    <>
                        <span className="nav-user-email">{email}</span>
                        <button className="nav-link nav-link-danger" onClick={onLogout}>
                            Logout
                        </button>
                    </>
                )}

                {!token && !isAuthPage && (
                    <>
                        <Link to="/login" className="nav-link">
                            Login
                        </Link>
                        <Link to="/register" className="nav-link nav-link-primary">
                            Register
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
}
