from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    analyses = relationship("Analysis", back_populates="user")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    sentiment_score = Column(Float)
    market_type = Column(String(50))  # 'stock', 'forex', 'crypto'
    language = Column(String(10))  # 'en', 'fa'
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="analyses")
    events = relationship("Event", back_populates="analysis")
    rumors = relationship("Rumor", back_populates="analysis")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50))  # 'earnings', 'merger', 'regulatory', etc.
    description = Column(Text)
    confidence = Column(Float)
    impact = Column(String(20))  # 'high', 'medium', 'low'
    event_data = Column(JSON)  # Additional event data
    created_at = Column(DateTime, default=datetime.utcnow)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))

    analysis = relationship("Analysis", back_populates="events")

class Rumor(Base):
    __tablename__ = "rumors"

    id = Column(Integer, primary_key=True, index=True)
    rumor_type = Column(String(50))  # 'market_manipulation', 'insider_trading', etc.
    description = Column(Text)
    confidence = Column(Float)
    verdict = Column(String(20))  # 'verified', 'unverified', 'debunked'
    sources = Column(JSON)  # List of source texts
    rumor_data = Column(JSON)  # Additional rumor data
    created_at = Column(DateTime, default=datetime.utcnow)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))

    analysis = relationship("Analysis", back_populates="rumors")

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    market_type = Column(String(50))  # 'stock', 'forex', 'crypto'
    symbol = Column(String(50), index=True)
    price = Column(Float)
    volume = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sentiment_impact = Column(Float)  # Correlation between sentiment and price movement
    market_data = Column(JSON)  # Additional market data

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    log_data = Column(JSON)  # Additional log data
    
    user = relationship("User") 