from typing import Dict, List, Optional, Tuple
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from textblob import TextBlob
import torch

class SentimentAnalyzer:
    def __init__(self, model_name: str = "finiteautomata/bertweet-base-sentiment-analysis"):
        """Initialize the sentiment analyzer with a pre-trained model."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1
        )
        
    def analyze_text(self, text: str, language: str = "en") -> Dict[str, float]:
        """Analyze sentiment of a given text.
        
        Args:
            text: Input text to analyze
            language: Language of the text (default: "en")
            
        Returns:
            Dictionary containing sentiment scores
        """
        # Basic text preprocessing
        text = text.strip()
        
        # Get model prediction
        result = self.sentiment_pipeline(text)[0]
        
        # Calculate confidence scores
        scores = {
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 0.0
        }
        
        if result["label"] == "POS":
            scores["positive"] = result["score"]
            scores["negative"] = (1 - result["score"]) / 2
            scores["neutral"] = (1 - result["score"]) / 2
        elif result["label"] == "NEG":
            scores["negative"] = result["score"]
            scores["positive"] = (1 - result["score"]) / 2
            scores["neutral"] = (1 - result["score"]) / 2
        else:  # NEU
            scores["neutral"] = result["score"]
            scores["positive"] = (1 - result["score"]) / 2
            scores["negative"] = (1 - result["score"]) / 2
            
        return scores
        
    def analyze_batch(self, texts: List[str], language: str = "en") -> List[Dict[str, float]]:
        """Analyze sentiment of multiple texts.
        
        Args:
            texts: List of texts to analyze
            language: Language of the texts (default: "en")
            
        Returns:
            List of dictionaries containing sentiment scores
        """
        return [self.analyze_text(text, language) for text in texts]
        
    def get_market_sentiment(self, texts: List[str], weights: Optional[List[float]] = None) -> float:
        """Calculate overall market sentiment from multiple texts.
        
        Args:
            texts: List of texts to analyze
            weights: Optional weights for each text (default: equal weights)
            
        Returns:
            Overall market sentiment score (-1 to 1)
        """
        if not texts:
            return 0.0
            
        if weights is None:
            weights = [1.0 / len(texts)] * len(texts)
            
        sentiments = self.analyze_batch(texts)
        weighted_scores = []
        
        for sentiment, weight in zip(sentiments, weights):
            score = sentiment["positive"] - sentiment["negative"]
            weighted_scores.append(score * weight)
            
        return np.sum(weighted_scores)
        
    def get_sentiment_trend(self, texts: List[str], window_size: int = 5) -> List[float]:
        """Calculate sentiment trend over time using a sliding window.
        
        Args:
            texts: List of texts in chronological order
            window_size: Size of the sliding window (default: 5)
            
        Returns:
            List of sentiment scores over time
        """
        if not texts:
            return []
            
        sentiments = self.analyze_batch(texts)
        scores = [s["positive"] - s["negative"] for s in sentiments]
        
        # Apply sliding window
        trend = []
        for i in range(len(scores)):
            start = max(0, i - window_size + 1)
            window = scores[start:i+1]
            trend.append(np.mean(window))
            
        return trend 