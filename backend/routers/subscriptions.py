from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models
from deps import get_db, get_current_user

router = APIRouter(prefix="/subscription", tags=["Subscription"])

@router.get("/me")
def my_subscription(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
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
        return {"active": False}

    plan = sub.plan
    remaining = max(plan.tokens_per_month - sub.used_tokens, 0)

    return {
        "active": True,
        "plan_id": plan.id,
        "plan_name": plan.name,
        "price": plan.price,
        "currency": plan.currency,
        "tokens_per_month": plan.tokens_per_month,
        "used_tokens": sub.used_tokens,
        "remaining_tokens": remaining,
        "end_date": sub.end_date.isoformat() if sub.end_date else None,
        "is_expired": sub.end_date < datetime.utcnow() if sub.end_date else False,
    }


@router.delete("/cancel")
def cancel_subscription(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    sub = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.status == "active",
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription found")

    sub.status = "cancelled"
    db.commit()

    return {"message": "Subscription cancelled successfully"}
