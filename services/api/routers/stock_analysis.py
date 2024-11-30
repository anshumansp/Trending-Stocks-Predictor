from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..models import (
    StockAnalysisRequest,
    HistoricalDataRequest,
    TechnicalIndicatorRequest,
    SentimentAnalysisRequest,
    WatchlistRequest,
    AlertRequest,
    AnalysisResponse,
    ErrorResponse,
    IndianStockRequest,
    IndianStockResponse
)
from ..dependencies import (
    verify_api_key,
    get_current_user,
    get_rate_limit,
    get_cached_analysis,
    cache_analysis
)
from ...agents.orchestrator import StockAnalysisOrchestrator
from ...agents.indian_stock_data_agent import IndianStockDataAgent
from ..services.claude_service import ClaudeService

router = APIRouter(prefix="/api/v1/stock", tags=["stock"])
orchestrator = StockAnalysisOrchestrator()
indian_stock_agent = IndianStockDataAgent()
claude_service = ClaudeService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(
    request: StockAnalysisRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    rate_limit: dict = Depends(get_rate_limit)
):
    """
    Analyze a stock and provide comprehensive insights
    """
    try:
        # Check cache first
        cached_result = get_cached_analysis(request.symbol)
        if cached_result:
            return AnalysisResponse(**cached_result)

        # Perform analysis
        result = await orchestrator.analyze_stock(
            request.symbol,
            include_technical=request.include_technical,
            include_sentiment=request.include_sentiment,
            include_growth=request.include_growth
        )

        # Cache result in background
        background_tasks.add_task(cache_analysis, request.symbol, result)

        return AnalysisResponse(
            status="success",
            symbol=request.symbol,
            timestamp=datetime.now(),
            **result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical", response_model=dict)
async def get_historical_data(
    request: HistoricalDataRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Get historical stock data
    """
    try:
        result = await orchestrator.stock_agent.process({
            'action': 'historical_data',
            'symbol': request.symbol,
            'start_date': request.start_date,
            'end_date': request.end_date,
            'interval': request.interval
        })
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/technical", response_model=dict)
async def calculate_technical_indicators(
    request: TechnicalIndicatorRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Calculate technical indicators for a stock
    """
    try:
        result = await orchestrator.stock_agent.process({
            'action': 'technical_indicators',
            'symbol': request.symbol,
            'indicators': request.indicators,
            'period': request.period
        })
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sentiment", response_model=dict)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze sentiment for a stock using Claude's advanced NLP capabilities
    """
    try:
        # Get news and financial data
        news_data = await orchestrator.sentiment_agent.process({
            'action': 'fetch_news',
            'symbol': request.symbol,
            'timeframe': request.timeframe
        })
        
        financial_data = await orchestrator.stock_agent.process({
            'action': 'get_financials',
            'symbol': request.symbol
        })

        # Use Claude for advanced sentiment analysis
        claude_analysis = await claude_service.analyze_stock_sentiment(
            company_name=request.symbol,
            news_data=news_data,
            financial_data=financial_data
        )

        # Combine with traditional sentiment analysis
        traditional_analysis = await orchestrator.sentiment_agent.process({
            'action': 'analyze',
            'symbol': request.symbol,
            'sources': request.sources,
            'timeframe': request.timeframe
        })

        # Merge both analyses
        result = {
            'claude_analysis': claude_analysis,
            'traditional_analysis': traditional_analysis,
            'timestamp': datetime.now().isoformat(),
            'symbol': request.symbol
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/watchlist", response_model=dict)
async def manage_watchlist(
    request: WatchlistRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Manage user's stock watchlist
    """
    try:
        # Implement watchlist management
        return {
            'status': 'success',
            'message': 'Watchlist updated',
            'symbols': request.symbols
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alert", response_model=dict)
async def set_alert(
    request: AlertRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Set price alert for a stock
    """
    try:
        # Implement alert setting
        return {
            'status': 'success',
            'message': 'Alert set successfully',
            'alert': {
                'symbol': request.symbol,
                'condition': request.condition,
                'value': request.value
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-summary", response_model=dict)
async def get_market_summary(
    api_key: str = Depends(verify_api_key)
):
    """
    Get comprehensive market summary using Claude's analysis
    """
    try:
        # Get market data
        market_data = await orchestrator.stock_agent.process({
            'action': 'market_summary'
        })

        # Get economic indicators
        economic_data = await orchestrator.stock_agent.process({
            'action': 'economic_indicators'
        })

        # Get global events
        global_events = await orchestrator.sentiment_agent.process({
            'action': 'global_events'
        })

        # Get Claude's market insights
        claude_insights = await claude_service.generate_market_insights(
            market_data=market_data,
            economic_indicators=economic_data,
            global_events=global_events
        )

        # Combine all data
        result = {
            'market_data': market_data,
            'economic_indicators': economic_data,
            'global_events': global_events,
            'claude_insights': claude_insights,
            'timestamp': datetime.now().isoformat()
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fundamentals/{symbol}", response_model=dict)
async def analyze_fundamentals(
    symbol: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get comprehensive fundamental analysis using Claude
    """
    try:
        # Get company data
        company_data = await orchestrator.stock_agent.process({
            'action': 'company_fundamentals',
            'symbol': symbol
        })

        # Get industry data
        industry_data = await orchestrator.stock_agent.process({
            'action': 'industry_metrics',
            'symbol': symbol
        })

        # Get competitor data
        competitor_data = await orchestrator.stock_agent.process({
            'action': 'competitor_analysis',
            'symbol': symbol
        })

        # Get Claude's fundamental analysis
        claude_analysis = await claude_service.analyze_company_fundamentals(
            company_data=company_data,
            industry_data=industry_data,
            competitor_data=competitor_data
        )

        # Combine all analyses
        result = {
            'company_data': company_data,
            'industry_data': industry_data,
            'competitor_data': competitor_data,
            'claude_analysis': claude_analysis,
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/indian", response_model=IndianStockResponse)
async def analyze_indian_stock(
    request: IndianStockRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    rate_limit: dict = Depends(get_rate_limit)
):
    """
    Analyze an Indian stock (NSE/BSE) and provide comprehensive insights
    """
    try:
        # Check cache first
        cache_key = f"{request.symbol}_{request.exchange}"
        cached_result = get_cached_analysis(cache_key)
        if cached_result:
            return IndianStockResponse(**cached_result)

        # Perform analysis
        result = await indian_stock_agent.process_request(
            f"Analyze {request.symbol} on {request.exchange}",
            context={
                'include_technical': request.include_technical,
                'include_sentiment': request.include_sentiment,
                'include_growth': request.include_growth,
                'timestamp': datetime.utcnow()
            }
        )

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        # Format response
        response_data = {
            'symbol': request.symbol,
            'exchange': request.exchange,
            'current_price': result['raw_data']['current_price'],
            'market_cap': result['raw_data']['market_cap'],
            'pe_ratio': result['raw_data']['pe_ratio'],
            'volume': result['raw_data']['volume'],
            'fifty_two_week_high': result['raw_data']['fifty_two_week_high'],
            'fifty_two_week_low': result['raw_data']['fifty_two_week_low'],
            'year_price_change': result['raw_data']['year_price_change'],
            'analysis': result['stock_data'],
            'timestamp': result.get('timestamp', datetime.utcnow()),
            'status': 'success'
        }

        # Cache the result in background
        background_tasks.add_task(cache_analysis, cache_key, response_data)

        return IndianStockResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/india")
async def get_indian_market_summary(
    api_key: str = Depends(verify_api_key)
):
    """
    Get comprehensive Indian market summary using Claude's analysis
    """
    try:
        # Analyze major Indian indices
        nifty_analysis = await indian_stock_agent.process_request("Analyze NIFTY50.NS")
        sensex_analysis = await indian_stock_agent.process_request("Analyze SENSEX.BO")
        
        # Get Claude's market analysis
        market_prompt = f"""Analyze the current Indian market conditions:

Nifty 50:
{nifty_analysis['stock_data']}

Sensex:
{sensex_analysis['stock_data']}

Please provide:
1. Overall Market Sentiment
2. Key Market Movers
3. Sector Performance
4. FII/DII Activity
5. Global Market Impact
6. Technical Outlook
7. Market Risks and Opportunities
"""
        
        market_analysis = await claude_service.analyze_text(market_prompt)
        
        return {
            'nifty50': nifty_analysis['raw_data'],
            'sensex': sensex_analysis['raw_data'],
            'market_analysis': market_analysis,
            'timestamp': datetime.utcnow(),
            'status': 'success'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
