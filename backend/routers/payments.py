import os
from datetime import datetime, timedelta

import razorpay
import stripe
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import models
from deps import get_db, get_current_user

from utils.invoice import generate_invoice
from utils.mailer import send_invoice_email

load_dotenv()

router = APIRouter(prefix="/payments", tags=["Payments"])

# ---------- Razorpay (INR) ----------
RAZORPAY_KEY = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

# ---------- Stripe (USD) ----------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def activate_subscription(db: Session, user_id: int, plan: models.Plan) -> models.Subscription:
    now = datetime.utcnow()
    end_date = now + timedelta(days=30)

    # expire old active subscriptions
    db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id,
        models.Subscription.status == "active"
    ).update({"status": "expired"})

    subscription = models.Subscription(
        user_id=user_id,
        plan_id=plan.id,
        status="active",
        start_date=now,
        end_date=end_date,
        used_tokens=0,
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@router.post("/razorpay/create-order/{plan_id}")
def razorpay_create_order(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id, models.Plan.is_active == True).first()
    if not plan or plan.currency != "INR":
        raise HTTPException(status_code=400, detail="Invalid INR plan")

    amount_paise = max(int(plan.price * 100), 100)  # Razorpay minimum = ₹1

    order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1,
    })

    payment = models.Payment(
        user_id=current_user.id,
        plan_id=plan.id,
        gateway="razorpay",
        amount=plan.price,
        currency="INR",
        status="created",
        transaction_id=order["id"],
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "order_id": order["id"],
        "key": RAZORPAY_KEY,
        "amount": amount_paise,
        "currency": "INR",
        "plan_name": plan.name,
    }


@router.post("/razorpay/verify")
async def razorpay_verify(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = await request.json()
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")
    signature = data.get("signature")

    if not all([order_id, payment_id, signature]):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    payment = db.query(models.Payment).filter_by(
        transaction_id=order_id,
        gateway="razorpay"
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = "success"
    db.commit()
    db.refresh(payment)

    plan = payment.plan
    activate_subscription(db, current_user.id, plan)

    user = current_user

    # generate invoice
    invoice_name, invoice_path = generate_invoice(payment, user, plan)
    payment.invoice_filename = invoice_name
    db.commit()

    await send_invoice_email(user.email, invoice_path)

    return {"message": "Payment verified, subscription activated & invoice emailed"}


@router.post("/stripe/checkout/{plan_id}")
def stripe_checkout(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id, models.Plan.is_active == True).first()
    if not plan or plan.currency != "USD":
        raise HTTPException(status_code=400, detail="Invalid USD plan")

    checkout = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": plan.name},
                "unit_amount": int(plan.price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5173/pricing?success=1",
        cancel_url="http://localhost:5173/pricing?canceled=1",
        metadata={"user_id": current_user.id, "plan_id": plan.id},
    )

    payment = models.Payment(
        user_id=current_user.id,
        plan_id=plan.id,
        gateway="stripe",
        amount=plan.price,
        currency="USD",
        status="pending",
        transaction_id=checkout.id,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {"checkout_url": checkout.url}


@router.get("/invoice/{payment_id}")
def download_invoice(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    payment = db.query(models.Payment).filter(
        models.Payment.id == payment_id,
        models.Payment.user_id == current_user.id,
    ).first()

    if not payment or not payment.invoice_filename:
        raise HTTPException(status_code=404, detail="Invoice not ready yet")

    path = os.path.join("invoices", payment.invoice_filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Invoice file missing")

    return FileResponse(path, filename=payment.invoice_filename)
