from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from deps import get_db, get_current_admin

router = APIRouter(prefix="/admin/plans", tags=["Admin - Plans"])


@router.get("", response_model=list[schemas.PlanOut])
def admin_list_plans(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    List ALL plans (including inactive).
    """
    plans = db.query(models.Plan).order_by(models.Plan.created_at.desc()).all()
    return plans


@router.post("", response_model=schemas.PlanOut)
def admin_create_plan(
    plan_in: schemas.PlanCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    plan = models.Plan(
        name=plan_in.name,
        description=plan_in.description,
        price=plan_in.price,
        currency=plan_in.currency,
        tokens_per_month=plan_in.tokens_per_month,
        is_active=plan_in.is_active,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.put("/{plan_id}", response_model=schemas.PlanOut)
def admin_update_plan(
    plan_id: int,
    plan_in: schemas.PlanUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    update_data = plan_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)

    db.commit()
    db.refresh(plan)
    return plan


@router.patch("/{plan_id}/toggle", response_model=schemas.PlanOut)
def admin_toggle_plan_active(
    plan_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.is_active = not plan.is_active
    db.commit()
    db.refresh(plan)
    return plan
