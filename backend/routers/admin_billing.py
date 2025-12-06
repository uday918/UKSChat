from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from deps import get_db, get_current_admin

router = APIRouter(prefix="/admin/billing", tags=["Admin - Billing"])


@router.get("/payments")
def list_payments(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    rows = (
        db.query(
            models.Payment.id,
            models.Payment.gateway,
            models.Payment.amount,
            models.Payment.currency,
            models.Payment.status,
            models.Payment.created_at,
            models.Payment.transaction_id,
            models.User.email,
            models.Plan.name.label("plan_name"),
        )
        .join(models.User, models.Payment.user_id == models.User.id)
        .join(models.Plan, models.Payment.plan_id == models.Plan.id)
        .order_by(models.Payment.created_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "gateway": r.gateway,
            "amount": r.amount,
            "currency": r.currency,
            "status": r.status,
            "created_at": r.created_at,
            "transaction_id": r.transaction_id,
            "user_email": r.email,
            "plan_name": r.plan_name,
        }
        for r in rows
    ]


@router.get("/usage-summary")
def usage_summary(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    # usage per user (total tokens)
    per_user = (
        db.query(
            models.User.email,
            func.sum(models.UsageLog.tokens_used).label("tokens"),
        )
        .join(models.User, models.User.id == models.UsageLog.user_id)
        .group_by(models.User.email)
        .order_by(func.sum(models.UsageLog.tokens_used).desc())
        .all()
    )

    # total revenue
    total_revenue = (
        db.query(func.sum(models.Payment.amount))
        .filter(models.Payment.status == "success")
        .scalar()
        or 0
    )

    return {
        "total_revenue": float(total_revenue),
        "top_users": [
            {"email": row.email, "tokens": int(row.tokens or 0)} for row in per_user
        ],
    }
