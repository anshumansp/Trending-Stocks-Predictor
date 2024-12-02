# Backend Setup Guide 🚀

## Prerequisites 📋

- Python 3.8+
- pip
- virtualenv
- AWS CLI configured
- Git

## Installation Steps 🔧

### 1. Clone Repository
```bash
git clone [repository-url]
cd aws-orchestrator/backend
```

### 2. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
.\venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
API_PORT=5000
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

## Project Structure 📁

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core functionality
│   ├── models/        # Data models
│   ├── services/      # Business logic
│   └── utils/         # Utilities
├── tests/             # Test files
├── config/            # Configuration
└── requirements.txt   # Dependencies
```

## Configuration ⚙️

### 1. AWS Configuration
```ini
# ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

# ~/.aws/config
[default]
region = us-east-1
output = json
```

### 2. Application Configuration
```python
# config/settings.py
class Config:
    API_PORT = 5000
    AWS_REGION = "us-east-1"
    LOG_LEVEL = "INFO"
    
    @classmethod
    def from_env(cls):
        return cls(
            API_PORT=int(os.getenv("API_PORT", 5000)),
            AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO")
        )
```

## Database Setup 💾

### 1. Local Development
```bash
# Install PostgreSQL
# Windows
choco install postgresql

# Start PostgreSQL service
# Windows
net start postgresql
```

### 2. Database Configuration
```python
# config/database.py
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "aws_orchestrator",
    "user": "postgres",
    "password": "your_password"
}
```

## Running the Application 🏃‍♂️

### 1. Development Server
```bash
# Start development server
python run.py

# With custom port
python run.py --port 8000
```

### 2. Production Server
```bash
# Using gunicorn
gunicorn app:app --workers 4 --bind 0.0.0.0:5000
```

## Testing 🧪

### 1. Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### 2. Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Run specific test file
pytest tests/integration/test_aws_service.py
```

## Logging 📝

### 1. Log Configuration
```python
# config/logging.py
LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard",
            "level": "DEBUG"
        }
    }
}
```

### 2. Log Usage
```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    try:
        # Some operation
        logger.info("Operation successful")
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
```

## Security Setup 🔐

### 1. SSL Configuration
```python
# config/ssl.py
SSL_CONFIG = {
    "cert_path": "/path/to/cert.pem",
    "key_path": "/path/to/key.pem",
    "ca_path": "/path/to/ca.pem"
}
```

### 2. Authentication Setup
```python
# config/auth.py
AUTH_CONFIG = {
    "jwt_secret": "your-secret-key",
    "token_expiry": 3600,
    "refresh_expiry": 86400
}
```

## Monitoring Setup 📊

### 1. Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aws-orchestrator'
    static_configs:
      - targets: ['localhost:5000']
```

### 2. Metrics Collection
```python
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

response_time = Histogram(
    'http_response_time_seconds',
    'HTTP response time'
)
```

## Troubleshooting 🔧

### Common Issues

1. **Database Connection**
```bash
# Check PostgreSQL status
pg_isready

# Reset PostgreSQL password
psql -U postgres -c "ALTER USER postgres PASSWORD 'new_password';"
```

2. **AWS Connectivity**
```bash
# Test AWS credentials
aws sts get-caller-identity

# Check AWS configuration
aws configure list
```

## Best Practices 📚

1. **Development**
   - Use virtual environments
   - Follow PEP 8
   - Write tests
   - Document code

2. **Security**
   - Secure credentials
   - Use HTTPS
   - Implement rate limiting
   - Regular updates

3. **Performance**
   - Cache responses
   - Use async operations
   - Optimize queries
   - Monitor resources

4. **Deployment**
   - Use CI/CD
   - Version control
   - Backup data
   - Monitor logs
