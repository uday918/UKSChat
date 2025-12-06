import React from "react";

export default function ChatMessage({ message }) {
    const isUser = message.role === "user";

    return (
        <div className={`chat-message ${isUser ? "chat-message-user" : "chat-message-ai"}`}>
            <div className="chat-avatar">
                {isUser ? "👤" : "🤖"}
            </div>
            <div className="chat-bubble">
                {message.content}
            </div>
        </div>
    );
}
