"""
Text processing module for Persian financial content using Hazm library.
"""
from typing import List, Dict, Optional, Union
import re
from hazm import Normalizer, Stemmer, Lemmatizer, WordTokenizer
import logging
import json
import os
from persian_tools import digits
from collections import Counter
from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FinancialTextProcessor:
    def __init__(self):
        # Initialize Persian text processing components
        self.persian_normalizer = Normalizer()
        self.persian_tokenizer = WordTokenizer()
        self.persian_stemmer = Stemmer()
        
        # Initialize English text processing components
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.english_stemmer = PorterStemmer()
        self.english_stopwords = set(stopwords.words('english'))
        
        # Load financial terms for both languages
        self.financial_terms = self._load_financial_terms()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def _load_financial_terms(self) -> Dict[str, Dict[str, List[str]]]:
        """Load financial terms for both Persian and English."""
        terms = {
            'persian': {
                # Stock Market Terms
                'price': ['قیمت', 'نرخ', 'ارزش', 'مبلغ', 'بها'],
                'increase': ['افزایش', 'صعود', 'رشد', 'بالا رفتن', 'ارتقا'],
                'decrease': ['کاهش', 'نزول', 'افت', 'پایین آمدن', 'تنزل'],
                'stock': ['سهام', 'سهم', 'بورس', 'اوراق بهادار', 'شرکت'],
                'market': ['بازار', 'بورس', 'بازار سرمایه', 'بازار سهام'],
                'company': ['شرکت', 'بنگاه', 'کارخانه', 'مجتمع', 'واحد تولیدی'],
                'profit': ['سود', 'منفعت', 'درآمد', 'عایدی', 'بهره'],
                'loss': ['زیان', 'ضرر', 'کسر', 'کسری', 'کمبود'],
                'dividend': ['سود سهام', 'سود نقدی', 'سود تقسیمی', 'سود سالانه'],
                'volume': ['حجم', 'مقدار', 'تعداد', 'میزان', 'کمیت'],
                'index': ['شاخص', 'نماگر', 'اندیکاتور', 'شاخص کل'],
                'trade': ['معامله', 'خرید و فروش', 'داد و ستد', 'مبادله'],
                'investor': ['سرمایه گذار', 'سهامدار', 'معامله گر', 'بازارگردان'],
                'capital': ['سرمایه', 'دارایی', 'ثروت', 'مال', 'پول'],
                'forecast': ['پیش بینی', 'تحلیل', 'برآورد', 'تخمین', 'پیشگویی'],
                'trend': ['روند', 'گرایش', 'جهت', 'مسیر', 'سیر'],
                'risk': ['ریسک', 'خطر', 'مخاطره', 'احتمال ضرر'],
                'return': ['بازده', 'بازگشت سرمایه', 'نرخ بازده', 'سودآوری'],
                'liquidity': ['نقدینگی', 'نقدشوندگی', 'سیالیت', 'قابلیت نقدشوندگی'],
                'volatility': ['نوسان', 'تغییرپذیری', 'بی ثباتی', 'تلاطم'],
                
                # Forex Terms
                'forex': ['فارکس', 'ارز', 'نرخ ارز', 'بازار ارز', 'مبادلات ارزی'],
                'currency': ['ارز', 'واحد پول', 'پول خارجی', 'ارز خارجی'],
                'exchange_rate': ['نرخ تبدیل', 'نرخ مبادله', 'قیمت ارز', 'نرخ برابری'],
                'pair': ['جفت ارز', 'زوج ارز', 'ارز پایه', 'ارز متقابل'],
                'pip': ['پیپ', 'نقطه', 'پیپت', 'واحد تغییر'],
                'spread': ['اسپرد', 'اختلاف قیمت', 'فاصله قیمتی', 'کارمزد'],
                'leverage': ['اهرم', 'لوریج', 'ضریب اهرمی', 'نسبت اهرمی'],
                'margin': ['مارجین', 'حاشیه', 'سپرده', 'وجه الضمان'],
                'lot': ['لات', 'واحد معاملاتی', 'حجم معامله', 'سایز پوزیشن'],
                'central_bank': ['بانک مرکزی', 'بانک مرکزی', 'نهاد پولی', 'مقام پولی'],
                'technical_analysis': ['تحلیل تکنیکال', 'تحلیل فنی', 'نمودارخوانی', 'تحلیل نموداری'],
                'fundamental_analysis': ['تحلیل بنیادی', 'تحلیل فاندامنتال', 'تحلیل اقتصادی'],
                'support': ['حمایت', 'سطح حمایت', 'نقطه حمایت', 'خط حمایت'],
                'resistance': ['مقاومت', 'سطح مقاومت', 'نقطه مقاومت', 'خط مقاومت'],
                'trend_line': ['خط روند', 'خط جهت', 'خط مسیر', 'خط حرکت'],
                'indicator': ['اندیکاتور', 'نشانگر', 'شاخص', 'مقیاس'],
                
                # Cryptocurrency Terms
                'crypto': ['کریپتو', 'ارز دیجیتال', 'رمز ارز', 'پول دیجیتال'],
                'bitcoin': ['بیت کوین', 'بیت کوین', 'بیت کوین', 'BTC'],
                'blockchain': ['بلاکچین', 'زنجیره بلوکی', 'دفتر کل توزیع شده'],
                'wallet': ['کیف پول', 'والت', 'کیف پول دیجیتال', 'کیف پول رمز ارز'],
                'mining': ['ماینینگ', 'استخراج', 'استخراج رمز ارز', 'تولید رمز ارز'],
                'token': ['توکن', 'نشانه', 'توکن دیجیتال', 'دارایی دیجیتال'],
                'ico': ['عرضه اولیه', 'آی سی او', 'عرضه اولیه سکه', 'عرضه اولیه توکن'],
                'defi': ['دیفای', 'مالی غیرمتمرکز', 'مالی غیرمتمرکز', 'دیفای'],
                'nft': ['ان اف تی', 'توکن غیرقابل تعویض', 'دارایی دیجیتال منحصر به فرد'],
                'smart_contract': ['قرارداد هوشمند', 'قرارداد هوشمند', 'قرارداد خوداجرا'],
                'exchange': ['صرافی', 'صرافی رمز ارز', 'بازار رمز ارز', 'پلتفرم معاملاتی'],
                'altcoin': ['آلت کوین', 'ارز جایگزین', 'رمزارز جایگزین', 'کوین جایگزین'],
                'stablecoin': ['استیبل کوین', 'ارز پایدار', 'رمزارز پایدار', 'توکن پایدار'],
                'gas': ['گس', 'کارمزد تراکنش', 'هزینه تراکنش', 'کارمزد شبکه'],
                'hash': ['هش', 'مقدار هش', 'کد هش', 'اثر انگشت دیجیتال'],
                'node': ['نود', 'گره', 'نقطه شبکه', 'سرور شبکه'],
                'fork': ['فورک', 'انشعاب', 'شاخه جدید', 'نسخه جدید'],
                'whale': ['نهنگ', 'سرمایه گذار بزرگ', 'معامله گر بزرگ', 'دارنده بزرگ']
            },
            'english': {
                # Stock Market Terms
                'price': ['price', 'value', 'rate', 'amount', 'cost'],
                'increase': ['increase', 'rise', 'growth', 'up', 'gain'],
                'decrease': ['decrease', 'fall', 'drop', 'down', 'decline'],
                'stock': ['stock', 'share', 'equity', 'security', 'company'],
                'market': ['market', 'exchange', 'stock market', 'trading floor'],
                'company': ['company', 'firm', 'enterprise', 'corporation', 'business'],
                'profit': ['profit', 'gain', 'earnings', 'income', 'return'],
                'loss': ['loss', 'deficit', 'shortfall', 'decrease', 'reduction'],
                'dividend': ['dividend', 'payout', 'distribution', 'share of profits'],
                'volume': ['volume', 'quantity', 'amount', 'size', 'number'],
                'index': ['index', 'indicator', 'measure', 'gauge', 'benchmark'],
                'trade': ['trade', 'transaction', 'deal', 'exchange', 'bargain'],
                'investor': ['investor', 'shareholder', 'trader', 'market maker'],
                'capital': ['capital', 'asset', 'wealth', 'money', 'funds'],
                'forecast': ['forecast', 'prediction', 'analysis', 'estimate', 'projection'],
                'trend': ['trend', 'direction', 'movement', 'course', 'path'],
                'risk': ['risk', 'hazard', 'danger', 'uncertainty', 'exposure'],
                'return': ['return', 'yield', 'profit', 'gain', 'earnings'],
                'liquidity': ['liquidity', 'cash flow', 'fluidity', 'marketability'],
                'volatility': ['volatility', 'fluctuation', 'instability', 'variation'],
                
                # Forex Terms
                'forex': ['forex', 'fx', 'foreign exchange', 'currency market'],
                'currency': ['currency', 'fiat', 'money', 'legal tender'],
                'exchange_rate': ['exchange rate', 'conversion rate', 'currency rate'],
                'pair': ['currency pair', 'forex pair', 'trading pair', 'currency couple'],
                'pip': ['pip', 'point', 'percentage in point', 'price interest point'],
                'spread': ['spread', 'bid-ask spread', 'price difference', 'trading cost'],
                'leverage': ['leverage', 'margin', 'gearing', 'trading power'],
                'margin': ['margin', 'collateral', 'deposit', 'security deposit'],
                'lot': ['lot', 'position size', 'trade size', 'unit size'],
                'central_bank': ['central bank', 'federal reserve', 'monetary authority'],
                'technical_analysis': ['technical analysis', 'chart analysis', 'market analysis'],
                'fundamental_analysis': ['fundamental analysis', 'economic analysis', 'market analysis'],
                'support': ['support', 'support level', 'floor', 'price floor'],
                'resistance': ['resistance', 'resistance level', 'ceiling', 'price ceiling'],
                'trend_line': ['trend line', 'trend channel', 'price channel', 'trend indicator'],
                'indicator': ['indicator', 'technical indicator', 'market indicator', 'trading tool'],
                
                # Cryptocurrency Terms
                'crypto': ['crypto', 'cryptocurrency', 'digital currency', 'virtual currency'],
                'bitcoin': ['bitcoin', 'btc', 'digital gold', 'crypto king'],
                'blockchain': ['blockchain', 'distributed ledger', 'digital ledger', 'chain'],
                'wallet': ['wallet', 'crypto wallet', 'digital wallet', 'blockchain wallet'],
                'mining': ['mining', 'crypto mining', 'block mining', 'transaction validation'],
                'token': ['token', 'coin', 'digital asset', 'crypto asset'],
                'ico': ['ico', 'initial coin offering', 'token sale', 'crowdsale'],
                'defi': ['defi', 'decentralized finance', 'open finance', 'blockchain finance'],
                'nft': ['nft', 'non-fungible token', 'digital collectible', 'unique token'],
                'smart_contract': ['smart contract', 'blockchain contract', 'digital contract'],
                'exchange': ['exchange', 'crypto exchange', 'trading platform', 'marketplace'],
                'altcoin': ['altcoin', 'alternative coin', 'crypto alternative', 'bitcoin alternative'],
                'stablecoin': ['stablecoin', 'stable token', 'pegged crypto', 'fiat-backed crypto'],
                'gas': ['gas', 'transaction fee', 'network fee', 'blockchain fee'],
                'hash': ['hash', 'hash value', 'digital fingerprint', 'cryptographic hash'],
                'node': ['node', 'network node', 'blockchain node', 'validator node'],
                'fork': ['fork', 'blockchain fork', 'protocol upgrade', 'chain split'],
                'whale': ['whale', 'large holder', 'major investor', 'big player']
            }
        }
        return terms

    def _load_stopwords(self) -> Dict[str, set]:
        """Load stopwords for both Persian and English."""
        persian_stopwords = set([
            'و', 'در', 'به', 'از', 'که', 'این', 'است', 'را', 'با', 'برای',
            'آن', 'یک', 'های', 'یا', 'اما', 'باید', 'شد', 'شود', 'بود',
            'شدند', 'می', 'هایش', 'هایم', 'هایت', 'هایمان', 'هایتان'
        ])
        
        return {
            'persian': persian_stopwords,
            'english': self.english_stopwords
        }

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
        
        if language == 'persian':
            # Normalize Persian text
            text = self.persian_normalizer.normalize(text)
            # Convert Persian numbers to English
            persian_numbers = '۰۱۲۳۴۵۶۷۸۹'
            english_numbers = '0123456789'
            translation_table = str.maketrans(persian_numbers, english_numbers)
            text = text.translate(translation_table)
        else:
            # Normalize English text
            text = re.sub(r'[^\w\s]', ' ', text)
            
        # Common normalizations for both languages
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def tokenize_text(self, text: str, language: str) -> List[str]:
        """Tokenize text based on language."""
        if language == 'persian':
            return self.persian_tokenizer.tokenize(text)
        return word_tokenize(text)

    def stem_word(self, word: str, language: str) -> str:
        """Stem word based on language."""
        if language == 'persian':
            return self.persian_stemmer.stem(word)
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
    processor = FinancialTextProcessor()
    
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