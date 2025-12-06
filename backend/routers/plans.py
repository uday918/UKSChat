from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models, schemas
from deps import get_db

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("", response_model=list[schemas.PlanOut])
def list_active_plans(db: Session = Depends(get_db)):
    """
    Public endpoint: show only active plans.
    Frontend pricing page yahan se data lega.
    """
    plans = (
        db.query(models.Plan)
        .filter(models.Plan.is_active == True)
        .order_by(models.Plan.price.asc())
        .all()
    )
    return plans
