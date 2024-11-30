import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ANTHROPIC_CONFIG = {
    'api_key': os.getenv('ANTHROPIC_API_KEY'),
    'model': 'claude-3-haiku-20240307',
    'streaming': True,
    'max_tokens': 4096,
    'temperature': 0.7
}

# Agent configuration
AGENT_CONFIG = {
    'stock_data': {
        'name': 'Stock Data Agent',
        'description': 'Specializes in analyzing stock market data, technical indicators, and price trends.',
        'streaming': True
    },
    'sentiment': {
        'name': 'Sentiment Analysis Agent',
        'description': 'Analyzes market sentiment, news, and social media trends for stocks.',
        'streaming': True
    },
    'growth': {
        'name': 'Growth Analysis Agent',
        'description': 'Evaluates company growth potential, financial metrics, and market position.',
        'streaming': True
    }
}
