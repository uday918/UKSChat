from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import models, schemas
from auth_utils import get_password_hash, verify_password, create_access_token
from deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


def activate_free_plan(db: Session, user_id: int):
    """Automatically assign Free plan to new users"""
    free_plan = db.query(models.Plan).filter(
        models.Plan.price == 0,
        models.Plan.is_active == True
    ).first()

    if free_plan:
        now = datetime.utcnow()
        end_date = now + timedelta(days=30)

        subscription = models.Subscription(
            user_id=user_id,
            plan_id=free_plan.id,
            status="active",
            start_date=now,
            end_date=end_date,
            used_tokens=0,
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed = get_password_hash(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Auto activate Free Tier
    activate_free_plan(db, user.id)

    return user


@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "email": user.email,
    }


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
