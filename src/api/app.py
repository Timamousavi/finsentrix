"""
FastAPI application for serving the sentiment analysis model.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from models.sentiment_analyzer import SentimentAnalyzer
from utils.text_processor import PersianTextProcessor

app = FastAPI(
    title="Iranian Stock Sentiment Analysis API",
    description="API for analyzing sentiment in Persian financial text",
    version="1.0.0"
)

# Initialize components
text_processor = PersianTextProcessor()
sentiment_analyzer = None  # Will be loaded on startup

class TextInput(BaseModel):
    """Input model for single text analysis."""
    text: str

class BatchInput(BaseModel):
    """Input model for batch text analysis."""
    texts: List[str]

class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""
    sentiment: str
    confidence: float
    processed_text: Optional[str] = None
    tokens: Optional[List[str]] = None
    financial_terms: Optional[dict] = None

@app.on_event("startup")
async def startup_event():
    """Load the sentiment analysis model on startup."""
    global sentiment_analyzer
    try:
        model_path = Path(project_root) / "models" / "sentiment_model.joblib"
        vectorizer_path = Path(project_root) / "models" / "vectorizer.joblib"
        
        if model_path.exists() and vectorizer_path.exists():
            sentiment_analyzer = SentimentAnalyzer.load_model(
                str(model_path),
                str(vectorizer_path)
            )
        else:
            # Initialize with default model if no saved model exists
            sentiment_analyzer = SentimentAnalyzer()
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        sentiment_analyzer = SentimentAnalyzer()

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Iranian Stock Sentiment Analysis API",
        "version": "1.0.0",
        "description": "API for analyzing sentiment in Persian financial text"
    }

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(input: TextInput):
    """
    Analyze sentiment for a single text.
    
    Args:
        input (TextInput): Input text to analyze
        
    Returns:
        SentimentResponse: Analysis results
    """
    try:
        # Process text
        processed = text_processor.process_text(input.text)
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.predict(input.text)
        
        return SentimentResponse(
            sentiment=sentiment['sentiment'],
            confidence=sentiment['confidence'],
            processed_text=processed['normalized_text'],
            tokens=processed['tokens'],
            financial_terms=processed['financial_terms']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/batch", response_model=List[SentimentResponse])
async def analyze_sentiment_batch(input: BatchInput):
    """
    Analyze sentiment for multiple texts.
    
    Args:
        input (BatchInput): List of texts to analyze
        
    Returns:
        List[SentimentResponse]: List of analysis results
    """
    try:
        results = []
        for text in input.texts:
            # Process text
            processed = text_processor.process_text(text)
            
            # Analyze sentiment
            sentiment = sentiment_analyzer.predict(text)
            
            results.append(SentimentResponse(
                sentiment=sentiment['sentiment'],
                confidence=sentiment['confidence'],
                processed_text=processed['normalized_text'],
                tokens=processed['tokens'],
                financial_terms=processed['financial_terms']
            ))
            
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 