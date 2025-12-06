import React, { useEffect, useState } from "react";
import { sendMessage, getMySubscription } from "../api";
import ChatMessage from "../components/ChatMessage";

export default function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [sub, setSub] = useState(null);

    useEffect(() => {
        (async () => {
            const s = await getMySubscription();
            setSub(s);
        })();
    }, []);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        setError("");
        const newUserMessage = {
            id: Date.now(),
            role: "user",
            content: input,
            created_at: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, newUserMessage]);
        const currentInput = input;
        setInput("");
        setLoading(true);

        try {
            const res = await sendMessage(currentInput);
            setMessages(res.history);
            const s = await getMySubscription();
            setSub(s);
        } catch (err) {
            setError(err.message || "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-page">
            <div className="chat-container">
                <div className="chat-header">
                    <h2>Your AI Assistant</h2>
                    <p>Ask anything. The AI will help you.</p>
                </div>

                {sub && sub.active && (
                    <div className="current-plan-banner">
                        Plan: <strong>{sub.plan_name}</strong> —{" "}
                        <span>
                            {sub.remaining_tokens} / {sub.tokens_per_month} messages left
                        </span>
                    </div>
                )}
                {sub && !sub.active && (
                    <div className="current-plan-banner warning">
                        No active subscription. Please select a plan from the{" "}
                        <a href="/pricing">pricing page</a>.
                    </div>
                )}

                <div className="chat-messages">
                    {messages.length === 0 && (
                        <div className="chat-empty">
                            Start a conversation by typing a message below.
                        </div>
                    )}
                    {messages.map((m) => (
                        <ChatMessage key={m.id} message={m} />
                    ))}
                    {loading && (
                        <div className="chat-message chat-message-ai">
                            <div className="chat-avatar">🤖</div>
                            <div className="chat-bubble typing-bubble">Thinking...</div>
                        </div>
                    )}
                </div>

                {error && <div className="chat-error">{error}</div>}

                <form className="chat-input-bar" onSubmit={handleSend}>
                    <textarea
                        rows="1"
                        placeholder="Type your message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                handleSend(e);
                            }
                        }}
                    />
                    <button type="submit" disabled={loading || !input.trim()}>
                        {loading ? "Sending..." : "Send"}
                    </button>
                </form>
            </div>
        </div>
    );
}
