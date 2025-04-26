import logging
from typing import Dict, Optional
from dataclasses import dataclass
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Container for sentiment analysis results."""
    sentiment: str
    confidence: float
    details: Dict[str, float]

class SentimentAnalyzer:
    """Analyzes sentiment in Persian financial texts."""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        
        # Initialize lexicons
        self.positive_terms = {
            # Market trend terms
            'صعودی': 1.0, 'رشد': 0.8, 'افزایش': 0.8, 'سودآور': 0.9,
            'مثبت': 0.7, 'بهبود': 0.6, 'توسعه': 0.5, 'پیشرفت': 0.6,
            'بالا': 0.7, 'قوی': 0.7, 'پایدار': 0.6, 'موفق': 0.8,
            
            # Financial performance terms
            'سود': 0.8, 'درآمد': 0.7, 'بازده': 0.8, 'ارزش‌افزوده': 0.9,
            'سودآوری': 0.9, 'بهره‌وری': 0.7, 'مازاد': 0.8, 'مطلوب': 0.7,
            
            # Market sentiment terms
            'امیدوار': 0.6, 'اطمینان': 0.7, 'برتر': 0.7, 'مطلوب': 0.7,
            'خوب': 0.6, 'عالی': 0.8, 'مناسب': 0.6
        }
        
        self.negative_terms = {
            # Market trend terms
            'نزولی': -1.0, 'کاهش': -0.8, 'افت': -0.8, 'زیان': -0.9,
            'منفی': -0.7, 'ضعیف': -0.6, 'سقوط': -0.9, 'پایین': -0.7,
            'ناپایدار': -0.6, 'شکست': -0.8, 'مشکل': -0.6,
            
            # Financial risk terms
            'ریسک': -0.7, 'بدهی': -0.6, 'ضرر': -0.9, 'زیان‌ده': -0.9,
            'بحران': -0.8, 'تورم': -0.7, 'کسری': -0.8, 'مشکل': -0.6,
            
            # Market sentiment terms
            'نگران': -0.6, 'تردید': -0.7, 'چالش': -0.5, 'نامطلوب': -0.7,
            'ضعیف': -0.6, 'بد': -0.7
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'بسیار': 1.5, 'خیلی': 1.3, 'کاملاً': 1.4, 'به‌شدت': 1.5,
            'اندکی': 0.7, 'کمی': 0.8, 'نسبتاً': 0.9, 'تاحدودی': 0.8,
            'قابل‌توجه': 1.2, 'چشمگیر': 1.3, 'مشهود': 1.2, 'محسوس': 1.1
        }
        
        # Negation terms
        self.negation_terms = {
            'نه', 'نیست', 'نبود', 'نخواهد', 'نمی', 'نشد', 'نکرد',
            'بدون', 'غیر', 'نا', 'نمی‌تواند', 'نمی‌شود'
        }
        
        # Market indicators
        self.market_indicators = {
            'شاخص': 0.5, 'حجم': 0.4, 'قیمت': 0.4, 'سهام': 0.3,
            'بورس': 0.3, 'بازار': 0.3, 'معاملات': 0.3
        }
    
    def _find_term_with_score(self, text: str, term_dict: Dict[str, float]) -> Dict[str, float]:
        """Find terms and their scores in the text."""
        found_terms = {}
        words = self.text_processor.tokenize(text)
        for term, score in term_dict.items():
            if term in words:
                found_terms[term] = score
        return found_terms
    
    def _check_for_negation(self, text: str, term: str) -> bool:
        """Check if a term is negated."""
        words = self.text_processor.tokenize(text)
        try:
            term_idx = words.index(term)
            # Check 3 words before the term
            start = max(0, term_idx - 3)
            context = words[start:term_idx]
            return any(neg in context for neg in self.negation_terms)
        except ValueError:
            return False
    
    def _find_intensity_modifier(self, text: str, term: str) -> float:
        """Find intensity modifiers that affect a term."""
        words = self.text_processor.tokenize(text)
        try:
            term_idx = words.index(term)
            # Check two words before the term
            start = max(0, term_idx - 2)
            context = words[start:term_idx]
            
            max_modifier = 1.0
            for word in context:
                if word in self.intensity_modifiers:
                    max_modifier = max(max_modifier, self.intensity_modifiers[word])
            return max_modifier
        except ValueError:
            return 1.0
    
    def _analyze_numbers(self, text: str) -> float:
        """Analyze numerical values in the text for sentiment impact."""
        words = self.text_processor.tokenize(text)
        sentiment_score = 0.0
        
        for i, word in enumerate(words):
            if word.isdigit() or (word.replace(',', '').isdigit()):
                try:
                    # Get the number value
                    num = float(word.replace(',', ''))
                    
                    # Check context around the number
                    context = words[max(0, i-2):min(len(words), i+3)]
                    
                    # Check for percentage terms
                    if 'درصد' in context:
                        if num > 0:
                            sentiment_score += min(num/100, 1.0)  # Cap at 1.0
                        else:
                            sentiment_score -= min(abs(num)/100, 1.0)
                    
                    # Check for market indicators
                    for indicator in self.market_indicators:
                        if indicator in context:
                            if num > 0:
                                sentiment_score += self.market_indicators[indicator]
                            else:
                                sentiment_score -= self.market_indicators[indicator]
                except ValueError:
                    continue
        
        return sentiment_score
    
    def analyze(self, text: str) -> Optional[SentimentResult]:
        """
        Analyze the sentiment of Persian financial text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentResult object containing the analysis or None if processing fails
        """
        try:
            # Find sentiment terms
            positive_matches = self._find_term_with_score(text, self.positive_terms)
            negative_matches = self._find_term_with_score(text, self.negative_terms)
            
            # Calculate sentiment scores
            sentiment_scores = []
            term_details = {}
            
            # Process positive terms
            for term, base_score in positive_matches.items():
                is_negated = self._check_for_negation(text, term)
                intensity = self._find_intensity_modifier(text, term)
                final_score = base_score * intensity * (-1 if is_negated else 1)
                sentiment_scores.append(final_score)
                term_details[term] = final_score
            
            # Process negative terms
            for term, base_score in negative_matches.items():
                is_negated = self._check_for_negation(text, term)
                intensity = self._find_intensity_modifier(text, term)
                final_score = base_score * intensity * (-1 if is_negated else 1)
                sentiment_scores.append(final_score)
                term_details[term] = final_score
            
            # Analyze numbers
            number_sentiment = self._analyze_numbers(text)
            if number_sentiment != 0:
                sentiment_scores.append(number_sentiment)
                term_details['numerical_analysis'] = number_sentiment
            
            # Calculate overall sentiment
            if not sentiment_scores:
                return SentimentResult(
                    sentiment="neutral",
                    confidence=0.5,
                    details={}
                )
            
            # Calculate average sentiment score
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
            
            # Determine sentiment and confidence
            if avg_score > 0.1:
                sentiment = "positive"
                confidence = min(abs(avg_score), 1.0)
            elif avg_score < -0.1:
                sentiment = "negative"
                confidence = min(abs(avg_score), 1.0)
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return SentimentResult(
                sentiment=sentiment,
                confidence=confidence,
                details=term_details
            )
            
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return None 