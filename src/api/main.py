from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from utils.text_processor import TextProcessor
from utils.sentiment_analyzer import SentimentAnalyzer, SentimentResult
from services.financial_data import FinancialDataService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Persian Financial Sentiment Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="src/api/templates")

# Initialize processors
text_processor = TextProcessor()
sentiment_analyzer = SentimentAnalyzer()

# Initialize services
financial_service = FinancialDataService()

class SentimentRequest(BaseModel):
    text: str
    api_key: Optional[str] = None

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    details: Dict[str, float]

class BatchSentimentRequest(BaseModel):
    texts: List[str]
    api_key: Optional[str] = None

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard page."""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment for a single text."""
    try:
        # Analyze sentiment directly
        result = sentiment_analyzer.analyze(request.text)
        if not result:
            raise HTTPException(status_code=500, detail="Sentiment analysis failed")
        
        return SentimentResponse(
            text=request.text,
            sentiment=result.sentiment,
            confidence=result.confidence,
            details=result.details
        )
    
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/batch", response_model=BatchSentimentResponse)
async def analyze_batch_sentiment(request: BatchSentimentRequest):
    """Analyze sentiment for multiple texts."""
    try:
        results = []
        for text in request.texts:
            # Analyze sentiment directly
            result = sentiment_analyzer.analyze(text)
            if not result:
                logger.warning(f"Sentiment analysis failed for: {text}")
                continue
            
            results.append(SentimentResponse(
                text=text,
                sentiment=result.sentiment,
                confidence=result.confidence,
                details=result.details
            ))
        
        if not results:
            raise HTTPException(status_code=400, detail="All texts failed processing")
        
        return BatchSentimentResponse(results=results)
    
    except Exception as e:
        logger.error(f"Error in batch sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/api/dashboard/real-time")
async def get_real_time_data() -> Dict[str, Any]:
    """Get real-time market data and sentiment indicators"""
    try:
        logger.info("Fetching real-time dashboard data")
        
        # For development, use mock data
        data = financial_service.generate_mock_data()
        logger.info(f"Generated mock data: {data}")
        
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error fetching real-time data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch real-time data: {str(e)}"
        ) 