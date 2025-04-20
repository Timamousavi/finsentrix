# FinSentrix (FSX) User Guide

## Introduction

Welcome to FinSentrix (FSX), your comprehensive solution for global financial market sentiment analysis. This guide will help you get started with using FinSentrix effectively.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Event Detection](#event-detection)
4. [Rumor Analysis](#rumor-analysis)
5. [Advanced Features](#advanced-features)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Getting Started

### System Requirements

- Python 3.9 or higher
- 4GB RAM minimum
- 2GB free disk space
- Internet connection

### Installation

1. **Download FinSentrix**
   ```bash
   pip install finsentrix
   ```

2. **Set Up Environment**
   ```bash
   # Create virtual environment
   python -m venv finsentrix-env
   source finsentrix-env/bin/activate  # On Windows: finsentrix-env\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   ```bash
   # Create .env file
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Authentication

```python
from finsentrix import FinSentrix

# Initialize with your API key
fsx = FinSentrix(api_key="your_api_key")
```

## Basic Usage

### Sentiment Analysis

```python
# Analyze single text
result = fsx.analyze("Bitcoin shows strong bullish momentum")
print(f"Sentiment: {result.sentiment}")
print(f"Confidence: {result.confidence}")

# Analyze multiple texts
results = fsx.analyze_batch([
    "Stock market rally continues",
    "Market correction expected"
])
```

## Event Detection

### Market Event Analysis

```python
# Detect events in text
events = fsx.detect_events(
    "Central Bank announced interest rate hike of 0.5%"
)

# Print event details
for event in events:
    print(f"Event: {event.text}")
    print(f"Type: {event.type}")
    print(f"Sentiment Impact: {event.sentiment_impact}")
```

### Timeline Visualization

```python
# Get sentiment timeline with events
timeline = fsx.get_timeline(
    start_time="2024-02-01",
    end_time="2024-02-20"
)

# Display interactive timeline
timeline.show()
```

## Rumor Analysis

### Detecting Rumors

```python
# Analyze messages for rumors
messages = [
    {"text": "Rumor about company X", "timestamp": "2024-02-20T10:00:00Z"},
    {"text": "Similar rumor about X", "timestamp": "2024-02-20T11:00:00Z"}
]

rumors = fsx.detect_rumors(messages)

# Print rumor analysis
for rumor in rumors:
    print(f"Confidence: {rumor.confidence}")
    print(f"Verdict: {rumor.verdict}")
    print(f"Pattern Matches: {rumor.pattern_matches}")
```

### Rumor Alerts

```python
# Get high-confidence rumor alerts
alerts = fsx.get_rumor_alerts(threshold=0.7)

# Process alerts
for alert in alerts:
    print(f"Alert: {alert.title}")
    print(f"Message: {alert.content.message}")
    print(f"Time Span: {alert.content.time_span}")
    print(f"Sample Messages: {alert.content.sample_messages}")
```

## Advanced Features

### Market-Specific Analysis

```python
# Stock market analysis
stock_result = fsx.analyze(
    text="AAPL showing strong growth",
    market_type="stock"
)

# Forex market analysis
forex_result = fsx.analyze(
    text="EUR/USD expected to rise",
    market_type="forex"
)

# Crypto market analysis
crypto_result = fsx.analyze(
    text="Bitcoin reaching new ATH",
    market_type="crypto"
)
```

### Language Support

```python
# English text
en_result = fsx.analyze(
    text="Market showing positive trends",
    language="en"
)

# Persian text
fa_result = fsx.analyze(
    text="بازار امروز روند مثبتی دارد",
    language="fa"
)
```

### Real-Time Analysis

```python
from finsentrix import RealTimeAnalyzer

# Initialize real-time analyzer
rt_analyzer = RealTimeAnalyzer()

# Start monitoring
rt_analyzer.start_monitoring(
    sources=["twitter", "news", "telegram"],
    market_types=["stock", "crypto"],
    callback=handle_sentiment_update
)

def handle_sentiment_update(update):
    print(f"New sentiment update: {update}")
```

### Custom Event Types

```python
# Add custom event types
fsx.add_event_type(
    name="custom_event",
    keywords=["custom", "event", "keywords"]
)
```

### Rumor Pattern Customization

```python
# Add custom rumor patterns
fsx.add_rumor_patterns([
    "custom pattern 1",
    "custom pattern 2"
])
```

### Visualization Customization

```python
# Customize timeline visualization
timeline = fsx.get_timeline(
    start_time="2024-02-01",
    end_time="2024-02-20",
    title="Custom Timeline",
    colors={
        "sentiment": "blue",
        "events": "red"
    }
)
```

## Best Practices

1. **Text Preparation**
   - Remove URLs and special characters
   - Normalize text length (100-500 characters optimal)
   - Use clear, concise language

2. **Market Selection**
   - Choose appropriate market type
   - Consider market-specific terminology
   - Account for market hours

3. **Language Handling**
   - Specify language when known
   - Use appropriate character encoding
   - Consider cultural context

4. **Performance Optimization**
   - Use batch processing for multiple texts
   - Cache results when possible
   - Monitor API usage

5. **Event Detection**
   - Use clear, concise text for better event detection
   - Include relevant context in event descriptions
   - Monitor event sentiment impact over time

6. **Rumor Analysis**
   - Set appropriate confidence thresholds
   - Consider message volume and spread
   - Monitor pattern matches and time spans

7. **Data Collection**
   - Collect data from diverse sources
   - Maintain proper timestamps
   - Include message metadata when available

8. **Visualization**
   - Use appropriate time ranges
   - Customize colors for better visibility
   - Include relevant annotations

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify API keys
   - Check token expiration
   - Ensure proper environment setup

2. **Language Detection**
   - Explicitly specify language
   - Check text encoding
   - Verify language support

3. **Market Type Issues**
   - Verify market type support
   - Check market-specific terminology
   - Consider market context

4. **Event Detection**
   - Issue: Events not detected
   - Solution: Check text clarity and add relevant keywords

5. **Rumor Analysis**
   - Issue: Low confidence scores
   - Solution: Adjust time window and pattern matching

6. **Visualization**
   - Issue: Timeline not displaying
   - Solution: Check data format and time ranges

### Getting Help

- Documentation: https://docs.finsentrix.com
- Support Email: support@finsentrix.com
- Community Forum: https://community.finsentrix.com

## FAQ

1. **What markets does FinSentrix support?**
   - Stocks
   - Forex
   - Cryptocurrency

2. **Which languages are supported?**
   - English
   - Persian

3. **How accurate is the sentiment analysis?**
   - Accuracy varies by market and language
   - Typically 85-90% for well-formatted text
   - Higher for market-specific content

4. **Can I use FinSentrix for real-time analysis?**
   - Yes, through the RealTimeAnalyzer
   - Supports multiple data sources
   - Configurable update intervals

5. **How do I handle rate limits?**
   - Monitor API usage
   - Implement exponential backoff
   - Consider upgrading plan

## Updates and Maintenance

- Check for updates regularly
- Review changelog before updating
- Backup configurations
- Test new versions in staging 