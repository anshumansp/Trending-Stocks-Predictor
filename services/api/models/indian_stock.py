from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class IndianStockRequest(BaseModel):
    symbol: str
    exchange: str = "NSE"  # Default to NSE
    include_technical: bool = True
    include_sentiment: bool = True
    include_growth: bool = True

class IndianStockResponse(BaseModel):
    symbol: str
    exchange: str
    current_price: str
    market_cap: str
    pe_ratio: float
    volume: int
    fifty_two_week_high: str
    fifty_two_week_low: str
    year_price_change: float
    analysis: Dict[str, Any]
    timestamp: datetime
    status: str

class IndianMarketSummary(BaseModel):
    nifty50: Dict[str, Any]
    sensex: Dict[str, Any]
    market_analysis: str
    timestamp: datetime
    status: str
