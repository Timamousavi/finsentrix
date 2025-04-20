# FinSentrix (FSX) - Global Financial Market Sentiment Analysis

<div align="center">
  <img src="docs/assets/banner.png" alt="FinSentrix Banner" width="800"/>
  
  [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Build Status](https://img.shields.io/github/actions/workflow/status/Timamousavi/finsentrix/ci.yml)](https://github.com/Timamousavi/finsentrix/actions)
  [![Code Coverage](https://img.shields.io/codecov/c/github/Timamousavi/finsentrix)](https://codecov.io/gh/Timamousavi/finsentrix)
  [![Stars](https://img.shields.io/github/stars/Timamousavi/finsentrix?style=social)](https://github.com/Timamousavi/finsentrix/stargazers)
  [![Docker Pulls](https://img.shields.io/docker/pulls/timamousavi/finsentrix)](https://hub.docker.com/r/timamousavi/finsentrix)
</div>

## 🌟 Overview

FinSentrix provides real-time sentiment analysis across multiple languages (including English and Persian) and various financial markets worldwide. Our advanced NLP models analyze news articles, social media, and market data to deliver actionable insights.

## 🚀 Key Features

- **Global Market Coverage**: Analyze sentiment across stocks, forex, and cryptocurrencies
- **Multi-language Support**: Specialized financial terminology in English and Persian
- **Event-Aware Analysis**: Detect market events and correlate with sentiment shifts
- **Rumor Detection**: Identify and analyze potential market manipulation
- **Real-time Analysis**: Process and analyze data as it arrives
- **Advanced NLP**: State-of-the-art models for accurate sentiment detection
- **Comprehensive API**: Easy integration with your existing systems
- **Beautiful Dashboard**: Intuitive interface for market insights

## 🧠 Advanced Features

### Event-Aware Sentiment Analysis
- Detect market events (earnings calls, central bank meetings, political news)
- Auto-tag news with events using Named Entity Recognition
- Timeline visualization: "Sentiment dipped before Fed meeting"
- Correlate events with market movements

### Rumor Detection Engine
- Use clustering + NLP to detect unverified rumors
- Track message spread across multiple sources
- Calculate confidence scores for rumor verification
- Alert system for potential market manipulation
- Anti-fake-news radar for financial content

## 📊 Quick Start

### Using Docker (Recommended)

```bash
docker pull timamousavi/finsentrix
docker run -p 8000:8000 timamousavi/finsentrix
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Timamousavi/finsentrix.git
cd finsentrix

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Python Package

```bash
pip install finsentrix
```

```python
from finsentrix import FinSentrix

# Initialize the analyzer
fsx = FinSentrix()

# Analyze text with event detection
result = fsx.analyze_with_events(
    "Central Bank announced interest rate hike",
    detect_events=True
)

# Detect rumors
rumors = fsx.detect_rumors([
    {"text": "Rumor about company X", "timestamp": "2024-02-20T10:00:00Z"}
])
```

## 📈 Example Results

Check out our [examples directory](examples/) for sample visualizations and insights:

- [Market Sentiment Trends](examples/market_trends.md)
- [Event-Sentiment Correlation](examples/event_correlation.md)
- [Rumor Analysis Dashboard](examples/rumor_analysis.md)
- [Crypto Market Analysis](examples/crypto_analysis.md)
- [Persian Market Insights](examples/persian_insights.md)

## 🛠️ Development

```bash
# Set up development environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8
black .
```

## 📚 Documentation

- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Model Architecture](docs/ARCHITECTURE.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@finsentrix.com or join our [Discord community](https://discord.gg/finsentrix).

## 🙏 Acknowledgments

- State-of-the-art NLP models from Hugging Face
- Modern web frameworks (FastAPI, React)
- Open-source financial data providers

## Project Structure

```
finsentrix/
├── data/                    # Data collection and processing
│   ├── raw/                # Raw collected data
│   ├── processed/          # Processed data
│   └── README.md          # Data documentation
├── src/                    # Source code
│   ├── api/               # API implementation
│   ├── config/            # Configuration files
│   ├── database/          # Database models and migrations
│   ├── models/            # ML models
│   │   ├── event_detector.py
│   │   ├── rumor_detector.py
│   │   └── sentiment_analyzer.py
│   └── utils/             # Utilities
│       ├── text_processor.py
│       └── visualization.py
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── api/              # API tests
├── docs/                  # Documentation
│   ├── API.md            # API documentation
│   ├── USER_GUIDE.md     # User guide
│   ├── DEVELOPER_GUIDE.md # Developer guide
│   └── ARCHITECTURE.md   # Architecture documentation
├── frontend/             # Frontend application
├── requirements.txt      # Dependencies
└── README.md            # Project documentation
```

## 📞 Contact

For questions or suggestions, please open an issue or contact us at support@finsentrix.com.

---

<div align="center">
  <sub>Built with ❤️ by the FinSentrix Team</sub>
</div> 