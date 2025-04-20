# FinSentrix (FSX) Developer Guide

## Introduction

This guide provides comprehensive information for developers working with the FinSentrix (FSX) codebase. It covers architecture, development workflow, and best practices.

## System Architecture

### Core Components

1. **Data Collection Layer**
   - Web scraping
   - Telegram integration
   - Real-time data feeds
   - Data validation

2. **Processing Layer**
   - Text normalization
   - Language detection
   - Market classification
   - Sentiment analysis

3. **API Layer**
   - RESTful endpoints
   - Authentication
   - Rate limiting
   - Error handling

4. **Storage Layer**
   - Database management
   - Cache system
   - File storage
   - Data versioning

### Technology Stack

- **Backend**: Python 3.9+
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **NLP**: Transformers, Hazm
- **Testing**: pytest
- **Documentation**: Sphinx

## Development Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+
- Redis 6+
- Git

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/timamousavi/finsentrix.git
   cd finsentrix
   ```

2. **Set Up Environment**
   ```bash
   # Create virtual environment
   python -m venv finsentrix-env
   source finsentrix-env/bin/activate  # On Windows: finsentrix-env\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure Development Environment**
   ```bash
   # Copy environment files
   cp .env.example .env
   cp .env.test.example .env.test

   # Set up database
   python src/scripts/init_db.py
   ```

## Code Structure

```
finsentrix/
├── src/
│   ├── api/              # API endpoints
│   ├── data/             # Data collection
│   ├── models/           # ML models
│   ├── utils/            # Utilities
│   └── config/           # Configuration
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── api/              # API tests
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Development Workflow

1. **Branch Management**
   ```bash
   # Create feature branch
   git checkout -b feature/your-feature

   # Create bugfix branch
   git checkout -b bugfix/your-bugfix

   # Create release branch
   git checkout -b release/v1.0.0
   ```

2. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Document functions
   - Write unit tests

3. **Testing**
   ```bash
   # Run all tests
   pytest

   # Run specific test
   pytest tests/unit/test_specific.py

   # Run with coverage
   pytest --cov=src
   ```

4. **Documentation**
   ```bash
   # Build documentation
   cd docs
   make html
   ```

## Adding New Features

1. **Market Support**
   ```python
   # Add new market type
   class NewMarketAnalyzer(MarketAnalyzer):
       def __init__(self):
           super().__init__()
           self.market_type = "new_market"
           self.terms = load_market_terms("new_market")
   ```

2. **Language Support**
   ```python
   # Add new language
   class NewLanguageProcessor(TextProcessor):
       def __init__(self):
           super().__init__()
           self.language = "new_lang"
           self.stopwords = load_stopwords("new_lang")
   ```

3. **API Endpoints**
   ```python
   # Add new endpoint
   @router.post("/new-endpoint")
   async def new_endpoint(request: NewRequest):
       return await process_new_request(request)
   ```

## Testing

### Unit Tests

```python
def test_market_analyzer():
    analyzer = MarketAnalyzer()
    result = analyzer.analyze("Test text")
    assert result.sentiment in ["positive", "negative", "neutral"]
```

### Integration Tests

```python
async def test_api_integration():
    client = TestClient(app)
    response = client.post("/analyze", json={"text": "Test"})
    assert response.status_code == 200
```

### Performance Tests

```python
def test_analyzer_performance():
    analyzer = MarketAnalyzer()
    start_time = time.time()
    analyzer.analyze_batch(["Test"] * 1000)
    assert time.time() - start_time < 5.0
```

## Documentation

### Code Documentation

```python
def analyze_text(text: str, market_type: str) -> Dict[str, Any]:
    """
    Analyze text sentiment for specific market.

    Args:
        text: Input text to analyze
        market_type: Market type (stock, forex, crypto)

    Returns:
        Dictionary containing sentiment analysis results
    """
    pass
```

### API Documentation

```python
@router.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text sentiment.

    Request:
        text: str - Text to analyze
        market_type: str - Market type
        language: str - Text language

    Response:
        sentiment: str - Analysis result
        confidence: float - Confidence score
    """
    pass
```

## Deployment

### Production Setup

1. **Environment**
   ```bash
   # Set production environment
   export ENV=production
   export DATABASE_URL=postgresql://user:pass@host:5432/db
   ```

2. **Database**
   ```bash
   # Run migrations
   alembic upgrade head
   ```

3. **Application**
   ```bash
   # Start application
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```

### Monitoring

- Use Prometheus for metrics
- Set up Grafana dashboards
- Configure alerts
- Monitor logs

## Contributing

1. **Fork Repository**
2. **Create Branch**
3. **Make Changes**
4. **Run Tests**
5. **Submit PR**

### PR Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] All tests pass

## Support

For development support:
- Documentation: https://docs.finsentrix.com
- Issues: https://github.com/your-org/finsentrix/issues
- Email: dev@finsentrix.com 

node --version
npm --version 