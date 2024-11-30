from typing import Dict, Any, Optional
import yfinance as yf
import pandas as pd
from base_agent import BaseStockAgent

class StockDataAgent(BaseStockAgent):
    def __init__(self):
        super().__init__(
            name="Stock Data Agent",
            description="Fetches and analyzes stock market data, including prices, volumes, and technical indicators."
        )
        self.cache = {}

    def _get_capabilities(self) -> Dict[str, Any]:
        return {
            'real_time_data': True,
            'historical_data': True,
            'technical_analysis': True,
            'fundamental_data': True,
            'market_data': True
        }

    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a stock data request"""
        # First, get the stock data
        symbol = self._extract_symbol(request)
        if not symbol:
            return {
                'error': 'No stock symbol found in request',
                'source': 'claude-3-haiku',
                'analysis_type': 'stock_data'
            }

        try:
            # Fetch stock data
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1y")
            info = stock.info

            # Prepare data for Claude's analysis
            data_context = {
                'symbol': symbol,
                'current_price': info.get('regularMarketPrice', 'N/A'),
                'volume': info.get('regularMarketVolume', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('forwardPE', 'N/A'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'year_price_change': self._calculate_price_change(hist)
            }

            system_prompt = """You are an expert stock market analyst. Your role is to:
1. Analyze stock price movements and patterns
2. Evaluate technical indicators
3. Identify key price levels and trends
4. Assess trading volumes and market activity
5. Provide data-driven market insights

Format your response as a structured analysis with clear sections and specific data points."""

            # Construct the analysis prompt
            analysis_prompt = f"""Analyze the stock data for {symbol}:

Current Data:
- Price: ${data_context['current_price']}
- Volume: {data_context['volume']}
- Market Cap: ${data_context['market_cap']}
- P/E Ratio: {data_context['pe_ratio']}
- 52-Week High: ${data_context['fifty_two_week_high']}
- 52-Week Low: ${data_context['fifty_two_week_low']}
- Year Price Change: {data_context['year_price_change']}%

Please provide:
1. Technical Analysis
   - Price Trend Analysis
   - Volume Analysis
   - Key Support/Resistance Levels
2. Market Statistics
   - Trading Range Analysis
   - Volatility Assessment
   - Volume Profile
3. Key Levels
   - Critical Price Points
   - Breakout/Breakdown Levels
   - Risk Management Levels
4. Market Context
   - Relative Strength
   - Market Conditions
   - Trading Activity Assessment

Additional Context:
{context if context else 'No additional context provided'}"""

            # Get Claude's analysis
            response = await self._call_claude(analysis_prompt, system_prompt)

            # Process and structure the response
            return {
                'stock_data': response,
                'raw_data': data_context,
                'source': 'claude-3-haiku',
                'analysis_type': 'comprehensive_stock_data',
                'timestamp': context.get('timestamp') if context else None
            }

        except Exception as e:
            return {
                'error': f"Failed to analyze stock data: {str(e)}",
                'source': 'claude-3-haiku',
                'analysis_type': 'stock_data'
            }

    def _extract_symbol(self, request: str) -> Optional[str]:
        """Extract stock symbol from request"""
        # Basic implementation - could be enhanced with Claude's help
        words = request.upper().split()
        for word in words:
            if word.isalpha() and len(word) <= 5:  # Most stock symbols are 1-5 letters
                return word
        return None

    def _calculate_price_change(self, hist: pd.DataFrame) -> float:
        """Calculate year-to-date price change percentage"""
        if hist.empty:
            return 0.0
        
        first_price = hist['Close'].iloc[0]
        last_price = hist['Close'].iloc[-1]
        
        return round(((last_price - first_price) / first_price) * 100, 2)
