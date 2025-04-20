# Market Sentiment Trends Analysis

## Overview
This example demonstrates how to analyze and visualize market sentiment trends across different market types and time periods.

## Example 1: Stock Market Sentiment

```python
from finsentrix import FinSentrix
import pandas as pd
import matplotlib.pyplot as plt

# Initialize analyzer
fsx = FinSentrix()

# Get sentiment data for a specific stock
data = fsx.get_market_sentiment(
    market_type="stock",
    symbol="AAPL",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Create visualization
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['sentiment_score'], label='Sentiment Score')
plt.plot(data['date'], data['price'], label='Stock Price', alpha=0.5)
plt.title('AAPL Sentiment vs Price (Q1 2024)')
plt.xlabel('Date')
plt.ylabel('Score/Price')
plt.legend()
plt.grid(True)
plt.show()
```

![AAPL Sentiment vs Price](assets/aapl_sentiment.png)

## Example 2: Forex Market Analysis

```python
# Analyze EUR/USD sentiment
forex_data = fsx.get_market_sentiment(
    market_type="forex",
    symbol="EUR/USD",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Create correlation heatmap
correlation = forex_data[['sentiment_score', 'price', 'volume']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('EUR/USD Market Correlation')
plt.show()
```

![EUR/USD Correlation](assets/eur_usd_correlation.png)

## Example 3: Crypto Market Overview

```python
# Get sentiment for multiple cryptocurrencies
crypto_symbols = ['BTC/USD', 'ETH/USD', 'BNB/USD']
crypto_data = {}

for symbol in crypto_symbols:
    crypto_data[symbol] = fsx.get_market_sentiment(
        market_type="crypto",
        symbol=symbol,
        start_date="2024-01-01",
        end_date="2024-03-31"
    )

# Create comparative visualization
plt.figure(figsize=(15, 8))
for symbol, data in crypto_data.items():
    plt.plot(data['date'], data['sentiment_score'], label=symbol)
plt.title('Crypto Market Sentiment Comparison')
plt.xlabel('Date')
plt.ylabel('Sentiment Score')
plt.legend()
plt.grid(True)
plt.show()
```

![Crypto Market Sentiment](assets/crypto_sentiment.png)

## Key Insights

1. **Stock Market**
   - Sentiment often leads price movements by 1-2 days
   - Strong correlation between sentiment and trading volume
   - Event-driven sentiment spikes are common

2. **Forex Market**
   - Sentiment shows higher volatility during market hours
   - Central bank announcements create significant sentiment shifts
   - Currency pairs show different sentiment patterns

3. **Crypto Market**
   - Higher sentiment volatility compared to traditional markets
   - Strong correlation between major cryptocurrencies
   - News events have immediate impact on sentiment

## Best Practices

1. **Data Collection**
   - Use appropriate time intervals (hourly for crypto, daily for stocks)
   - Consider market hours for forex analysis
   - Include volume data for better insights

2. **Visualization**
   - Use consistent color schemes
   - Include reference lines for important events
   - Add volume indicators for context

3. **Analysis**
   - Look for sentiment divergences
   - Consider market-specific factors
   - Use multiple timeframes for confirmation

## Next Steps

1. Try different time periods
2. Experiment with different market types
3. Add custom indicators
4. Compare with technical analysis 