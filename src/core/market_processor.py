from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy import stats
import yfinance as yf

class MarketProcessor:
    def __init__(self, ticker: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """Initialize the market processor with a stock ticker and date range."""
        self.ticker = ticker
        self.end_date = end_date or datetime.now()
        self.start_date = start_date or (self.end_date - timedelta(days=30))
        
        # Fetch historical data
        self.data = self._fetch_data()
        
    def _fetch_data(self) -> pd.DataFrame:
        """Fetch historical market data for the ticker."""
        try:
            stock = yf.Ticker(self.ticker)
            data = stock.history(
                start=self.start_date,
                end=self.end_date,
                interval="1d"
            )
            return data
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {str(e)}")
            return pd.DataFrame()
            
    def calculate_technical_indicators(self) -> Dict:
        """Calculate various technical indicators from the market data."""
        if self.data.empty:
            return {}
            
        # Calculate moving averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
        # Calculate RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Calculate Bollinger Bands
        self.data['BB_middle'] = self.data['Close'].rolling(window=20).mean()
        self.data['BB_std'] = self.data['Close'].rolling(window=20).std()
        self.data['BB_upper'] = self.data['BB_middle'] + 2 * self.data['BB_std']
        self.data['BB_lower'] = self.data['BB_middle'] - 2 * self.data['BB_std']
        
        # Calculate MACD
        exp1 = self.data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.data['Close'].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = exp1 - exp2
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
        
        return {
            'sma_20': self.data['SMA_20'].iloc[-1],
            'sma_50': self.data['SMA_50'].iloc[-1],
            'rsi': self.data['RSI'].iloc[-1],
            'bb_upper': self.data['BB_upper'].iloc[-1],
            'bb_lower': self.data['BB_lower'].iloc[-1],
            'macd': self.data['MACD'].iloc[-1],
            'signal_line': self.data['Signal_Line'].iloc[-1]
        }
        
    def calculate_volatility(self, window: int = 20) -> float:
        """Calculate market volatility using standard deviation of returns."""
        if self.data.empty:
            return 0.0
            
        returns = self.data['Close'].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        return volatility.iloc[-1]
        
    def detect_trend(self, window: int = 20) -> Dict:
        """Detect market trend using linear regression."""
        if self.data.empty:
            return {'trend': 'neutral', 'strength': 0.0}
            
        # Get recent data
        recent_data = self.data['Close'].tail(window)
        
        # Perform linear regression
        x = np.arange(len(recent_data))
        slope, _, r_value, _, _ = stats.linregress(x, recent_data)
        
        # Determine trend
        if slope > 0:
            trend = 'upward'
        elif slope < 0:
            trend = 'downward'
        else:
            trend = 'neutral'
            
        return {
            'trend': trend,
            'strength': abs(r_value),
            'slope': slope
        }
        
    def calculate_support_resistance(self, window: int = 20) -> Dict:
        """Calculate support and resistance levels."""
        if self.data.empty:
            return {'support': None, 'resistance': None}
            
        recent_data = self.data.tail(window)
        
        # Find local minima and maxima
        highs = recent_data['High']
        lows = recent_data['Low']
        
        # Calculate support and resistance
        support = lows.min()
        resistance = highs.max()
        
        return {
            'support': support,
            'resistance': resistance,
            'current_price': recent_data['Close'].iloc[-1]
        }
        
    def get_market_summary(self) -> Dict:
        """Generate a comprehensive market summary."""
        if self.data.empty:
            return {}
            
        technical_indicators = self.calculate_technical_indicators()
        volatility = self.calculate_volatility()
        trend = self.detect_trend()
        levels = self.calculate_support_resistance()
        
        return {
            'ticker': self.ticker,
            'current_price': self.data['Close'].iloc[-1],
            'volume': self.data['Volume'].iloc[-1],
            'volatility': volatility,
            'trend': trend,
            'technical_indicators': technical_indicators,
            'support_resistance': levels,
            'timestamp': datetime.now().isoformat()
        }
        
    def analyze_market_impact(self, event: Dict) -> float:
        """Analyze the potential impact of an event on the market.
        
        Args:
            event: Event to analyze
            
        Returns:
            Impact score between -1 and 1
        """
        if self.data.empty:
            return 0.0
            
        # Get current market conditions
        volatility = self.calculate_volatility()
        trend = self.detect_trend()
        
        # Base impact score
        impact = 0.0
        
        # Adjust based on market volatility
        impact *= (1 + volatility)
        
        # Consider trend strength
        if trend['trend'] == 'upward':
            impact *= (1 + trend['strength'])
        elif trend['trend'] == 'downward':
            impact *= (1 - trend['strength'])
            
        return min(max(impact, -1), 1) 