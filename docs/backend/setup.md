# Backend Setup Guide

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- Git

## Installation Steps

1. Clone the repository and navigate to backend directory:
```bash
git clone [repository-url]
cd stocks-ai/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` file with your configuration:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://localhost/stocks_ai
API_KEY=your_api_key
```

5. Initialize database:
```bash
flask db upgrade
```

6. Start the development server:
```bash
flask run
```

The API will be available at `http://localhost:5000`

## Project Structure

```
backend/
├── app/
│   ├── models/        # Database models
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   ├── utils/         # Helper functions
│   └── __init__.py    # App initialization
├── tests/             # Test files
├── migrations/        # Database migrations
├── config.py         # Configuration
└── requirements.txt  # Python dependencies
```

## Running Tests

1. Set up test environment:
```bash
export FLASK_ENV=testing
```

2. Run tests:
```bash
pytest
```

3. Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Database Migrations

- Create migration:
```bash
flask db migrate -m "migration description"
```

- Apply migration:
```bash
flask db upgrade
```

- Rollback migration:
```bash
flask db downgrade
```
