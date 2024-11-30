import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_CONFIG = {
    'region_name': os.getenv('AWS_REGION', 'us-east-1'),
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
}

# LangChain Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-3.5-turbo"

# Agent Configuration
AGENT_CONFIG = {
    'max_iterations': 5,
    'early_stopping_method': 'generate',
    'verbose': True
}

# Social Media API Configuration
TWITTER_CONFIG = {
    'api_key': os.getenv('TWITTER_API_KEY'),
    'api_secret': os.getenv('TWITTER_API_SECRET'),
    'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
}

REDDIT_CONFIG = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

# Stock Data Configuration
STOCK_DATA_CONFIG = {
    'nse_url': 'https://www.nseindia.com',
    'data_directory': 'data',
    'cache_duration': 3600  # 1 hour
}

# Redis Configuration for Agent Communication
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': 0
}

# Sentiment Analysis Configuration
SENTIMENT_CONFIG = {
    'batch_size': 32,
    'max_length': 512,
    'sentiment_threshold': {
        'positive': 0.6,
        'negative': 0.4
    }
}
