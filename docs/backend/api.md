# API Documentation

## Authentication

All API requests require an API key to be included in the header:
```
Authorization: Bearer your_api_key
```

## API Endpoints

### Stock Predictions

#### Get Stock Prediction
```http
GET /api/v1/predictions/{symbol}
```

Parameters:
- `symbol` (required): Stock symbol (e.g., AAPL, GOOGL)
- `timeframe` (optional): Prediction timeframe (default: '1d')

Response:
```json
{
    "symbol": "AAPL",
    "prediction": {
        "price": 150.25,
        "confidence": 0.85,
        "timestamp": "2023-12-20T10:00:00Z"
    }
}
```

#### Get Historical Data
```http
GET /api/v1/historical/{symbol}
```

Parameters:
- `symbol` (required): Stock symbol
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)

Response:
```json
{
    "symbol": "AAPL",
    "data": [
        {
            "date": "2023-12-20",
            "open": 148.5,
            "close": 150.25,
            "high": 151.0,
            "low": 148.0,
            "volume": 1234567
        }
    ]
}
```

### User Management

#### Create User Account
```http
POST /api/v1/users
```

Request Body:
```json
{
    "email": "user@example.com",
    "password": "secure_password",
    "name": "John Doe"
}
```

#### User Login
```http
POST /api/v1/auth/login
```

Request Body:
```json
{
    "email": "user@example.com",
    "password": "secure_password"
}
```

## Error Responses

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Error description"
    }
}
```

Common Error Codes:
- `AUTH_REQUIRED`: Authentication required
- `INVALID_CREDENTIALS`: Invalid login credentials
- `INVALID_SYMBOL`: Invalid stock symbol
- `RATE_LIMIT`: Rate limit exceeded
- `SERVER_ERROR`: Internal server error

## Rate Limiting

- API requests are limited to 100 requests per minute per API key
- Historical data requests are limited to 500 requests per day per API key

## Websocket API

Connect to real-time updates:
```javascript
ws://api.stocks-ai.com/ws?token=your_api_key
```

Events:
- `price_update`: Real-time price updates
- `prediction_update`: New prediction available
- `market_alert`: Market alerts and notifications
