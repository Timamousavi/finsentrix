# FinSentrix (FSX) API Documentation

## Overview

The FinSentrix (FSX) API provides sentiment analysis for global financial markets, supporting multiple languages (including English and Persian) and various market types worldwide. The API is designed to be simple, efficient, and secure, with a focus on international market coverage.

## Base URL

```
https://api.finsentrix.com/v1
```

## Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

To obtain a token, use the `/token` endpoint:

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

## Rate Limiting

- Free tier: 100 requests per hour
- Pro tier: 1000 requests per hour
- Enterprise tier: Custom limits

## Endpoints

### Analyze Single Text

```http
POST /analyze
Content-Type: application/json

{
    "text": "NASDAQ showing strong growth",
    "language": "en",  // Optional: "en" or "fa"
    "market_type": "stock",  // Optional: "stock", "forex", "crypto"
    "market_region": "US"  // Optional: Region code (e.g., "US", "EU", "ASIA")
}
```

Response:
```json
{
    "sentiment": "positive",
    "confidence": 0.85,
    "market_type": "stock",
    "market_region": "US",
    "language": "en",
    "timestamp": "2024-04-20T12:00:00Z"
}
```

### Analyze Multiple Texts

```http
POST /analyze/batch
Content-Type: application/json

{
    "texts": [
        "NASDAQ showing strong growth",
        "بازار جهانی امروز روند مثبتی دارد"
    ],
    "language": "auto",  // Optional: "auto", "en", "fa"
    "market_type": "stock",  // Optional
    "market_region": "global"  // Optional
}
```

Response:
```json
{
    "results": [
        {
            "text": "NASDAQ showing strong growth",
            "sentiment": "positive",
            "confidence": 0.85,
            "language": "en",
            "market_region": "US"
        },
        {
            "text": "بازار جهانی امروز روند مثبتی دارد",
            "sentiment": "positive",
            "confidence": 0.78,
            "language": "fa",
            "market_region": "global"
        }
    ],
    "summary": {
        "total": 2,
        "positive": 2,
        "negative": 0,
        "neutral": 0
    }
}
```

### Get Model Information

```http
GET /model/info
```

Response:
```json
{
    "version": "1.0.0",
    "supported_languages": ["en", "fa"],
    "supported_markets": ["stock", "forex", "crypto"],
    "supported_regions": ["US", "EU", "ASIA", "ME", "global"],
    "last_updated": "2024-04-20T12:00:00Z"
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

Error responses include a message and error code:

```json
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Text must be between 1 and 1000 characters"
    }
}
```

## Best Practices

1. **Authentication**
   - Store tokens securely
   - Rotate tokens regularly
   - Use environment variables for credentials

2. **Rate Limiting**
   - Implement exponential backoff
   - Monitor usage
   - Upgrade plan if needed

3. **Error Handling**
   - Implement retry logic
   - Log errors
   - Handle rate limits gracefully

4. **Performance**
   - Use batch endpoints for multiple texts
   - Cache results when possible
   - Monitor API latency

5. **Market Analysis**
   - Specify market region when known
   - Use appropriate language codes
   - Consider timezone differences

## Support

For API support:
- Email: api@finsentrix.com
- Documentation: https://docs.finsentrix.com
- Status Page: https://status.finsentrix.com 