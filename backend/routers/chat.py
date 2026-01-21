import os
from typing import List

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from deps import get_db, get_current_user

load_dotenv()

router = APIRouter(prefix="/chat", tags=["Chat"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def call_ai_api(messages: List[dict]) -> str:
    """Try OpenAI first → fallback to Groq if failed."""

    OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
    GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")

    if OPENAI_API_KEY:
        try:
            response = requests.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=60,
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            print("OpenAI Error:", response.text)
        except Exception as e:
            print("OpenAI Exception:", e)

    if GROQ_API_KEY:
        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=60,
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            print("Groq Error:", response.text)
        except Exception as e:
            print("Groq Exception:", e)

    raise HTTPException(
        status_code=500,
        detail="AI API error - no valid API response received."
    )


@router.post("", response_model=schemas.ChatResponse)
def send_message(
    chat_in: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Handle user chat and AI response with subscription validation."""

    # Find active subscription
    sub = (
        db.query(models.Subscription)
        .filter(
            models.Subscription.user_id == current_user.id,
            models.Subscription.status == "active",
        )
        .order_by(models.Subscription.start_date.desc())
        .first()
    )

    if not sub:
        raise HTTPException(
            status_code=402,
            detail="No active subscription! Please upgrade your plan."
        )

    plan = sub.plan

    # Check usage limits
    if sub.used_tokens >= plan.tokens_per_month:
        raise HTTPException(
            status_code=402,
            detail="Your plan token limit is exceeded! Please upgrade."
        )

    # Save user message
    user_msg = models.ChatMessage(
        user_id=current_user.id,
        role="user",
        content=chat_in.message,
    )
    db.add(user_msg)
    db.commit()

    # Fetch last chat history for AI context
    last_msgs = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == current_user.id)
        .order_by(models.ChatMessage.created_at.desc())
        .limit(10)
        .all()
    )

    messages_for_ai = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    for m in reversed(last_msgs):
        messages_for_ai.append({"role": m.role, "content": m.content})

    messages_for_ai.append({"role": "user", "content": chat_in.message})

    # Call AI API for assistant response
    reply_text = call_ai_api(messages_for_ai)

    ai_msg = models.ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply_text,
    )
    db.add(ai_msg)

    # Update usage log & subscription usage
    sub.used_tokens += 1
    usage = models.UsageLog(
        user_id=current_user.id,
        tokens_used=1,
    )

    db.add(usage)
    db.commit()

    # Return full chat history back to frontend
    all_msgs = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == current_user.id)
        .order_by(models.ChatMessage.created_at.asc())
        .all()
    )

    return schemas.ChatResponse(
        reply=reply_text,
        history=all_msgs,
    )
