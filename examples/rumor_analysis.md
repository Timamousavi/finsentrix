# Rumor Analysis Dashboard

## Overview
This example demonstrates how to create a comprehensive dashboard for analyzing market rumors, tracking their spread, and assessing their impact.

## Example 1: Rumor Detection and Tracking

```python
from finsentrix import FinSentrix
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Initialize analyzer
fsx = FinSentrix()

# Get rumor data
rumor_data = fsx.get_rumor_data(
    market_type="stock",
    symbol="TSLA",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Create rumor network
G = nx.Graph()
for _, row in rumor_data.iterrows():
    G.add_node(row['source'], type='source')
    G.add_node(row['rumor_id'], type='rumor')
    G.add_edge(row['source'], row['rumor_id'], 
               weight=row['confidence'])

# Visualize rumor network
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=500, font_size=8, font_weight='bold')
plt.title('Rumor Propagation Network')
plt.show()
```

![Rumor Network](assets/rumor_network.png)

## Example 2: Rumor Impact Analysis

```python
# Analyze rumor impact
impact_data = fsx.analyze_rumor_impact(
    rumor_data=rumor_data,
    market_data=market_data,
    window_size=24  # hours
)

# Create impact visualization
plt.figure(figsize=(15, 6))
plt.plot(impact_data['timestamp'], impact_data['price_change'],
         label='Price Change', color='blue')
plt.plot(impact_data['timestamp'], impact_data['sentiment_change'],
         label='Sentiment Change', color='red')
plt.fill_between(impact_data['timestamp'],
                 impact_data['price_change'] - impact_data['price_std'],
                 impact_data['price_change'] + impact_data['price_std'],
                 alpha=0.2, color='blue')
plt.title('Rumor Impact on Price and Sentiment')
plt.xlabel('Time')
plt.ylabel('Change (%)')
plt.legend()
plt.grid(True)
plt.show()
```

![Rumor Impact](assets/rumor_impact.png)

## Example 3: Rumor Dashboard

```python
# Create comprehensive dashboard
dashboard = fsx.create_rumor_dashboard(
    market_type="stock",
    symbol="TSLA",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Display key metrics
metrics = dashboard.get_metrics()
print(f"""
Rumor Analysis Metrics:
- Total Rumors: {metrics['total_rumors']}
- Verified Rumors: {metrics['verified_rumors']}
- Average Confidence: {metrics['avg_confidence']:.2f}
- Impact Score: {metrics['impact_score']:.2f}
- Spread Rate: {metrics['spread_rate']:.2f}
""")

# Create timeline visualization
timeline = dashboard.get_timeline()
plt.figure(figsize=(15, 8))
for rumor in timeline['rumors']:
    plt.scatter(rumor['timestamp'], rumor['confidence'],
                s=rumor['impact']*100, alpha=0.6,
                label=f"Rumor {rumor['id']}")
plt.title('Rumor Timeline with Impact')
plt.xlabel('Date')
plt.ylabel('Confidence')
plt.legend()
plt.grid(True)
plt.show()
```

![Rumor Dashboard](assets/rumor_dashboard.png)

## Key Features

1. **Rumor Detection**
   - Pattern matching
   - Source verification
   - Confidence scoring
   - Spread tracking

2. **Impact Analysis**
   - Price impact
   - Sentiment impact
   - Volume analysis
   - Market reaction

3. **Visualization**
   - Network graphs
   - Timeline views
   - Impact charts
   - Metric dashboards

## Best Practices

1. **Data Collection**
   - Use multiple sources
   - Verify source reliability
   - Track rumor evolution
   - Monitor spread patterns

2. **Analysis**
   - Consider market context
   - Account for time zones
   - Use appropriate timeframes
   - Validate with market data

3. **Visualization**
   - Use clear color schemes
   - Include reference points
   - Show confidence intervals
   - Highlight key events

## Implementation Tips

1. **Performance**
   - Use efficient data structures
   - Implement caching
   - Optimize queries
   - Handle real-time updates

2. **Scalability**
   - Design for multiple markets
   - Support concurrent analysis
   - Handle large datasets
   - Manage resource usage

3. **User Experience**
   - Provide clear navigation
   - Include tooltips
   - Enable customization
   - Support export options

## Next Steps

1. Add more visualization types
2. Implement real-time updates
3. Add custom alerts
4. Develop predictive features 