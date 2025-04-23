import aiohttp
import asyncio
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class FinancialDataService:
    def __init__(self):
        self.api_key = os.getenv("FINANCIAL_DATA_API_KEY")
        self.base_url = os.getenv("FINANCIAL_DATA_BASE_URL", "https://api.example.com")
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_market_data(self) -> Dict[str, Any]:
        """Fetch real-time market data from financial data provider."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(
                f"{self.base_url}/market-data",
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "timestamp": datetime.now().isoformat(),
                        "market_data": data
                    }
                else:
                    logger.error(f"Failed to fetch market data: {response.status}")
                    return self.generate_mock_data()
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            return self.generate_mock_data()

    async def fetch_sentiment_indicators(self) -> Dict[str, Any]:
        """Fetch sentiment indicators from various sources."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(
                f"{self.base_url}/sentiment-indicators",
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "timestamp": datetime.now().isoformat(),
                        "sentiment_indicators": data
                    }
                else:
                    logger.error(f"Failed to fetch sentiment indicators: {response.status}")
                    return self.generate_mock_sentiment_data()
        except Exception as e:
            logger.error(f"Error fetching sentiment indicators: {str(e)}")
            return self.generate_mock_sentiment_data()

    def generate_mock_data(self) -> Dict[str, Any]:
        """Generate mock market data for development."""
        return {
            "timestamp": datetime.now().isoformat(),
            "market_data": {
                "tse_index": {
                    "value": 150000,
                    "change": 0.5,
                    "volume": 1000000
                },
                "ifx_index": {
                    "value": 25000,
                    "change": -0.2,
                    "volume": 500000
                }
            }
        }

    def generate_mock_sentiment_data(self) -> Dict[str, Any]:
        """Generate mock sentiment data for development."""
        return {
            "timestamp": datetime.now().isoformat(),
            "sentiment_indicators": {
                "overall_sentiment": "positive",
                "confidence": 0.75,
                "sector_sentiment": {
                    "banking": "positive",
                    "oil": "neutral",
                    "automotive": "negative"
                }
            }
        }

    async def get_real_time_data(self) -> Dict[str, Any]:
        """Get combined real-time market and sentiment data."""
        try:
            market_data, sentiment_data = await asyncio.gather(
                self.fetch_market_data(),
                self.fetch_sentiment_indicators()
            )
            
            return {
                "status": "success",
                "data": {
                    "market_data": market_data["market_data"],
                    "sentiment_data": sentiment_data["sentiment_indicators"],
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error getting real-time data: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": {
                    "market_data": self.generate_mock_data()["market_data"],
                    "sentiment_data": self.generate_mock_sentiment_data()["sentiment_indicators"],
                    "timestamp": datetime.now().isoformat()
                }
            } 