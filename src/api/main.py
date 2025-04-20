from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging

from utils.text_processor import TextProcessor
from utils.sentiment_analyzer import SentimentAnalyzer, SentimentResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Persian Financial Sentiment Analysis API")

# Initialize processors
text_processor = TextProcessor()
sentiment_analyzer = SentimentAnalyzer()

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

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Persian Financial Sentiment Analysis API",
        "version": "1.0.0",
        "description": "Analyzes sentiment in Persian financial texts"
    }

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment for a single text."""
    try:
        # Preprocess text
        processed_text = text_processor.process_text(request.text)
        if not processed_text:
            raise HTTPException(status_code=400, detail="Text preprocessing failed")
        
        # Analyze sentiment
        result = sentiment_analyzer.analyze(processed_text)
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
            # Preprocess text
            processed_text = text_processor.process_text(text)
            if not processed_text:
                logger.warning(f"Text preprocessing failed for: {text}")
                continue
            
            # Analyze sentiment
            result = sentiment_analyzer.analyze(processed_text)
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