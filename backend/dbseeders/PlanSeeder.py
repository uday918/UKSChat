from sqlalchemy.orm import Session
from models import Plan


def run(db: Session):
    if db.query(Plan).count() == 0:
        plans = [
            Plan(
                name="Free Tier",
                description="Features: Limited response speed\nTokens/Month: 50 requests",
                price=0,
                currency="INR",
                tokens_per_month=50,
                is_active=True,
            ),
            Plan(
                name="Pro Monthly",
                description="Features: Fast responses\nTokens/Month: 1000 requests",
                price=299,
                currency="INR",
                tokens_per_month=1000,
                is_active=True,
            ),
            Plan(
                name="Pro Plus",
                description="Features: Priority support\nTokens/Month: 3000 requests",
                price=599,
                currency="INR",
                tokens_per_month=3000,
                is_active=True,
            )
        ]
        db.add_all(plans)
        db.commit()
        print("Default Plans Inserted!")
    else:
        print("Plans already exist — Seeding skipped.")
