from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class StockAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze")
    include_technical: bool = Field(True, description="Include technical analysis")
    include_sentiment: bool = Field(True, description="Include sentiment analysis")
    include_growth: bool = Field(True, description="Include growth analysis")

class HistoricalDataRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    start_date: datetime = Field(..., description="Start date for historical data")
    end_date: datetime = Field(..., description="End date for historical data")
    interval: str = Field("1d", description="Data interval (1d, 1h, etc.)")

class TechnicalIndicatorRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    indicators: List[str] = Field(..., description="List of technical indicators to calculate")
    period: int = Field(14, description="Period for indicator calculation")

class SentimentAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    sources: List[str] = Field(["twitter", "reddit", "news"], description="Sources for sentiment analysis")
    timeframe: str = Field("24h", description="Timeframe for sentiment analysis")

class WatchlistRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of stock symbols to watch")
    user_id: str = Field(..., description="User ID for watchlist")

class AlertRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    condition: str = Field(..., description="Alert condition (above, below, etc.)")
    value: float = Field(..., description="Threshold value")
    user_id: str = Field(..., description="User ID for alert")

class AnalysisResponse(BaseModel):
    status: str
    symbol: str
    timestamp: datetime
    recommendation: Dict[str, Any]
    technical_analysis: Optional[Dict[str, Any]]
    sentiment_analysis: Optional[Dict[str, Any]]
    growth_analysis: Optional[Dict[str, Any]]

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: int
