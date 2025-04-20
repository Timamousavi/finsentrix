import asyncio
import schedule
import time
from datetime import datetime
import logging
from typing import List, Dict
import pandas as pd
from .scraper import WebScraper
from .telegram_scraper import TelegramScraper
import os
from pathlib import Path
from .market_sentiment_analyzer import MarketSentimentAnalyzer

class DataCollectionPipeline:
    def __init__(self, api_credentials: Dict[str, str]):
        """
        Initialize the data collection pipeline.
        
        Args:
            api_credentials (Dict[str, str]): Dictionary containing API credentials
        """
        # Initialize scrapers
        self.web_scraper = WebScraper()
        self.telegram_scraper = TelegramScraper(api_credentials)
        
        # Configure financial sources
        self.financial_sources = {
            'persian': {
                'stock': {
                    'websites': [
                        'https://www.tgju.org/',
                        'https://www.irbourse.com/',
                        'https://www.boursenews.ir/',
                        'https://www.bourse24.ir/',
                        'https://www.tsetmc.com/',
                        'https://www.irbourse.com/analysis/',
                        'https://www.boursenews.ir/analysis/'
                    ],
                    'telegram_channels': [
                        'iranbourse',
                        'bourse24',
                        'boursenews',
                        'tse_analysis',
                        'stock_signals_ir',
                        'iran_stock_analysis'
                    ]
                },
                'forex': {
                    'websites': [
                        'https://www.tgju.org/currency',
                        'https://www.irbourse.com/forex/',
                        'https://www.boursenews.ir/forex/',
                        'https://www.forex.ir/',
                        'https://www.fxstreet.ir/',
                        'https://www.forexanalysis.ir/',
                        'https://www.forexsignals.ir/'
                    ],
                    'telegram_channels': [
                        'forex_ir',
                        'forex_signals_ir',
                        'forex_analysis_ir',
                        'forex_trading_ir',
                        'forex_education_ir',
                        'forex_market_ir',
                        'forex_news_ir'
                    ]
                },
                'crypto': {
                    'websites': [
                        'https://www.tgju.org/crypto',
                        'https://www.irbourse.com/crypto/',
                        'https://www.boursenews.ir/crypto/',
                        'https://www.cryptoprice.ir/',
                        'https://www.bitcoin.ir/',
                        'https://www.cryptoanalysis.ir/',
                        'https://www.blockchain.ir/'
                    ],
                    'telegram_channels': [
                        'crypto_ir',
                        'bitcoin_ir',
                        'crypto_signals_ir',
                        'crypto_trading_ir',
                        'crypto_education_ir',
                        'crypto_market_ir',
                        'crypto_news_ir',
                        'defi_ir',
                        'nft_ir'
                    ]
                }
            },
            'english': {
                'stock': {
                    'websites': [
                        'https://www.bloomberg.com/markets/stocks',
                        'https://www.reuters.com/markets/stocks',
                        'https://www.marketwatch.com/investing/stocks',
                        'https://www.investing.com/equities/',
                        'https://www.finviz.com/',
                        'https://www.tradingview.com/markets/stocks/',
                        'https://www.seekingalpha.com/'
                    ],
                    'telegram_channels': [
                        'BloombergMarkets',
                        'ReutersBusiness',
                        'MarketWatch',
                        'StockMarketNews',
                        'TradingSignals',
                        'MarketAnalysis'
                    ]
                },
                'forex': {
                    'websites': [
                        'https://www.bloomberg.com/markets/currencies',
                        'https://www.reuters.com/markets/currencies',
                        'https://www.investing.com/currencies/',
                        'https://www.forexfactory.com/',
                        'https://www.dailyfx.com/',
                        'https://www.fxstreet.com/',
                        'https://www.babypips.com/',
                        'https://www.forexlive.com/',
                        'https://www.forexcrunch.com/'
                    ],
                    'telegram_channels': [
                        'ForexFactory',
                        'ForexSignals',
                        'ForexAnalysis',
                        'ForexTrading',
                        'ForexEducation',
                        'ForexMarket',
                        'ForexNews',
                        'ForexLive',
                        'ForexCrunch'
                    ]
                },
                'crypto': {
                    'websites': [
                        'https://www.coindesk.com/',
                        'https://cointelegraph.com/',
                        'https://www.cryptonews.com/',
                        'https://www.investing.com/crypto/',
                        'https://www.coinmarketcap.com/',
                        'https://www.coingecko.com/',
                        'https://www.cryptocompare.com/',
                        'https://www.theblock.co/',
                        'https://www.decrypt.co/',
                        'https://www.defipulse.com/',
                        'https://www.dappradar.com/'
                    ],
                    'telegram_channels': [
                        'CoinDesk',
                        'CryptoNews',
                        'CryptoSignals',
                        'CryptoMarket',
                        'CryptoEducation',
                        'CryptoAnalysis',
                        'DeFiNews',
                        'NFTNews',
                        'BlockchainNews',
                        'CryptoLive',
                        'CryptoCrunch'
                    ]
                }
            }
        }
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create log directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Add file handler
        file_handler = logging.FileHandler('logs/data_collection.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)
        
        # Create data directories
        self.data_dir = Path('data')
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        
        for directory in [self.raw_dir, self.processed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Create language and market-specific subdirectories
        for lang in ['persian', 'english']:
            for market in ['stock', 'forex', 'crypto']:
                (self.raw_dir / lang / market).mkdir(parents=True, exist_ok=True)
                (self.processed_dir / lang / market).mkdir(parents=True, exist_ok=True)

    def collect_web_data(self, language: str = 'persian', market: str = 'stock') -> None:
        """
        Collect data from financial websites.
        
        Args:
            language (str): Language of the sources ('persian' or 'english')
            market (str): Market type ('stock', 'forex', or 'crypto')
        """
        self.logger.info(f"Starting web data collection for {language} {market} sources")
        
        for website in self.financial_sources[language][market]['websites']:
            try:
                self.logger.info(f"Scraping {website}")
                data = self.web_scraper.scrape_website(website)
                
                # Save data with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{language}_{market}_web_{timestamp}.csv"
                filepath = self.raw_dir / language / market / filename
                
                data.to_csv(filepath, index=False)
                self.logger.info(f"Saved data to {filepath}")
                
            except Exception as e:
                self.logger.error(f"Error scraping {website}: {str(e)}")

    def collect_telegram_data(self, language: str = 'persian', market: str = 'stock') -> None:
        """
        Collect data from Telegram channels.
        
        Args:
            language (str): Language of the sources ('persian' or 'english')
            market (str): Market type ('stock', 'forex', or 'crypto')
        """
        self.logger.info(f"Starting Telegram data collection for {language} {market} channels")
        
        for channel in self.financial_sources[language][market]['telegram_channels']:
            try:
                self.logger.info(f"Collecting messages from {channel}")
                messages = self.telegram_scraper.collect_messages(channel)
                
                # Save data with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{language}_{market}_telegram_{timestamp}.csv"
                filepath = self.raw_dir / language / market / filename
                
                messages.to_csv(filepath, index=False)
                self.logger.info(f"Saved data to {filepath}")
                
            except Exception as e:
                self.logger.error(f"Error collecting from {channel}: {str(e)}")

    def run_collection(self) -> None:
        """Run data collection for all sources and markets."""
        self.logger.info("Starting data collection pipeline")
        
        # Collect data for both languages and all markets
        for language in ['persian', 'english']:
            for market in ['stock', 'forex', 'crypto']:
                self.collect_web_data(language, market)
                self.collect_telegram_data(language, market)
            
        self.logger.info("Data collection completed")

    def schedule_collection(self, interval_hours: int = 6) -> None:
        """
        Schedule data collection to run at regular intervals.
        
        Args:
            interval_hours (int): Interval in hours between collections
        """
        self.logger.info(f"Scheduling data collection every {interval_hours} hours")
        schedule.every(interval_hours).hours.do(self.run_collection)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Example usage
if __name__ == "__main__":
    # Initialize pipeline with Telegram API credentials
    api_credentials = {
        'api_id': 'YOUR_API_ID',
        'api_hash': 'YOUR_API_HASH',
        'phone': 'YOUR_PHONE_NUMBER'
    }
    
    pipeline = DataCollectionPipeline(api_credentials)
    
    # Run collection once
    pipeline.run_collection()
    
    # Or schedule collection
    # pipeline.schedule_collection(interval_hours=6)

# Initialize the analyzer
analyzer = MarketSentimentAnalyzer()

# Analyze a single text
result = analyzer.analyze_sentiment("بیت کوین امروز رشد خوبی داشت و به 50 هزار دلار رسید")
print(result)
# Output:
# {
#     'sentiment': 'positive',
#     'confidence': 0.85,
#     'market_type': 'crypto',
#     'scores': {
#         'positive': 0.85,
#         'neutral': 0.10,
#         'negative': 0.05
#     }
# }

# Get market insights from multiple texts
insights = analyzer.get_market_insights([
    "بیت کوین امروز رشد خوبی داشت",
    "اتریوم در حال اصلاح است",
    "بازار کریپتو نوسان زیادی دارد"
])
print(insights)
# Output:
# {
#     'overall_sentiment': 'neutral',
#     'sentiment_distribution': {
#         'positive': 33.3,
#         'neutral': 33.3,
#         'negative': 33.3
#     },
#     'average_confidence': 0.82,
#     'market_type': 'crypto',
#     'total_samples': 3
# } 