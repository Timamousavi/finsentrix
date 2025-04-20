from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, Field
from typing import List, Optional
import jwt
import os
from datetime import datetime, timedelta
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from ..models.sentiment_analyzer import SentimentAnalyzer
from ..utils.text_processor import FinancialTextProcessor
from dotenv import load_dotenv
from ..models.event_detector import EventDetector, RumorDetector
from ..utils.visualization import create_timeline_visualization, create_rumor_analysis_visualization
import pandas as pd
import numpy as np
from ..core.sentiment_analyzer import SentimentAnalyzer as CoreSentimentAnalyzer
from ..core.event_detector import EventDetector as CoreEventDetector
from ..core.rumor_analyzer import RumorAnalyzer as CoreRumorAnalyzer
from ..core.market_processor import MarketProcessor as CoreMarketProcessor
from ..database.database import SessionLocal, get_db
from ..database.models import Analysis, Event, Rumor, MarketData
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api.log'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FinSentrix (FSX) API",
    description="Global Financial Market Sentiment Analysis API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, replace with specific domains
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    language: Optional[str] = "auto"
    market_type: Optional[str] = None
    market_region: Optional[str] = None
    model_version: Optional[str] = "latest"

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    market_type: str
    market_region: str
    language: str
    model_version: str
    processing_time: float

class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100)
    language: Optional[str] = "auto"
    market_type: Optional[str] = None
    market_region: Optional[str] = None
    model_version: Optional[str] = "latest"

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]
    total_processing_time: float

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()

# Initialize components
event_detector = EventDetector()
rumor_detector = RumorDetector()

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # In production, use proper password hashing
    return plain_password == hashed_password

def get_user(username: str):
    # In production, use a proper database
    fake_users_db = {
        "testuser": {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "disabled": False,
            "hashed_password": "testpass"
        }
    }
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
@RateLimiter(times=5, minutes=1)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
@limiter.limit("5/minute")
async def root():
    return {"message": "FinSentrix (FSX) Global Market Sentiment Analysis API"}

@app.post("/analyze", response_model=SentimentResponse)
@RateLimiter(times=10, minutes=1)
async def analyze_sentiment(
    request: Request,
    sentiment_request: SentimentRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        start_time = datetime.now()
        
        # Process text
        pred_labels, probabilities = analyzer.predict([sentiment_request.text])
        
        # Calculate confidence
        confidence = float(probabilities[0][1] if pred_labels[0] == 1 else probabilities[0][0])
        
        # Determine sentiment
        sentiment = "positive" if pred_labels[0] == 1 else "negative"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return SentimentResponse(
            sentiment=sentiment,
            confidence=confidence,
            market_type=sentiment_request.market_type or "global",
            market_region=sentiment_request.market_region or "global",
            language=sentiment_request.language or "auto",
            model_version=analyzer.metadata['version'],
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/batch", response_model=BatchSentimentResponse)
@RateLimiter(times=5, minutes=1)
async def analyze_batch_sentiment(
    request: Request,
    batch_request: BatchSentimentRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        start_time = datetime.now()
        
        # Process texts
        pred_labels, probabilities = analyzer.predict(batch_request.texts)
        
        # Prepare results
        results = []
        for i, (label, prob) in enumerate(zip(pred_labels, probabilities)):
            confidence = float(prob[1] if label == 1 else prob[0])
            sentiment = "positive" if label == 1 else "negative"
            
            results.append(SentimentResponse(
                sentiment=sentiment,
                confidence=confidence,
                market_type=batch_request.market_type or "global",
                market_region=batch_request.market_region or "global",
                language=batch_request.language or "auto",
                model_version=analyzer.metadata['version'],
                processing_time=0  # Individual processing time not tracked
            ))
        
        total_processing_time = (datetime.now() - start_time).total_seconds()
        
        return BatchSentimentResponse(
            results=results,
            total_processing_time=total_processing_time
        )
    except Exception as e:
        logger.error(f"Error in batch sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
@limiter.limit("5/minute")
async def get_model_info(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    try:
        return {
            "version": analyzer.metadata['version'],
            "created_at": analyzer.metadata['created_at'],
            "last_updated": analyzer.metadata['last_updated'],
            "performance_metrics": analyzer.metadata['performance_metrics'],
            "supported_languages": ["en", "fa"],
            "supported_markets": ["stock", "forex", "crypto"],
            "supported_regions": ["US", "EU", "ASIA", "ME", "global"]
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/events")
async def analyze_events(text: str):
    """Analyze text for market events and their sentiment impact."""
    try:
        # Detect events
        events = event_detector.detect_events(text)
        
        # Analyze sentiment for each event
        for event in events:
            sentiment_result = analyzer.analyze(event["text"])
            event["sentiment_impact"] = sentiment_result["sentiment_score"]
        
        return {
            "events": events,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing events: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/rumors")
async def analyze_rumors(messages: List[dict], time_window: Optional[int] = 12):
    """Analyze messages for potential rumors."""
    try:
        # Convert string timestamps to datetime objects
        for msg in messages:
            if isinstance(msg["timestamp"], str):
                msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
        
        # Detect rumors
        rumors = rumor_detector.detect_rumors(messages, time_window)
        
        # Create visualization
        fig = create_rumor_analysis_visualization(rumors)
        
        return {
            "rumors": rumors,
            "visualization": fig.to_json(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing rumors: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/timeline")
async def get_timeline(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    """Get sentiment timeline with event markers."""
    try:
        # Get sentiment data (mock for now)
        sentiment_data = pd.DataFrame({
            "timestamp": pd.date_range(start=start_time or datetime.now() - timedelta(days=7),
                                     end=end_time or datetime.now(),
                                     freq="H"),
            "sentiment_score": np.random.normal(0, 1, 169)  # 7 days * 24 hours
        })
        
        # Get events (mock for now)
        events = [
            {
                "timestamp": datetime.now() - timedelta(days=3),
                "text": "Central Bank Meeting",
                "type": "central_bank",
                "sentiment_impact": -0.5
            },
            {
                "timestamp": datetime.now() - timedelta(days=1),
                "text": "Earnings Report",
                "type": "earnings",
                "sentiment_impact": 0.7
            }
        ]
        
        # Create visualization
        fig = create_timeline_visualization(events, sentiment_data)
        
        return {
            "timeline": {
                "events": events,
                "sentiment_data": sentiment_data.to_dict("records")
            },
            "visualization": fig.to_json()
        }
    except Exception as e:
        logger.error(f"Error generating timeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alerts/rumors")
async def get_rumor_alerts(threshold: Optional[float] = 0.7):
    """Get alerts for high-confidence rumors."""
    try:
        # Get recent rumors (mock for now)
        rumors = [
            {
                "confidence": 0.85,
                "messages": [
                    {"text": "Rumor about company X", "timestamp": datetime.now() - timedelta(hours=1)},
                    {"text": "Similar rumor about X", "timestamp": datetime.now() - timedelta(hours=2)}
                ],
                "time_span": timedelta(hours=1),
                "pattern_matches": 2,
                "verdict": "Likely manipulation"
            }
        ]
        
        # Filter high-confidence rumors
        alerts = [
            create_rumor_alert(rumor, threshold)
            for rumor in rumors
            if rumor["confidence"] >= threshold
        ]
        
        return {
            "alerts": [alert for alert in alerts if alert is not None],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating rumor alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FinSentrix (FSX) API",
        version="1.0.0",
        description="Global Financial Market Sentiment Analysis API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FinSentrix (FSX) API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# Rate limiting setup
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)

# Health check endpoint
@app.get("/health")
@RateLimiter(times=60, minutes=1)
async def health_check():
    return {"status": "healthy"}

# Initialize core components
sentiment_analyzer = SentimentAnalyzer()
event_detector = EventDetector()
rumor_analyzer = RumorAnalyzer()

# Pydantic models
class TextAnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = "en"

class BatchAnalysisRequest(BaseModel):
    texts: List[str]
    language: Optional[str] = "en"

class MarketDataRequest(BaseModel):
    ticker: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# Sentiment Analysis Endpoints
@app.post("/api/sentiment/analyze")
async def analyze_sentiment(request: TextAnalysisRequest, db: Session = Depends(get_db)):
    try:
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze_text(request.text, request.language)
        
        # Save to database
        analysis = Analysis(
            text=request.text,
            sentiment_scores=sentiment,
            language=request.language,
            timestamp=datetime.now()
        )
        db.add(analysis)
        db.commit()
        
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sentiment/batch")
async def analyze_batch(request: BatchAnalysisRequest, db: Session = Depends(get_db)):
    try:
        sentiments = sentiment_analyzer.analyze_batch(request.texts, request.language)
        
        # Save to database
        analyses = [
            Analysis(
                text=text,
                sentiment_scores=sentiment,
                language=request.language,
                timestamp=datetime.now()
            )
            for text, sentiment in zip(request.texts, sentiments)
        ]
        db.bulk_save_objects(analyses)
        db.commit()
        
        return {"sentiments": sentiments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Event Detection Endpoints
@app.post("/api/events/detect")
async def detect_events(request: TextAnalysisRequest, db: Session = Depends(get_db)):
    try:
        events = event_detector.detect_events(request.text)
        
        # Save to database
        db_events = [
            Event(
                text=event["text"],
                event_type=event["type"],
                confidence=event["confidence"],
                timestamp=datetime.fromisoformat(event["timestamp"])
            )
            for event in events
        ]
        db.bulk_save_objects(db_events)
        db.commit()
        
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/events/timeline")
async def get_event_timeline(request: BatchAnalysisRequest):
    try:
        timeline = event_detector.get_event_timeline(request.texts)
        return {"timeline": timeline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rumor Analysis Endpoints
@app.post("/api/rumors/detect")
async def detect_rumors(request: BatchAnalysisRequest, db: Session = Depends(get_db)):
    try:
        timestamps = [datetime.now()] * len(request.texts)
        rumors = rumor_analyzer.detect_rumors(request.texts, timestamps)
        
        # Save to database
        db_rumors = [
            Rumor(
                texts=rumor["texts"],
                spread_rate=rumor["spread_rate"],
                confidence=rumor["confidence"],
                key_phrases=rumor["key_phrases"],
                timestamp=datetime.now()
            )
            for rumor in rumors
        ]
        db.bulk_save_objects(db_rumors)
        db.commit()
        
        return {"rumors": rumors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Market Data Endpoints
@app.post("/api/market/data")
async def get_market_data(request: MarketDataRequest, db: Session = Depends(get_db)):
    try:
        processor = MarketProcessor(request.ticker, request.start_date, request.end_date)
        market_data = processor.get_market_summary()
        
        # Save to database
        db_market_data = MarketData(
            ticker=request.ticker,
            data=market_data,
            timestamp=datetime.now()
        )
        db.add(db_market_data)
        db.commit()
        
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/indicators/{ticker}")
async def get_technical_indicators(ticker: str):
    try:
        processor = MarketProcessor(ticker)
        indicators = processor.calculate_technical_indicators()
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 