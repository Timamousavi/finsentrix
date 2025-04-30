# FinSentrix (FSX) - Global Financial Sentiment Analysis

A comprehensive system for analyzing sentiment in financial texts across multiple languages and markets, providing real-time market insights and sentiment indicators.

## Features

- **Multi-language Support**: Advanced sentiment analysis for both English and Persian financial texts
- **Market Coverage**: Analysis across Stocks, Forex, and Cryptocurrency markets
- **Real-time Data Processing**: Integration with multiple data sources (Twitter, News, Telegram)
- **Event Detection**: Automatic detection of market events and rumors
- **Timeline Visualization**: Interactive visualization of market trends and sentiment
- **API Access**: RESTful API for integration with other systems
- **Dashboard**: Real-time visualization of market sentiment across different markets

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

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the application in your web browser:
   - Dashboard: http://localhost:8000/dashboard
   - API Documentation: http://localhost:8000/docs
   - Home Page: http://localhost:8000/

### Example Usage

#### English Text Analysis
```python
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Bitcoin shows strong bullish momentum",
        "language": "en",
        "market_type": "crypto"
    }
)
```

#### Persian Text Analysis
```python
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "این شرکت در سال جاری عملکرد خوبی داشته است",
        "language": "fa",
        "market_type": "stock"
    }
)
```

#### Real-time Market Analysis
```python
response = requests.get(
    "http://localhost:8000/api/dashboard/real-time",
    params={
        "market_types": ["stock", "forex", "crypto"],
        "sources": ["twitter", "news", "telegram"]
    }
)
```

### API Endpoints

- `GET /`: API information
- `POST /analyze`: Single text sentiment analysis
- `POST /analyze/batch`: Batch sentiment analysis
- `GET /api/dashboard/real-time`: Real-time market data
- `GET /api/events`: Market events detection
- `GET /api/rumors`: Rumor analysis
- `GET /health`: Health check

### Troubleshooting

If you cannot access the application:

1. Check if the server is running:
```bash
netstat -ano | findstr :8000
```

2. If the port is in use, stop existing processes:
```bash
taskkill /F /PID <process_id>
```

3. Common issues and solutions:
   - **Firewall Blocking**: Add an inbound rule for port 8000 in Windows Defender Firewall
   - **Port Already in Use**: Stop any other applications using port 8000
   - **Browser Issues**: Try clearing cache or using a different browser
   - **Connection Refused**: Make sure the server is running with the correct host configuration

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

This project is licensed under the Dual License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- [Hazm](https://github.com/roshan-research/hazm) for Persian NLP
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [React](https://reactjs.org/) for the frontend
