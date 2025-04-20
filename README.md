# FinSentrix (FSX)

<div align="center">
  <img src="docs/images/logo.png" alt="FinSentrix Logo" width="200"/>
  
  [![License](https://img.shields.io/badge/license-Dual-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
  [![Documentation](https://img.shields.io/badge/docs-passing-green.svg)](docs/)
  [![Tests](https://img.shields.io/badge/tests-passing-green.svg)](tests/)
</div>

## 🌐 Overview

FinSentrix (FSX) is a sophisticated sentiment analysis system designed for global financial markets. It provides real-time sentiment analysis across multiple languages (including English and Persian) and various financial markets worldwide.

### Key Features

- **Global Market Coverage**: Analyze sentiment across international markets
- **Multi-Language Support**: Including English and Persian with specialized financial terminology
- **Market-Specific Analysis**: Stocks, forex, and cryptocurrency markets worldwide
- **Real-Time Processing**: Continuous sentiment analysis with scheduled updates
- **Advanced NLP**: Specialized financial term processing and sentiment detection
- **RESTful API**: Easy integration with existing systems
- **Comprehensive Documentation**: Detailed guides for users and developers

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finsentrix.git
cd finsentrix
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python src/scripts/init_db.py
```

## 📊 Usage

### Basic Usage

```python
from src.models.sentiment_analyzer import SentimentAnalyzer

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Analyze text in English
result = analyzer.analyze(
    text="NASDAQ showing positive trends",
    language="en",
    market_type="stock"
)

# Analyze text in Persian
result = analyzer.analyze(
    text="بازار جهانی امروز روند مثبتی دارد",
    language="fa",
    market_type="stock"
)

print(result)
```

### API Usage

```python
import requests

# Analyze global market sentiment
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Global markets showing mixed signals",
        "language": "en",
        "market_type": "stock"
    },
    headers={"Authorization": "Bearer your_token"}
)
print(response.json())
```

## 📚 Documentation

- [API Documentation](docs/api/README.md)
- [User Guide](docs/user/README.md)
- [Developer Guide](docs/developer/README.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under a dual-license agreement:
- **Academic License**: Free for non-commercial, academic use
- **Commercial License**: Requires a separate license agreement for commercial use

For commercial licensing inquiries, please contact:
- Email: licensing@finsentrix.com
- Website: https://finsentrix.com/licensing

See [LICENSE](LICENSE) for full terms and conditions.

## 📞 Support

For support, please open an issue in the GitHub repository or contact us at support@finsentrix.com.

## 🌟 Acknowledgments

- [Hazm](https://github.com/roshan-research/hazm) for Persian NLP
- [Transformers](https://huggingface.co/transformers/) for sentiment analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework

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