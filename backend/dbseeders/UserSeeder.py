from sqlalchemy.orm import Session
from models import User
from auth_utils import get_password_hash


def run(db: Session):
    # ---- Seed Admin User ----
    admin_email = "admin@ukschat.com"
    admin = db.query(User).filter(User.email == admin_email).first()

    if not admin:
        new_admin = User(
            email=admin_email,
            hashed_password=get_password_hash("Admin@123"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created: admin@ukschat.com / Admin@123")
    else:
        print("Admin user already exists — Seeder skipped!")

    # ---- Seed Normal User ----
    user_email = "user@ukschat.com"
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        new_user = User(
            email=user_email,
            hashed_password=get_password_hash("User@123"),
            role="user"
        )
        db.add(new_user)
        db.commit()
        print("User created: user@ukschat.com / User@123")
    else:
        print("Default user already exists — Seeder skipped!")
