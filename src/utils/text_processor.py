"""
Basic text processing module for financial content.
"""
from typing import Optional, List
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
        self.word_pattern = re.compile(r'[\u0600-\u06FF\s]+')
        
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
    
    def tokenize(self, text: str) -> List[str]:
        """Split text into words."""
        # First normalize the text
        text = self.normalize_whitespace(text)
        # Remove punctuation
        text = self.remove_punctuation(text)
        # Split on whitespace and filter out empty strings
        return [word for word in text.split() if word]
    
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