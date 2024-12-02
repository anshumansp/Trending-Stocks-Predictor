# Stock Analysis API Documentation 📈

## Overview 🌐

This API provides comprehensive stock analysis capabilities, including technical analysis, sentiment analysis, and market insights for both global and Indian markets.

## Authentication 🔑

All endpoints require API key authentication via header:
```http
X-API-Key: your_api_key_here
```

## Endpoints 📡

### 1. Stock Analysis

#### Analyze Stock
```http
POST /api/v1/stock/analyze
Content-Type: application/json

{
  "symbol": "AAPL",
  "timeframe": "1d",
  "indicators": ["sma", "rsi", "macd"]
}

Response (200 OK):
{
  "symbol": "AAPL",
  "price": {
    "current": 150.23,
    "change": 2.5,
    "changePercent": 1.67
  },
  "analysis": {
    "technical": {
      "trend": "bullish",
      "indicators": {
        "sma": 148.92,
        "rsi": 65.4,
        "macd": {
          "line": 2.1,
          "signal": 1.8,
          "histogram": 0.3
        }
      }
    },
    "sentiment": {
      "score": 0.75,
      "label": "positive"
    }
  }
}
```

#### Historical Data
```http
POST /api/v1/stock/historical
Content-Type: application/json

{
  "symbol": "AAPL",
  "startDate": "2023-01-01",
  "endDate": "2023-12-31",
  "interval": "1d"
}

Response (200 OK):
{
  "symbol": "AAPL",
  "data": [
    {
      "date": "2023-12-31",
      "open": 149.8,
      "high": 151.2,
      "low": 149.5,
      "close": 150.23,
      "volume": 12345678
    }
  ]
}
```

#### Technical Indicators
```http
POST /api/v1/stock/technical
Content-Type: application/json

{
  "symbol": "AAPL",
  "indicators": ["sma", "ema", "rsi", "macd"],
  "timeframe": "1d"
}

Response (200 OK):
{
  "symbol": "AAPL",
  "indicators": {
    "sma": {
      "value": 148.92,
      "period": 20
    },
    "rsi": {
      "value": 65.4,
      "period": 14
    }
  }
}
```

#### Sentiment Analysis
```http
POST /api/v1/stock/sentiment
Content-Type: application/json

{
  "symbol": "AAPL",
  "sources": ["news", "social", "filings"]
}

Response (200 OK):
{
  "symbol": "AAPL",
  "sentiment": {
    "overall": {
      "score": 0.75,
      "label": "positive"
    },
    "sources": {
      "news": 0.8,
      "social": 0.7,
      "filings": 0.75
    }
  }
}
```

### 2. Watchlist Management

#### Manage Watchlist
```http
POST /api/v1/stock/watchlist
Content-Type: application/json
Authorization: Bearer {token}

{
  "action": "add",
  "symbols": ["AAPL", "MSFT"]
}

Response (200 OK):
{
  "watchlist": ["AAPL", "MSFT", "GOOGL"],
  "updated": "2023-12-31T00:00:00Z"
}
```

### 3. Alerts

#### Set Price Alert
```http
POST /api/v1/stock/alert
Content-Type: application/json
Authorization: Bearer {token}

{
  "symbol": "AAPL",
  "condition": "above",
  "price": 150.00,
  "notification": {
    "type": "email",
    "target": "user@example.com"
  }
}

Response (200 OK):
{
  "alertId": "alert_123",
  "status": "active",
  "created": "2023-12-31T00:00:00Z"
}
```

### 4. Market Analysis

#### Market Summary
```http
GET /api/v1/stock/market/summary

Response (200 OK):
{
  "timestamp": "2023-12-31T00:00:00Z",
  "indices": {
    "SPX": {
      "value": 4700.23,
      "change": 15.6,
      "changePercent": 0.33
    }
  },
  "sectors": {
    "technology": {
      "performance": 1.2,
      "sentiment": "bullish"
    }
  },
  "analysis": {
    "summary": "Markets showing strength...",
    "keyEvents": [
      {
        "event": "Fed Meeting",
        "impact": "positive"
      }
    ]
  }
}
```

### 5. Indian Market Analysis

#### Analyze Indian Stock
```http
POST /api/v1/stock/indian/analyze
Content-Type: application/json

{
  "symbol": "RELIANCE.NS",
  "exchange": "NSE"
}

Response (200 OK):
{
  "symbol": "RELIANCE.NS",
  "exchange": "NSE",
  "price": {
    "current": 2500.45,
    "change": 25.6,
    "changePercent": 1.03
  },
  "analysis": {
    "technical": {
      "trend": "bullish"
    },
    "fundamental": {
      "pe": 25.6,
      "marketCap": "16.7T"
    }
  }
}
```

#### Indian Market Summary
```http
GET /api/v1/stock/indian/market/summary

Response (200 OK):
{
  "timestamp": "2023-12-31T00:00:00Z",
  "indices": {
    "NIFTY50": {
      "value": 19800.45,
      "change": 125.6,
      "changePercent": 0.64
    },
    "SENSEX": {
      "value": 65900.34,
      "change": 412.3,
      "changePercent": 0.63
    }
  },
  "sectors": {
    "IT": {
      "performance": 1.5,
      "sentiment": "bullish"
    }
  }
}
```

### 6. Fundamental Analysis

#### Analyze Fundamentals
```http
POST /api/v1/stock/fundamentals/{symbol}
Content-Type: application/json

Response (200 OK):
{
  "symbol": "AAPL",
  "fundamentals": {
    "financials": {
      "revenue": "394.3B",
      "netIncome": "96.7B",
      "eps": "6.15",
      "peRatio": "30.2"
    },
    "metrics": {
      "marketCap": "2.95T",
      "dividendYield": "0.5%",
      "beta": "1.2",
      "52WeekHigh": "198.23",
      "52WeekLow": "124.17"
    },
    "analysis": {
      "strengths": [
        "Strong cash position",
        "Brand value",
        "Product ecosystem"
      ],
      "weaknesses": [
        "Supply chain dependencies",
        "High product prices"
      ],
      "opportunities": [
        "Services growth",
        "New markets"
      ],
      "threats": [
        "Competition",
        "Regulatory challenges"
      ]
    }
  }
}
```

### 7. Advanced Analytics

#### Get Market Correlation
```http
POST /api/v1/stock/correlation
Content-Type: application/json

{
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "timeframe": "1y"
}

Response (200 OK):
{
  "correlationMatrix": {
    "AAPL": {
      "MSFT": 0.85,
      "GOOGL": 0.78
    },
    "MSFT": {
      "GOOGL": 0.82
    }
  },
  "analysis": {
    "highestCorrelation": {
      "pair": ["AAPL", "MSFT"],
      "value": 0.85
    },
    "lowestCorrelation": {
      "pair": ["AAPL", "GOOGL"],
      "value": 0.78
    }
  }
}
```

#### Get Sector Performance
```http
GET /api/v1/stock/sectors/performance

Response (200 OK):
{
  "timestamp": "2023-12-31T00:00:00Z",
  "sectors": {
    "technology": {
      "performance": {
        "daily": 1.2,
        "weekly": 3.5,
        "monthly": 8.2,
        "yearly": 25.4
      },
      "topPerformers": [
        {
          "symbol": "AAPL",
          "change": 2.5
        }
      ]
    }
  },
  "analysis": {
    "bestPerforming": "technology",
    "worstPerforming": "utilities"
  }
}
```

### 8. Risk Analysis

#### Get Risk Metrics
```http
POST /api/v1/stock/risk
Content-Type: application/json

{
  "symbol": "AAPL",
  "timeframe": "1y"
}

Response (200 OK):
{
  "symbol": "AAPL",
  "riskMetrics": {
    "volatility": 25.4,
    "beta": 1.2,
    "sharpeRatio": 1.8,
    "valueAtRisk": {
      "daily": {
        "95confidence": -2.3,
        "99confidence": -3.1
      }
    }
  },
  "stressTest": {
    "marketCrash": -15.2,
    "recessionScenario": -12.5,
    "techSectorDecline": -18.7
  }
}
```

## Error Handling ⚠️

### Error Response Format
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 100,
      "reset": "2023-12-31T00:05:00Z"
    }
  }
}
```

### Common Error Codes
```typescript
const ERROR_CODES = {
  // Authentication Errors
  INVALID_API_KEY: "Invalid API key",
  TOKEN_EXPIRED: "Authentication token expired",
  
  // Request Errors
  INVALID_SYMBOL: "Invalid stock symbol",
  INVALID_TIMEFRAME: "Invalid timeframe specified",
  
  // Service Errors
  SERVICE_UNAVAILABLE: "Service temporarily unavailable",
  DATA_NOT_AVAILABLE: "Requested data not available",
  
  // Rate Limiting
  RATE_LIMIT_EXCEEDED: "API rate limit exceeded"
};
```

## Best Practices 📚

1. **Rate Limiting**
   - Global limit: 100 requests/minute
   - Burst limit: 150 requests/minute
   - Headers: X-RateLimit-Limit, X-RateLimit-Remaining

2. **Caching**
   - Analysis results cached for 5 minutes
   - Historical data cached for 1 hour
   - Market summaries cached for 1 minute

3. **Authentication**
   - API keys for general access
   - JWT tokens for user-specific operations
   - Refresh tokens for extended sessions

4. **Performance**
   - Batch requests when possible
   - Use appropriate timeframes
   - Implement request queuing

## Rate Limiting and Quotas 📊

### 1. API Tiers
```typescript
const API_TIERS = {
  basic: {
    requestsPerMinute: 60,
    endpoints: ["analyze", "historical", "technical"],
    features: ["Basic Analysis"]
  },
  premium: {
    requestsPerMinute: 300,
    endpoints: ["*"],
    features: ["All Features"]
  }
}
```

### 2. Rate Limit Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## Webhook Notifications 🔔

### 1. Configure Webhook
```http
POST /api/v1/webhooks/configure
Content-Type: application/json
Authorization: Bearer {token}

{
  "url": "https://your-server.com/webhook",
  "events": ["price_alert", "analysis_complete"],
  "secret": "your_webhook_secret"
}

Response (200 OK):
{
  "webhookId": "webhook_123",
  "status": "active",
  "created": "2023-12-31T00:00:00Z"
}
```

### 2. Webhook Payload Format
```json
{
  "event": "price_alert",
  "timestamp": "2023-12-31T00:00:00Z",
  "data": {
    "symbol": "AAPL",
    "trigger": {
      "condition": "above",
      "price": 150.00,
      "currentPrice": 151.23
    }
  },
  "signature": "sha256=..."
}
```

## Security Recommendations 🔒

1. **API Key Management**
   - Rotate keys regularly
   - Use environment variables
   - Implement key scoping

2. **Request Signing**
   - Sign all webhook payloads
   - Verify webhook signatures
   - Use HMAC SHA-256

3. **Rate Limiting**
   - Implement client-side throttling
   - Use exponential backoff
   - Monitor usage patterns

4. **Data Protection**
   - Use HTTPS only
   - Encrypt sensitive data
   - Implement request logging

## SDK Examples 💻

### Python
```python
from aws_orchestrator import StockClient

client = StockClient(api_key="your_api_key")

# Analyze a stock
analysis = client.analyze_stock("AAPL")

# Set up a price alert
alert = client.set_alert(
    symbol="AAPL",
    condition="above",
    price=150.00
)
```

### JavaScript
```javascript
import { StockClient } from 'aws-orchestrator';

const client = new StockClient({ apiKey: 'your_api_key' });

// Analyze a stock
const analysis = await client.analyzeStock('AAPL');

// Set up a price alert
const alert = await client.setAlert({
  symbol: 'AAPL',
  condition: 'above',
  price: 150.00
});
```

## Testing 🧪

### 1. Test Environment
```http
Base URL: https://api-test.aws-orchestrator.com
Test API Key: test_key_xxxxxxxxxxxx
```

### 2. Test Data
```json
{
  "testSymbols": ["TEST", "DEMO"],
  "testPrices": {
    "TEST": 100.00,
    "DEMO": 50.00
  }
}
```

### 3. Integration Testing
```python
# Example test case
def test_stock_analysis():
    client = StockClient(
        api_key="test_key",
        base_url="https://api-test.aws-orchestrator.com"
    )
    response = client.analyze_stock("TEST")
    assert response.status_code == 200
    assert "analysis" in response.data
```

## Changelog 📝

### Version 2.0.0 (2023-12-31)
- Added Indian market analysis
- Enhanced fundamental analysis
- Improved risk metrics
- Added webhook support

### Version 1.1.0 (2023-06-30)
- Added technical indicators
- Enhanced market summary
- Improved error handling

### Version 1.0.0 (2023-01-01)
- Initial API release
- Basic stock analysis
- Historical data support
