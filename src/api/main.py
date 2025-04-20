from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import List, Optional
import jwt
from datetime import datetime, timedelta
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from ..models.sentiment_analyzer import SentimentAnalyzer
from ..utils.text_processor import FinancialTextProcessor

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@limiter.limit("10/minute")
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
@limiter.limit("5/minute")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 