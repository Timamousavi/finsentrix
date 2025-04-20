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
- **Real-time Analysis**: Process and analyze data as it arrives
- **Advanced NLP**: State-of-the-art models for accurate sentiment detection
- **Comprehensive API**: Easy integration with your existing systems
- **Beautiful Dashboard**: Intuitive interface for market insights

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
from finsentrix import SentimentAnalyzer

# Initialize the analyzer
analyzer = SentimentAnalyzer()

# Analyze text
result = analyzer.analyze("Bitcoin shows strong bullish momentum")
print(result.sentiment)  # Output: positive
```

## 📈 Example Results

Check out our [examples directory](examples/) for sample visualizations and insights:

- [Market Sentiment Trends](examples/market_trends.md)
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
├── data/
│   ├── raw/                  # Raw collected data
│   ├── processed/            # Processed data
│   └── README.md            # Data documentation
├── src/
│   ├── api/                 # API implementation
│   ├── data/                # Data collection
│   ├── models/              # ML models
│   └── utils/               # Utilities
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt         # Dependencies
└── README.md               # Project documentation
```

## Documentation

- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Data Documentation](data/README.md)

## License

This project is licensed under a dual-license agreement:
- **Academic License**: Free for non-commercial, academic use
- **Commercial License**: Requires a separate license agreement for commercial use

For commercial licensing inquiries, please contact:
- Email: licensing@finsentrix.com
- Website: https://finsentrix.com/licensing

See [LICENSE](LICENSE) for full terms and conditions.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support, please contact:
- Email: fatemehmousavy@ut.ac.ir
- Documentation: https://docs.finsentrix.com
- Community: https://community.finsentrix.com

## Acknowledgments

- [Hazm](https://github.com/sobhe/hazm) - Persian text processing library
- [Transformers](https://huggingface.co/transformers/) - State-of-the-art NLP models
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

## 📞 Contact

For questions or suggestions, please open an issue or contact us at [fatemehmousavy@ut.ac.ir](mailto:fatemehmousavy@ut.ac.ir).

---

<div align="center">
  <sub>Built with ❤️ by Tima Mousavi</sub>
</div> 