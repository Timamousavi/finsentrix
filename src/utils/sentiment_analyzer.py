import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Container for sentiment analysis results."""
    sentiment: str
    confidence: float
    details: Dict[str, float]
    original_text: str
    processed_text: str

class SentimentAnalyzer:
    """Analyzes sentiment in Persian financial texts."""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        
        # Initialize lexicons
        self.positive_terms = {
            # Market trend terms
            'صعودی': 1.0, 'رشد': 0.8, 'افزایش': 0.8, 'سودآور': 0.9,
            'مثبت': 0.7, 'بهبود': 0.6, 'توسعه': 0.5, 'پیشرفت': 0.6,
            
            # Financial performance terms
            'سود': 0.8, 'درآمد': 0.7, 'بازده': 0.8, 'ارزش‌افزوده': 0.9,
            'سودآوری': 0.9, 'بهره‌وری': 0.7,
            
            # Market sentiment terms
            'امیدوار': 0.6, 'اطمینان': 0.7, 'قوی': 0.7, 'پایدار': 0.6,
            'موفق': 0.8, 'برتر': 0.7
        }
        
        self.negative_terms = {
            # Market trend terms
            'نزولی': -1.0, 'کاهش': -0.8, 'افت': -0.8, 'زیان': -0.9,
            'منفی': -0.7, 'ضعیف': -0.6, 'سقوط': -0.9,
            
            # Financial risk terms
            'ریسک': -0.7, 'بدهی': -0.6, 'ضرر': -0.9, 'زیان‌ده': -0.9,
            'بحران': -0.8, 'تورم': -0.7,
            
            # Market sentiment terms
            'نگران': -0.6, 'تردید': -0.7, 'ناپایدار': -0.6, 'شکست': -0.8,
            'مشکل': -0.6, 'چالش': -0.5
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'بسیار': 1.5, 'خیلی': 1.3, 'کاملاً': 1.4, 'به‌شدت': 1.5,
            'اندکی': 0.7, 'کمی': 0.8, 'نسبتاً': 0.9,
            'قابل‌توجه': 1.2, 'چشمگیر': 1.3
        }
        
        # Negation terms
        self.negation_terms = {'نه', 'نیست', 'نبود', 'نخواهد', 'نمی', 'نشد', 'نکرد'}
        
    def _find_term_with_score(self, text: str, term_dict: Dict[str, float]) -> List[Tuple[str, float]]:
        """Find terms and their scores in the text."""
        found_terms = []
        for term, score in term_dict.items():
            if term in text:
                found_terms.append((term, score))
        return found_terms
    
    def _check_for_negation(self, text: str, term_position: int) -> bool:
        """Check if a term is negated by looking at surrounding context."""
        # Get the context window (5 words before the term)
        words = text.split()
        start = max(0, term_position - 5)
        context = words[start:term_position]
        
        # Check if any negation terms appear in the context
        return any(neg_term in context for neg_term in self.negation_terms)
    
    def _find_intensity_modifiers(self, text: str, term_position: int) -> float:
        """Find intensity modifiers that affect a term."""
        words = text.split()
        # Check two words before the term
        start = max(0, term_position - 2)
        context = words[start:term_position]
        
        # Return the strongest modifier if found, otherwise return 1.0
        max_modifier = 1.0
        for word in context:
            if word in self.intensity_modifiers:
                max_modifier = max(max_modifier, self.intensity_modifiers[word])
        return max_modifier
    
    def analyze_text(self, text: str) -> Optional[SentimentResult]:
        """
        Analyze the sentiment of Persian financial text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentResult object containing the analysis or None if processing fails
        """
        try:
            # Preprocess text
            processed_text = self.text_processor.process_text(text)
            if not processed_text:
                logger.warning("Text processing failed")
                return None
            
            # Find sentiment terms
            words = processed_text.split()
            sentiment_scores = []
            term_details = {}
            
            # Analyze each word in context
            for i, _ in enumerate(words):
                current_text = ' '.join(words[max(0, i-5):min(len(words), i+6)])
                
                # Check positive terms
                for term, base_score in self._find_term_with_score(current_text, self.positive_terms):
                    # Check for negation
                    is_negated = self._check_for_negation(current_text, i)
                    # Find intensity modifiers
                    intensity = self._find_intensity_modifiers(current_text, i)
                    
                    # Calculate final score
                    final_score = base_score * intensity * (-1 if is_negated else 1)
                    sentiment_scores.append(final_score)
                    term_details[term] = final_score
                
                # Check negative terms
                for term, base_score in self._find_term_with_score(current_text, self.negative_terms):
                    # Check for negation
                    is_negated = self._check_for_negation(current_text, i)
                    # Find intensity modifiers
                    intensity = self._find_intensity_modifiers(current_text, i)
                    
                    # Calculate final score
                    final_score = base_score * intensity * (-1 if is_negated else 1)
                    sentiment_scores.append(final_score)
                    term_details[term] = final_score
            
            # Calculate overall sentiment
            if not sentiment_scores:
                # No sentiment terms found
                return SentimentResult(
                    sentiment="neutral",
                    confidence=0.5,
                    details={},
                    original_text=text,
                    processed_text=processed_text
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
                details=term_details,
                original_text=text,
                processed_text=processed_text
            )
            
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            for i, word in enumerate(words):
                if skip_next:
                    skip_next = False
                    continue
                
                # Check for negation
                is_negated = False
                if i > 0 and any(neg in words[i-1] for neg in self.negation_words):
                    is_negated = True
                
                # Get base sentiment score
                score = 0.0
                if word in self.positive_words:
                    score = self.positive_words[word]
                elif word in self.negative_words:
                    score = self.negative_words[word]
                
                # Apply negation
                if is_negated:
                    score *= -1
                
                # Check for intensifiers
                if i > 0 and words[i-1] in self.intensifiers:
                    score *= self.intensifiers[words[i-1]]
                
                if score != 0.0:
                    scores.append(score)
            
            if not scores:
                return SentimentResult(
                    sentiment="neutral",
                    confidence=1.0,
                    details={"neutral": 1.0}
                )
            
            # Calculate final sentiment
            avg_score = sum(scores) / len(scores)
            abs_score = abs(avg_score)
            
            if abs_score < 0.3:
                sentiment = "neutral"
                confidence = 1.0 - abs_score
            else:
                sentiment = "positive" if avg_score > 0 else "negative"
                confidence = min(abs_score, 1.0)
            
            # Calculate sentiment distribution
            details = {
                "positive": max(0, avg_score) if sentiment == "positive" else 0,
                "negative": abs(min(0, avg_score)) if sentiment == "negative" else 0,
                "neutral": 1.0 - confidence
            }
            
            return SentimentResult(
                sentiment=sentiment,
                confidence=confidence,
                details=details
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return None 