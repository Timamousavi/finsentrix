# FinSentrix (FSX) Deployment Guide

## Overview

This guide provides detailed instructions for deploying FinSentrix (FSX) in various environments, from development to production.

## Deployment Options

### 1. Local Development

#### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Git

#### Setup
```bash
# Clone repository
git clone https://github.com/your-org/finsentrix.git
cd finsentrix

# Create virtual environment
python -m venv finsentrix-env
source finsentrix-env/bin/activate  # On Windows: finsentrix-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python src/scripts/init_db.py

# Start services
python src/scripts/start_services.py
```

### 2. Docker Deployment

#### Prerequisites
- Docker
- Docker Compose

#### Setup
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

#### Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/finsentrix
    depends_on:
      - db
      - redis

  db:
    image: postgres:12
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=finsentrix
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3. Kubernetes Deployment

#### Prerequisites
- Kubernetes cluster
- kubectl
- Helm

#### Setup
```bash
# Add Helm repository
helm repo add finsentrix https://charts.finsentrix.com

# Install chart
helm install finsentrix finsentrix/finsentrix \
  --set env=production \
  --set database.url=postgresql://user:pass@db:5432/finsentrix
```

#### Configuration
```yaml
# values.yaml
replicaCount: 3
image:
  repository: finsentrix/api
  tag: latest
env: production
database:
  url: postgresql://user:pass@db:5432/finsentrix
redis:
  url: redis://redis:6379
```

### 4. Cloud Deployment

#### AWS Setup
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name finsentrix

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service --cluster finsentrix --service-name finsentrix-api --task-definition finsentrix:1
```

#### GCP Setup
```bash
# Create cluster
gcloud container clusters create finsentrix

# Deploy application
kubectl apply -f k8s/
```

## Configuration

### Environment Variables

```bash
# Required
ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379

# Optional
LOG_LEVEL=INFO
API_KEY=your_api_key
MODEL_PATH=/models/v1
```

### Database Setup

```sql
-- Create database
CREATE DATABASE finsentrix;

-- Create user
CREATE USER finsentrix WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE finsentrix TO finsentrix;
```

### Redis Setup

```bash
# Configure Redis
redis-cli config set maxmemory 1gb
redis-cli config set maxmemory-policy allkeys-lru
```

## Monitoring

### Metrics

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'finsentrix'
    static_configs:
      - targets: ['localhost:8000']
```

### Logging

```python
# logging.conf
[loggers]
keys=root,finsentrix

[handlers]
keys=console,file

[formatters]
keys=simple,detailed

[logger_root]
level=INFO
handlers=console

[logger_finsentrix]
level=DEBUG
handlers=console,file
qualname=finsentrix
```

### Alerts

```yaml
# alerts.yml
groups:
- name: finsentrix
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate on {{ $labels.instance }}
```

## Scaling

### Horizontal Scaling

```bash
# Scale API
kubectl scale deployment finsentrix-api --replicas=5

# Scale workers
kubectl scale deployment finsentrix-worker --replicas=3
```

### Vertical Scaling

```yaml
# resources.yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump -U user -d finsentrix > backup.sql

# Restore backup
psql -U user -d finsentrix < backup.sql
```

### Redis Backup

```bash
# Create backup
redis-cli SAVE

# Restore backup
redis-cli --pipe < dump.rdb
```

## Security

### SSL/TLS

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name api.finsentrix.com;

    ssl_certificate /etc/ssl/certs/finsentrix.crt;
    ssl_certificate_key /etc/ssl/private/finsentrix.key;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### Authentication

```python
# auth.py
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read": "Read access",
        "write": "Write access"
    }
)
```

## Maintenance

### Updates

```bash
# Update application
git pull
pip install -r requirements.txt
python src/scripts/update.py

# Update database
alembic upgrade head
```

### Monitoring

```bash
# Check status
curl http://localhost:8000/health

# View logs
tail -f /var/log/finsentrix/app.log
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   ```bash
   # Check connection
   psql -U user -d finsentrix -c "\conninfo"
   ```

2. **Redis Connection**
   ```bash
   # Check connection
   redis-cli ping
   ```

3. **API Health**
   ```bash
   # Check health
   curl http://localhost:8000/health
   ```

### Log Analysis

```bash
# View error logs
grep ERROR /var/log/finsentrix/app.log

# Analyze performance
cat /var/log/finsentrix/app.log | grep "processing_time"
```

## Support

For deployment support:
- Documentation: https://docs.finsentrix.com
- Issues: https://github.com/your-org/finsentrix/issues
- Email: ops@finsentrix.com 