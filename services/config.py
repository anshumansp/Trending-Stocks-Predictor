"""Configuration settings for the services"""

ANTHROPIC_CONFIG = {
    "api_key": "",  # Add your Anthropic API key here
    "model": "claude-2",
    "temperature": 0.7,
    "max_tokens": 1000
}

NSE_CONFIG = {
    "base_url": "https://www.nseindia.com",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "headers": {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
}
