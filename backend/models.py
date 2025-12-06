from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete")
    payments = relationship("Payment", back_populates="user", cascade="all, delete")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="messages")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    currency = Column(String(5), default="INR")
    tokens_per_month = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    subscriptions = relationship("Subscription", back_populates="plan", cascade="all, delete")
    payments = relationship("Payment", back_populates="plan", cascade="all, delete")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    status = Column(String(20), default="active")
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime)
    used_tokens = Column(Integer, default=0)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    gateway = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(5), nullable=False, default="INR")
    status = Column(String(20), default="pending")
    transaction_id = Column(String(100), unique=True)
    invoice_filename = Column(String(100))
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="payments")
    plan = relationship("Plan", back_populates="payments")


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
