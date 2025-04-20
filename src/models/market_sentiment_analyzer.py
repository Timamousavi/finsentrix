from typing import Dict, List, Optional, Union
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from ..utils.text_processor import FinancialTextProcessor

class MarketSentimentAnalyzer:
    """A specialized sentiment analyzer for different financial markets."""
    
    def __init__(
        self,
        model_name: str = "HooshvareLab/bert-fa-base-uncased-sentiment-snappfood",
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """Initialize the market sentiment analyzer.
        
        Args:
            model_name: Name of the pre-trained model to use
            device: Device to run the model on (cuda or cpu)
        """
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
        self.text_processor = FinancialTextProcessor()
        self.logger = logging.getLogger(__name__)
        
        # Market-specific sentiment thresholds
        self.market_thresholds = {
            'stock': {
                'positive': 0.6,
                'negative': 0.4,
                'confidence': 0.7
            },
            'forex': {
                'positive': 0.65,
                'negative': 0.35,
                'confidence': 0.75
            },
            'crypto': {
                'positive': 0.7,
                'negative': 0.3,
                'confidence': 0.8
            }
        }
        
    def detect_market_type(self, text: str) -> str:
        """Detect the market type from the text content.
        
        Args:
            text: Input text to analyze
            
        Returns:
            str: Detected market type ('stock', 'forex', 'crypto')
        """
        processed = self.text_processor.process_text(text)
        term_counts = processed['term_frequencies']
        
        # Count market-specific terms
        market_scores = {
            'stock': sum(term_counts.get(term, 0) for term in 
                        self.text_processor.financial_terms['persian']['stock'] +
                        self.text_processor.financial_terms['english']['stock']),
            'forex': sum(term_counts.get(term, 0) for term in 
                        self.text_processor.financial_terms['persian']['forex'] +
                        self.text_processor.financial_terms['english']['forex']),
            'crypto': sum(term_counts.get(term, 0) for term in 
                         self.text_processor.financial_terms['persian']['crypto'] +
                         self.text_processor.financial_terms['english']['crypto'])
        }
        
        # Return market with highest term count
        return max(market_scores.items(), key=lambda x: x[1])[0]
    
    def analyze_sentiment(
        self,
        text: str,
        market_type: Optional[str] = None
    ) -> Dict[str, Union[str, float]]:
        """Analyze sentiment of financial text with market-specific thresholds.
        
        Args:
            text: Input text to analyze
            market_type: Optional market type override
            
        Returns:
            Dict containing sentiment label and confidence score
        """
        # Detect market type if not provided
        if market_type is None:
            market_type = self.detect_market_type(text)
            self.logger.info(f"Detected market type: {market_type}")
        
        # Get market-specific thresholds
        thresholds = self.market_thresholds[market_type]
        
        # Process and tokenize text
        processed_text = self.text_processor.process_text(text)['normalized_text']
        inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)[0].cpu().numpy()
            
        # Get confidence score
        confidence = float(np.max(scores))
        
        # Determine sentiment based on market-specific thresholds
        if confidence < thresholds['confidence']:
            sentiment = 'neutral'
        elif scores[2] > thresholds['positive']:  # Positive class
            sentiment = 'positive'
        elif scores[0] > thresholds['negative']:  # Negative class
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'market_type': market_type,
            'scores': {
                'positive': float(scores[2]),
                'neutral': float(scores[1]),
                'negative': float(scores[0])
            }
        }
    
    def analyze_batch(
        self,
        texts: List[str],
        market_types: Optional[List[str]] = None
    ) -> List[Dict[str, Union[str, float]]]:
        """Analyze sentiment for a batch of texts.
        
        Args:
            texts: List of texts to analyze
            market_types: Optional list of market types
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        for i, text in enumerate(texts):
            market_type = market_types[i] if market_types else None
            results.append(self.analyze_sentiment(text, market_type))
        return results
    
    def get_market_insights(
        self,
        texts: List[str],
        market_type: Optional[str] = None
    ) -> Dict[str, Union[float, Dict[str, float]]]:
        """Get market-specific insights from a collection of texts.
        
        Args:
            texts: List of texts to analyze
            market_type: Optional market type override
            
        Returns:
            Dict containing market insights
        """
        # Analyze all texts
        results = self.analyze_batch(texts, [market_type] * len(texts) if market_type else None)
        
        # Calculate market sentiment distribution
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        total_confidence = 0.0
        
        for result in results:
            sentiment_counts[result['sentiment']] += 1
            total_confidence += result['confidence']
            
        # Calculate average confidence
        avg_confidence = total_confidence / len(texts)
        
        # Calculate sentiment percentages
        total = len(texts)
        sentiment_percentages = {
            sentiment: count / total * 100
            for sentiment, count in sentiment_counts.items()
        }
        
        # Determine overall market sentiment
        if sentiment_percentages['positive'] > 60:
            overall_sentiment = 'bullish'
        elif sentiment_percentages['negative'] > 60:
            overall_sentiment = 'bearish'
        else:
            overall_sentiment = 'neutral'
            
        return {
            'overall_sentiment': overall_sentiment,
            'sentiment_distribution': sentiment_percentages,
            'average_confidence': avg_confidence,
            'market_type': market_type or self.detect_market_type(' '.join(texts)),
            'total_samples': total
        } 