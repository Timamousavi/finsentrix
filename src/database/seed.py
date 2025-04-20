from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from passlib.context import CryptContext
import hashlib

from .models import User, Analysis, Event, Rumor, MarketData
from .database import Base, engine

def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def clear_database(db: Session):
    """Remove all data from the database."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Only try to delete from tables that exist
    if "market_data" in existing_tables:
        db.query(MarketData).delete()
    if "rumors" in existing_tables:
        db.query(Rumor).delete()
    if "events" in existing_tables:
        db.query(Event).delete()
    if "analyses" in existing_tables:
        db.query(Analysis).delete()
    if "users" in existing_tables:
        db.query(User).delete()
    db.commit()

def seed_database(db: Session):
    """Seed the database with initial data."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create admin user
    admin = User(
        email="admin@finsentrix.com",
        username="admin",
        hashed_password=hash_password("admin123"),
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    
    # Create test user
    test_user = User(
        email="test@finsentrix.com",
        username="testuser",
        hashed_password=hash_password("test123"),
        is_active=True
    )
    db.add(test_user)
    db.commit()
    
    # Sample texts for different market types
    sample_texts = {
        "stock": [
            "شرکت ایران خودرو گزارش مالی مثبتی منتشر کرد",
            "سود سهام شرکت فولاد مبارکه افزایش یافت",
            "بازار سرمایه امروز روند صعودی داشت"
        ],
        "forex": [
            "نرخ دلار در بازار آزاد کاهش یافت",
            "یورو به بالاترین قیمت خود در ماه جاری رسید",
            "نوسانات ارزی در بازار تهران ادامه دارد"
        ],
        "crypto": [
            "بیت کوین از مرز مقاومتی عبور کرد",
            "اتریوم روند نزولی را آغاز کرد",
            "ارزهای دیجیتال در مسیر بهبود قرار گرفتند"
        ]
    }
    
    # Create analyses with events and rumors
    for _ in range(20):
        market_type = random.choice(["stock", "forex", "crypto"])
        text = random.choice(sample_texts[market_type])
        
        analysis = Analysis(
            text=text,
            sentiment_score=random.uniform(-1.0, 1.0),
            market_type=market_type,
            confidence=random.uniform(0.5, 1.0),
            user_id=random.choice([admin.id, test_user.id])
        )
        db.add(analysis)
        db.commit()
        
        # Add event for some analyses
        if random.random() > 0.5:
            event = Event(
                event_type=random.choice(["earnings", "merger", "regulatory", "market_news"]),
                description=f"Event related to {text}",
                impact_score=random.uniform(-1.0, 1.0),
                analysis_id=analysis.id
            )
            db.add(event)
        
        # Add rumor for some analyses
        if random.random() > 0.7:
            rumor = Rumor(
                rumor_type=random.choice(["market_manipulation", "insider_trading", "false_news"]),
                description=f"Rumor related to {text}",
                credibility_score=random.uniform(0.0, 1.0),
                analysis_id=analysis.id
            )
            db.add(rumor)
    
    # Create market data for the last 30 days
    symbols = {
        "stock": ["IKCO", "FOLD", "PARS"],
        "forex": ["USD/IRR", "EUR/IRR", "GBP/IRR"],
        "crypto": ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    }
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    for market_type, market_symbols in symbols.items():
        for symbol in market_symbols:
            current_date = start_date
            base_price = random.uniform(100, 10000)
            
            while current_date <= end_date:
                price_change = random.uniform(-0.05, 0.05)
                new_price = base_price * (1 + price_change)
                
                market_data = MarketData(
                    market_type=market_type,
                    symbol=symbol,
                    price=new_price,
                    volume=random.uniform(1000, 100000),
                    timestamp=current_date,
                    sentiment_impact=random.uniform(-1.0, 1.0)
                )
                db.add(market_data)
                
                base_price = new_price
                current_date += timedelta(hours=4)
    
    db.commit() 