import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from routers import (
    auth,
    chat,
    plans,
    payments,
    subscriptions,
    admin_plans,
    admin_billing,
)
from dbseeders.PlanSeeder import run as seed_plans
from dbseeders.UserSeeder import run as seed_admin
from dbseeders.SubscriptionSeeder import run as seed_admin_subscription

# Create DB Tables if not exist
Base.metadata.create_all(bind=engine)

# Insert seed data
db = SessionLocal()
seed_plans(db)
seed_admin(db)
seed_admin_subscription(db)
db.close()

# FastAPI App
app = FastAPI(title="UKSChat - AI SaaS Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public API
app.include_router(auth.router)
app.include_router(plans.router)
app.include_router(chat.router)

# User Billing API
app.include_router(payments.router)
app.include_router(subscriptions.router)

# Admin API
app.include_router(admin_plans.router)
app.include_router(admin_billing.router)


@app.get("/")
def root():
    return {"message": "UKSChat Backend Running 🎯"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
