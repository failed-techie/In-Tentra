"""
Database models for INTENTRA
Defines SQLAlchemy ORM models for trade tracking
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from .database import Base


class TradeIntent(Base):
    """
    Stores user trading intents and their processing status
    """
    __tablename__ = "trade_intents"
    
    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(String, unique=True, index=True, nullable=False)
    
    # Intent details
    symbol = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)  # buy/sell
    quantity = Column(Integer, nullable=False)
    order_type = Column(String, default="market")
    price = Column(Float, nullable=True)
    
    # Processing status
    status = Column(String, default="pending")  # pending/analyzing/approved/rejected/executed/failed
    
    # Raw intent and compiled intent
    raw_intent = Column(JSON)
    compiled_intent = Column(JSON)
    
    # Analysis and validation results
    analysis_result = Column(JSON)
    validation_result = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    executions = relationship("TradeExecution", back_populates="intent")
    violations = relationship("PolicyViolation", back_populates="intent")


class TradeExecution(Base):
    """
    Stores actual trade execution details
    """
    __tablename__ = "trade_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(String, unique=True, index=True, nullable=False)
    intent_id = Column(Integer, ForeignKey("trade_intents.id"))
    
    # Order details
    order_id = Column(String, index=True)  # Alpaca order ID
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy/sell
    quantity = Column(Integer, nullable=False)
    order_type = Column(String)
    
    # Execution details
    filled_qty = Column(Integer, default=0)
    filled_avg_price = Column(Float, nullable=True)
    status = Column(String)  # submitted/filled/cancelled/rejected
    
    # Execution metadata
    execution_details = Column(JSON)
    
    # Timestamps
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    filled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    intent = relationship("TradeIntent", back_populates="executions")


class PolicyViolation(Base):
    """
    Logs policy violations for audit and analysis
    """
    __tablename__ = "policy_violations"
    
    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("trade_intents.id"))
    
    # Violation details
    violation_type = Column(String, nullable=False)
    policy_name = Column(String)
    severity = Column(String)  # low/medium/high/critical
    description = Column(String)
    
    # Context
    violation_data = Column(JSON)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    intent = relationship("TradeIntent", back_populates="violations")
