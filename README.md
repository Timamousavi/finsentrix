# FinSentrix - Persian Financial Sentiment Analysis

A comprehensive system for analyzing sentiment in Persian financial texts, providing real-time market insights and sentiment indicators.

## Features

- **Persian Text Processing**: Advanced preprocessing for Persian financial texts
- **Sentiment Analysis**: Deep learning-based sentiment analysis for financial content
- **Real-time Market Data**: Integration with financial data sources
- **Event Detection**: Automatic detection of market events and rumors
- **Multi-language Support**: English and Persian interface
- **API Access**: RESTful API for integration with other systems
- **Dashboard**: Real-time visualization of market sentiment

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis (for rate limiting)
- PostgreSQL (for data storage)

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
alembic upgrade head
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Usage

### API Endpoints

- `GET /`: API information
- `POST /analyze`: Single text sentiment analysis
- `POST /analyze/batch`: Batch sentiment analysis
- `GET /api/dashboard/real-time`: Real-time market data
- `GET /health`: Health check

### Example API Usage

```python
import requests

# Single text analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={"text": "این شرکت در سال جاری عملکرد خوبی داشته است"}
)
print(response.json())

# Batch analysis
response = requests.post(
    "http://localhost:8000/analyze/batch",
    json={"texts": [
        "این شرکت در سال جاری عملکرد خوبی داشته است",
        "سهام این شرکت ریسک بالایی دارد"
    ]}
)
print(response.json())
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run performance tests
pytest tests/test_performance.py
```

### Code Style

```bash
# Format code
black .

# Check types
mypy .

# Lint code
flake8
```

### Security

- Regular dependency updates
- Rate limiting
- Input validation
- Secure API key handling
- CORS protection

## Performance Optimization

- Async processing for batch requests
- Redis caching
- Database indexing
- Query optimization
- Memory management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- [Hazm](https://github.com/roshan-research/hazm) for Persian NLP
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [React](https://reactjs.org/) for the frontend
