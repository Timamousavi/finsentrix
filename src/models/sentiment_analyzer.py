"""
Basic sentiment analyzer for financial text.
"""
import logging
from datetime import datetime
from typing import Dict, Tuple
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Simple sentiment analyzer for Persian financial texts."""
    
    def __init__(self):
        """Initialize the sentiment analyzer with basic Persian financial sentiment words."""
        self.logger = logging.getLogger(__name__)
        
        # Basic Persian financial sentiment words
        self.positive_words = {
            'مثبت', 'رشد', 'سود', 'افزایش', 'موفق', 'خوب',
            'قوی', 'بهبود', 'پیشرفت', 'توسعه', 'برتر'
        }
        
        self.negative_words = {
            'منفی', 'کاهش', 'ضرر', 'زیان', 'ضعیف', 'بد',
            'سقوط', 'افت', 'بحران', 'ریسک', 'خطر'
        }
        
        self.neutral_words = {
            'ثابت', 'معامله', 'بازار', 'سهام', 'قیمت',
            'شاخص', 'نماد', 'حجم', 'ارزش', 'معاملات'
        }

    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze the sentiment of given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Tuple[str, float]: Sentiment label and confidence score
        """
        try:
            # Convert to lowercase for consistency
            words = set(re.findall(r'\b\w+\b', text))
            
            # Count sentiment words
            pos_count = len(words.intersection(self.positive_words))
            neg_count = len(words.intersection(self.negative_words))
            neu_count = len(words.intersection(self.neutral_words))
            
            total = pos_count + neg_count + neu_count
            if total == 0:
                return "neutral", 0.5
            
            # Calculate sentiment scores
            pos_score = pos_count / total
            neg_score = neg_count / total
            neu_score = neu_count / total
            
            # Determine sentiment
            max_score = max(pos_score, neg_score, neu_score)
            if max_score == pos_score:
                return "positive", pos_score
            elif max_score == neg_score:
                return "negative", neg_score
            else:
                return "neutral", neu_score
                
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return "neutral", 0.5  # Default to neutral if analysis fails

    def predict(self, texts):
        """Mock sentiment prediction."""
        # For testing, return positive sentiment with high confidence
        labels = [1] * len(texts)  # 1 for positive
        probabilities = [[0.15, 0.85]] * len(texts)  # [negative_prob, positive_prob]
        return labels, probabilities

    def analyze_text(self, text):
        """Mock sentiment analysis."""
        return {
            'sentiment_score': 0.85,
            'sentiment': 'positive',
            'confidence': 0.85
        } 