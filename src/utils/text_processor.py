"""
Basic text processing module for financial content.
"""
from typing import List, Dict, Optional, Union
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessor:
    """Handles preprocessing of Persian text."""
    
    def __init__(self):
        # Common Persian punctuation and special characters
        self.punctuation = '،؛؟»«!@#$%^&*()_+-=[]{}|\\:;"\'<>,.?/~`'
        # Persian numbers
        self.persian_numbers = '۰۱۲۳۴۵۶۷۸۹'
        # Arabic numbers
        self.arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
        # English numbers
        self.english_numbers = '0123456789'
        
        # Compile regex patterns
        self.number_pattern = re.compile(f'[{self.persian_numbers}{self.arabic_numbers}{self.english_numbers}]')
        self.whitespace_pattern = re.compile(r'\s+')
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self.email_pattern = re.compile(r'\S+@\S+')
        
    def normalize_numbers(self, text: str) -> str:
        """Convert all number formats to Persian numbers."""
        # Create translation tables
        arabic_to_persian = str.maketrans(self.arabic_numbers, self.persian_numbers)
        english_to_persian = str.maketrans(self.english_numbers, self.persian_numbers)
        
        # Apply translations
        text = text.translate(arabic_to_persian)
        text = text.translate(english_to_persian)
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return self.url_pattern.sub(' ', text)
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return self.email_pattern.sub(' ', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace to single spaces and strip."""
        return self.whitespace_pattern.sub(' ', text).strip()
    
    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation marks."""
        return ''.join(char for char in text if char not in self.punctuation)
    
    def process_text(self, text: Optional[str]) -> Optional[str]:
        """
        Process Persian text by applying various preprocessing steps.
        
        Args:
            text: Input text to process
            
        Returns:
            Processed text or None if processing fails
        """
        try:
            if not text or not isinstance(text, str):
                logger.warning("Invalid input text")
                return None
            
            # Convert to string and normalize whitespace
            text = str(text)
            text = self.normalize_whitespace(text)
            
            # Skip empty strings
            if not text:
                logger.warning("Empty text after normalization")
                return None
            
            # Apply preprocessing steps
            text = self.remove_urls(text)
            text = self.remove_emails(text)
            text = self.normalize_numbers(text)
            text = self.remove_punctuation(text)
            text = self.normalize_whitespace(text)
            
            return text if text else None
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return None

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        try:
            return text.split()
        except Exception as e:
            logger.error(f"Error tokenizing text: {str(e)}")
            return [text]

    def detect_language(self, text: str) -> str:
        """Detect if the text is in Persian or English."""
        # Simple detection based on character ranges
        persian_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        english_chars = sum(1 for char in text if 'a' <= char.lower() <= 'z')
        
        if persian_chars > english_chars:
            return 'persian'
        return 'english'

    def normalize_text(self, text: str, language: str = None) -> str:
        """Normalize text based on language."""
        if language is None:
            language = self.detect_language(text)
            
        text = text.lower()
        
        # Common normalizations for both languages
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def tokenize_text(self, text: str, language: str) -> List[str]:
        """Tokenize text based on language."""
        if language == 'persian':
            return self.tokenizer.tokenize(text)
        return word_tokenize(text)

    def stem_word(self, word: str, language: str) -> str:
        """Stem word based on language."""
        if language == 'persian':
            return self.stemmer.stem(word)
        return self.english_stemmer.stem(word)

    def extract_financial_terms(self, text: str, language: str) -> Dict[str, int]:
        """Extract financial terms from text."""
        terms_freq = {}
        normalized_text = self.normalize_text(text, language)
        
        for category, terms in self.financial_terms[language].items():
            for term in terms:
                if term in normalized_text:
                    terms_freq[category] = terms_freq.get(category, 0) + 1
        
        return terms_freq

    def process_text(self, text: str) -> Dict[str, Union[str, Dict[str, int], List[str]]]:
        """Process text and return features."""
        language = self.detect_language(text)
        normalized_text = self.normalize_text(text, language)
        tokens = self.tokenize_text(normalized_text, language)
        
        # Remove stopwords and stem
        stopwords_set = self._load_stopwords()[language]
        processed_tokens = [
            self.stem_word(token, language)
            for token in tokens
            if token not in stopwords_set
        ]
        
        # Extract financial terms
        financial_terms = self.extract_financial_terms(text, language)
        
        return {
            'original_text': text,
            'normalized_text': normalized_text,
            'language': language,
            'tokens': processed_tokens,
            'financial_terms': financial_terms
        }

    def process_batch(self, texts: List[str]) -> List[Dict[str, Union[str, Dict[str, int], List[str]]]]:
        """Process multiple texts in batch."""
        return [self.process_text(text) for text in texts]

# Example usage
if __name__ == "__main__":
    processor = TextProcessor()
    
    # Persian text example
    persian_text = "قیمت سهام شرکت ایران خودرو امروز با افزایش ۵ درصدی همراه بود"
    persian_result = processor.process_text(persian_text)
    print("\nPersian Text Processing:")
    print(f"Original: {persian_result['original_text']}")
    print(f"Normalized: {persian_result['normalized_text']}")
    print(f"Financial Terms: {persian_result['financial_terms']}")
    
    # English text example
    english_text = "Tesla stock price increased by 5% today after positive earnings report"
    english_result = processor.process_text(english_text)
    print("\nEnglish Text Processing:")
    print(f"Original: {english_result['original_text']}")
    print(f"Normalized: {english_result['normalized_text']}")
    print(f"Financial Terms: {english_result['financial_terms']}") 