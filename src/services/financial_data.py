import aiohttp
import asyncio
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FinancialDataService:
    def __init__(self):
        # Using Alpha Vantage as our data source - you'll need to replace with your API key
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Store this in environment variables
        
    async def fetch_market_data(self) -> Dict[str, Any]:
        """Fetch real-time market data for Tehran Stock Exchange (TEDPIX)"""
        async with aiohttp.ClientSession() as session:
            try:
                # For demo, we'll use a global quote endpoint
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": "TEDPIX.TEH",  # Tehran Stock Exchange Index
                    "apikey": self.api_key
                }
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_market_data(data)
                    else:
                        logger.error(f"Failed to fetch market data: {response.status}")
                        return {}
            except Exception as e:
                logger.error(f"Error fetching market data: {str(e)}")
                return {}

    async def fetch_sentiment_indicators(self) -> List[Dict[str, Any]]:
        """Fetch and calculate sentiment indicators from various sources"""
        async with aiohttp.ClientSession() as session:
            try:
                # For demo, we'll use technical indicators as a proxy for sentiment
                params = {
                    "function": "RSI",  # Relative Strength Index
                    "symbol": "TEDPIX.TEH",
                    "interval": "daily",
                    "time_period": "14",
                    "apikey": self.api_key
                }
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_sentiment_data(data)
                    else:
                        logger.error(f"Failed to fetch sentiment data: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Error fetching sentiment data: {str(e)}")
                return []

    def _process_market_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and format market data"""
        try:
            quote = data.get("Global Quote", {})
            return {
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": float(quote.get("10. change percent", "0").strip("%")),
                "volume": int(quote.get("06. volume", 0)),
                "timestamp": datetime.now().isoformat()
            }
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing market data: {str(e)}")
            return {}

    def _process_sentiment_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process and format sentiment data"""
        try:
            technical_data = data.get("Technical Analysis: RSI", {})
            return [
                {
                    "timestamp": date,
                    "sentiment_score": float(values["RSI"]) / 100,  # Normalize to 0-1
                }
                for date, values in list(technical_data.items())[:30]  # Last 30 days
            ]
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing sentiment data: {str(e)}")
            return []

    @staticmethod
    def generate_mock_data() -> Dict[str, Any]:
        """Generate mock data for testing when API is not available"""
        current_time = datetime.now()
        return {
            "market_data": {
                "price": 1500000,  # Example TEDPIX value
                "change": 15000,
                "change_percent": 1.2,
                "volume": 1500000000,
                "timestamp": current_time.isoformat()
            },
            "sentiment_data": [
                {
                    "timestamp": (current_time - timedelta(days=i)).isoformat(),
                    "sentiment_score": 0.5 + ((-1) ** i) * 0.1  # Oscillating values for demo
                }
                for i in range(30)
            ]
        } 