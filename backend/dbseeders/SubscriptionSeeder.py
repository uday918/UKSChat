from sqlalchemy.orm import Session
from models import Subscription, User, Plan
from datetime import datetime, timedelta


def create_subscription(db: Session, user: User, plan: Plan):
    existing_sub = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.plan_id == plan.id
    ).first()

    if not existing_sub:
        new_subscription = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            status="active",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=365),
            used_tokens=0,
        )
        db.add(new_subscription)
        db.commit()
        print(f"Subscribed: {user.email} → {plan.name}")
    else:
        print(f"{user.email} already subscribed to {plan.name} — Skipped!")


def run(db: Session):

    # ---------- Admin Subscription ----------
    admin = db.query(User).filter(User.email == "admin@ukschat.com").first()
    pro_plus = db.query(Plan).filter(Plan.name == "Pro Plus").first()

    if admin and pro_plus:
        create_subscription(db, admin, pro_plus)
    else:
        print("Admin or Pro Plus plan missing — Skipping!")

    # ---------- Default User Subscription ----------
    default_user = db.query(User).filter(User.email == "user@ukschat.com").first()
    free_plan = db.query(Plan).filter(Plan.price == 0).first()  # Free tier detection

    if default_user and free_plan:
        create_subscription(db, default_user, free_plan)
    else:
        print("Default User or Free Plan missing — Skipping!")
