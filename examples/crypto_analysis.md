# Crypto Market Analysis

## Overview
This example demonstrates specialized analysis techniques for cryptocurrency markets, including sentiment analysis, market correlation, and trend detection.

## Example 1: Crypto Market Sentiment

```python
from finsentrix import FinSentrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize analyzer
fsx = FinSentrix()

# Get sentiment data for major cryptocurrencies
crypto_symbols = ['BTC/USD', 'ETH/USD', 'BNB/USD']
sentiment_data = {}

for symbol in crypto_symbols:
    sentiment_data[symbol] = fsx.get_market_sentiment(
        market_type="crypto",
        symbol=symbol,
        start_date="2024-01-01",
        end_date="2024-03-31",
        interval="1h"  # Hourly data for crypto
    )

# Create sentiment comparison
plt.figure(figsize=(15, 8))
for symbol, data in sentiment_data.items():
    plt.plot(data['timestamp'], data['sentiment_score'], 
             label=symbol, alpha=0.7)
plt.title('Cryptocurrency Sentiment Comparison')
plt.xlabel('Date')
plt.ylabel('Sentiment Score')
plt.legend()
plt.grid(True)
plt.show()
```

![Crypto Sentiment Comparison](assets/crypto_sentiment_comparison.png)

## Example 2: Market Correlation Analysis

```python
# Calculate correlation matrix
correlation_data = pd.DataFrame()
for symbol, data in sentiment_data.items():
    correlation_data[symbol] = data['sentiment_score']

correlation_matrix = correlation_data.corr()

# Create correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
            vmin=-1, vmax=1)
plt.title('Cryptocurrency Sentiment Correlation')
plt.show()

# Analyze market movements
price_data = fsx.get_market_data(
    market_type="crypto",
    symbols=crypto_symbols,
    start_date="2024-01-01",
    end_date="2024-03-31",
    interval="1h"
)

# Create price-sentiment correlation
plt.figure(figsize=(15, 10))
for symbol in crypto_symbols:
    plt.scatter(price_data[symbol]['price_change'],
                sentiment_data[symbol]['sentiment_change'],
                alpha=0.5, label=symbol)
plt.title('Price Change vs Sentiment Change')
plt.xlabel('Price Change (%)')
plt.ylabel('Sentiment Change')
plt.legend()
plt.grid(True)
plt.show()
```

![Crypto Correlation](assets/crypto_correlation.png)

## Example 3: Trend Analysis

```python
# Detect market trends
trend_data = fsx.analyze_market_trends(
    market_type="crypto",
    symbols=crypto_symbols,
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Create trend visualization
plt.figure(figsize=(15, 10))
for symbol in crypto_symbols:
    data = trend_data[symbol]
    plt.plot(data['timestamp'], data['trend_strength'],
             label=f'{symbol} Trend', alpha=0.7)
    plt.fill_between(data['timestamp'],
                     data['trend_strength'] - data['confidence_interval'],
                     data['trend_strength'] + data['confidence_interval'],
                     alpha=0.2)
plt.title('Cryptocurrency Trend Analysis')
plt.xlabel('Date')
plt.ylabel('Trend Strength')
plt.legend()
plt.grid(True)
plt.show()

# Analyze trend components
components = fsx.analyze_trend_components(trend_data)
print(f"""
Trend Analysis Components:
- Market Sentiment: {components['market_sentiment']:.2f}
- Social Media Activity: {components['social_activity']:.2f}
- Trading Volume: {components['trading_volume']:.2f}
- News Impact: {components['news_impact']:.2f}
""")
```

![Crypto Trends](assets/crypto_trends.png)

## Key Insights

1. **Market Behavior**
   - Higher sentiment volatility
   - Strong correlation between major coins
   - 24/7 market impact on analysis
   - Social media influence

2. **Trend Patterns**
   - Sentiment often leads price
   - News events create spikes
   - Weekend patterns differ
   - Exchange-specific effects

3. **Analysis Challenges**
   - Multiple data sources
   - High-frequency data
   - Market manipulation
   - Regulatory news impact

## Best Practices

1. **Data Collection**
   - Use multiple exchanges
   - Consider time zones
   - Include social media
   - Track news sources

2. **Analysis**
   - Use appropriate timeframes
   - Consider market hours
   - Account for volume
   - Validate with price data

3. **Visualization**
   - Show multiple timeframes
   - Include volume data
   - Highlight events
   - Use clear indicators

## Implementation Tips

1. **Performance**
   - Optimize for real-time
   - Handle high-frequency data
   - Implement caching
   - Manage API limits

2. **Accuracy**
   - Use multiple sources
   - Validate signals
   - Consider market depth
   - Account for liquidity

3. **User Experience**
   - Provide real-time updates
   - Show clear trends
   - Include alerts
   - Enable customization

## Next Steps

1. Add more cryptocurrencies
2. Implement real-time analysis
3. Add technical indicators
4. Develop prediction models 