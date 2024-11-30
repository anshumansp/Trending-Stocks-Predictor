from fastapi import Header, HTTPException, Depends
from typing import Optional
import jwt
from datetime import datetime, timedelta
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
mongo_client: Optional[AsyncIOMotorClient] = None

async def get_mongo_client() -> AsyncIOMotorClient:
    global mongo_client
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(MONGO_URL)
    return mongo_client

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client: Optional[aioredis.Redis] = None

async def get_redis_client() -> aioredis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def close_mongo_client():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        mongo_client = None

async def close_redis_client():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from headers"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required")
    
    # Check if API key is valid (implement your validation logic)
    if not is_valid_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key

def is_valid_api_key(api_key: str) -> bool:
    """Validate API key"""
    # Implement your API key validation logic
    return True  # Placeholder

async def get_current_user(authorization: str = Header(...)):
    """Get current user from JWT token"""
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        user_id = payload.get('sub')
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_id
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_cached_analysis(symbol: str) -> Optional[dict]:
    """Get cached analysis result"""
    redis = get_redis_client()
    cached = redis.get(f"analysis:{symbol}")
    return cached.decode() if cached else None

def cache_analysis(symbol: str, result: dict, expire: int = 3600):
    """Cache analysis result"""
    redis = get_redis_client()
    redis.setex(f"analysis:{symbol}", expire, str(result))

async def get_rate_limit(api_key: str = Depends(verify_api_key)):
    """Get rate limit for API key"""
    # Implement rate limiting logic
    return {
        'limit': 100,
        'remaining': 95,
        'reset': int((datetime.now() + timedelta(hours=1)).timestamp())
    }
