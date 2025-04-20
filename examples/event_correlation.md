# Event-Sentiment Correlation Analysis

## Overview
This example demonstrates how to analyze the correlation between market events and sentiment changes, with a focus on different types of events and their impact.

## Example 1: Earnings Announcements

```python
from finsentrix import FinSentrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize analyzer
fsx = FinSentrix()

# Get event and sentiment data for a company
company_data = fsx.get_event_sentiment(
    market_type="stock",
    symbol="MSFT",
    event_type="earnings",
    days_before=5,
    days_after=5
)

# Create event impact visualization
plt.figure(figsize=(12, 6))
plt.plot(company_data['timestamp'], company_data['sentiment_score'], 
         label='Sentiment Score', color='blue')
plt.axvline(x=company_data['event_timestamp'].iloc[0], 
            color='red', linestyle='--', label='Earnings Announcement')
plt.fill_between(company_data['timestamp'],
                 company_data['sentiment_score'] - company_data['sentiment_std'],
                 company_data['sentiment_score'] + company_data['sentiment_std'],
                 alpha=0.2, color='blue')
plt.title('MSFT Sentiment Around Earnings Announcement')
plt.xlabel('Date')
plt.ylabel('Sentiment Score')
plt.legend()
plt.grid(True)
plt.show()
```

![MSFT Earnings Impact](assets/msft_earnings.png)

## Example 2: Central Bank Decisions

```python
# Analyze EUR/USD around ECB meeting
forex_data = fsx.get_event_sentiment(
    market_type="forex",
    symbol="EUR/USD",
    event_type="central_bank",
    days_before=3,
    days_after=3
)

# Create event impact analysis
impact_analysis = fsx.analyze_event_impact(
    data=forex_data,
    event_window=(-3, 3),  # 3 days before and after
    confidence_level=0.95
)

# Plot impact distribution
sns.histplot(impact_analysis['impact_scores'], kde=True)
plt.axvline(x=impact_analysis['mean_impact'], color='red', 
            linestyle='--', label='Mean Impact')
plt.title('Distribution of ECB Meeting Impacts')
plt.xlabel('Sentiment Impact Score')
plt.ylabel('Frequency')
plt.legend()
plt.show()
```

![ECB Impact Distribution](assets/ecb_impact.png)

## Example 3: Political Events

```python
# Get sentiment around political events
political_data = fsx.get_event_sentiment(
    market_type="stock",
    symbol="^GSPC",  # S&P 500
    event_type="political",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Create event timeline
events = political_data['events'].unique()
timeline_data = []

for event in events:
    event_data = political_data[political_data['events'] == event]
    timeline_data.append({
        'event': event,
        'timestamp': event_data['timestamp'].iloc[0],
        'sentiment_impact': event_data['sentiment_impact'].mean(),
        'market_impact': event_data['price_change'].mean()
    })

# Create timeline visualization
timeline_df = pd.DataFrame(timeline_data)
plt.figure(figsize=(15, 8))
plt.scatter(timeline_df['timestamp'], timeline_df['sentiment_impact'],
            s=timeline_df['market_impact']*100, alpha=0.6)
plt.title('Political Events Impact Timeline')
plt.xlabel('Date')
plt.ylabel('Sentiment Impact')
plt.grid(True)
plt.show()
```

![Political Events Timeline](assets/political_timeline.png)

## Key Insights

1. **Event Types**
   - Earnings announcements show predictable patterns
   - Central bank decisions create immediate impacts
   - Political events have varying degrees of influence

2. **Impact Analysis**
   - Sentiment changes often precede price movements
   - Different event types have different impact durations
   - Market context affects event impact

3. **Correlation Patterns**
   - Strong correlation between sentiment and volume
   - Event type affects correlation strength
   - Market conditions influence correlation patterns

## Best Practices

1. **Event Selection**
   - Choose relevant event types for your market
   - Consider event significance
   - Account for market conditions

2. **Analysis Window**
   - Use appropriate timeframes
   - Consider event-specific characteristics
   - Account for market hours

3. **Impact Measurement**
   - Use standardized metrics
   - Consider market context
   - Account for confounding factors

## Next Steps

1. Analyze more event types
2. Develop custom impact metrics
3. Create automated alerts
4. Build predictive models 