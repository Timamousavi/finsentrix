# FinSentrix Architecture

This document provides an overview of the FinSentrix system architecture.

## System Overview

FinSentrix is a distributed system with the following main components:

1. Frontend (React/TypeScript)
2. Backend API (FastAPI/Python)
3. Database (PostgreSQL)
4. Machine Learning Models
5. Event Detection System
6. Rumor Analysis Engine

## Component Architecture

### Frontend

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── store/         # Redux store
│   ├── services/      # API services
│   ├── hooks/         # Custom React hooks
│   └── utils/         # Utility functions
```

### Backend

```
src/
├── api/              # FastAPI application
├── models/           # ML models
├── database/         # Database models and operations
├── utils/            # Utility functions
├── core/             # Core business logic
└── config/           # Configuration
```

## Data Flow

1. User submits text through frontend
2. Frontend sends request to API
3. API processes request:
   - Text preprocessing
   - Sentiment analysis
   - Event detection
   - Rumor analysis
4. Results stored in database
5. Response sent back to frontend
6. Frontend displays results

## Database Schema

### Main Tables

- users: User information
- analyses: Sentiment analysis results
- events: Detected market events
- rumors: Detected rumors
- market_data: Market data points
- logs: System logs

## API Architecture

### REST Endpoints

- /analyze: Text sentiment analysis
- /events: Event detection
- /rumors: Rumor analysis
- /model: Model information
- /auth: Authentication

### WebSocket Endpoints

- /ws/updates: Real-time updates
- /ws/alerts: Alert notifications

## Machine Learning Pipeline

1. Text Preprocessing
   - Tokenization
   - Stopword removal
   - Stemming
   - Feature extraction

2. Model Training
   - Data collection
   - Feature engineering
   - Model training
   - Evaluation
   - Deployment

3. Inference
   - Text processing
   - Model prediction
   - Result formatting

## Event Detection System

1. Text Analysis
   - NER for entities
   - Keyword matching
   - Pattern recognition

2. Event Classification
   - Type detection
   - Impact assessment
   - Confidence scoring

## Rumor Analysis Engine

1. Pattern Detection
   - Source analysis
   - Content analysis
   - Propagation tracking

2. Verification
   - Fact-checking
   - Source reliability
   - Impact assessment

## Security Architecture

1. Authentication
   - JWT tokens
   - OAuth2 integration
   - Session management

2. Authorization
   - Role-based access
   - Permission system
   - API key management

3. Data Protection
   - Encryption at rest
   - Secure communication
   - Data sanitization

## Monitoring and Logging

1. Metrics Collection
   - Performance metrics
   - Usage statistics
   - Error rates

2. Logging
   - Application logs
   - Access logs
   - Error logs

3. Alerting
   - System health
   - Performance issues
   - Security events

## Deployment Architecture

1. Containerization
   - Docker containers
   - Kubernetes orchestration
   - Service mesh

2. CI/CD Pipeline
   - Automated testing
   - Continuous integration
   - Continuous deployment

3. Infrastructure
   - Cloud providers
   - Load balancing
   - Auto-scaling

## Future Considerations

1. Scalability
   - Horizontal scaling
   - Caching strategies
   - Database sharding

2. Performance
   - Query optimization
   - Caching layers
   - Async processing

3. Features
   - Additional languages
   - More market types
   - Advanced analytics 