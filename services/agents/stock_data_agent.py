from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate
from typing import List, Dict, Any
import json
import aiohttp
from base_agent import BaseAgent
from config import STOCK_DATA_CONFIG

class StockDataPromptTemplate(StringPromptTemplate):
    template = """You are a Stock Data Agent responsible for fetching and analyzing stock market data.
Your goal is to gather accurate market data and provide initial analysis.

You have access to the following tools:
{tools}

Current conversation:
{chat_history}

New input: {input}

Think through this step-by-step:
1) What specific data do you need to fetch?
2) How will you analyze this data?
3) What format should the output be in?

Action: """

    def format(self, **kwargs) -> str:
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in kwargs["tools"]])
        return self.template.format(**kwargs)

class StockDataAgent(BaseAgent):
    def __init__(self):
        super().__init__("StockDataAgent")
        self.cache = {}

    def _get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="fetch_stock_data",
                func=self._fetch_stock_data,
                description="Fetch current stock data including price, volume, and basic metrics"
            ),
            Tool(
                name="analyze_technical_indicators",
                func=self._analyze_technical_indicators,
                description="Calculate technical indicators like RSI, MACD, and moving averages"
            ),
            Tool(
                name="get_historical_data",
                func=self._get_historical_data,
                description="Fetch historical stock data for trend analysis"
            )
        ]

    def _create_prompt(self) -> StringPromptTemplate:
        return StockDataPromptTemplate()

    async def _fetch_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch current stock data from NSE"""
        try:
            # Check cache first
            if symbol in self.cache:
                return self.cache[symbol]

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{STOCK_DATA_CONFIG['nse_url']}/api/quote-equity?symbol={symbol}") as response:
                    data = await response.json()
                    
                    processed_data = {
                        'symbol': symbol,
                        'price': data['lastPrice'],
                        'change': data['change'],
                        'volume': data['totalTradedVolume'],
                        'high': data['dayHigh'],
                        'low': data['dayLow'],
                        'timestamp': data['lastUpdateTime']
                    }

                    # Cache the result
                    self.cache[symbol] = processed_data
                    return processed_data

        except Exception as e:
            return {'error': f"Failed to fetch stock data: {str(e)}"}

    async def _analyze_technical_indicators(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate technical indicators for the stock"""
        try:
            # Implementation of technical analysis
            # This would use the analysis module we created earlier
            return {
                'symbol': data['symbol'],
                'indicators': {
                    'rsi': 0,  # Calculate RSI
                    'macd': {  # Calculate MACD
                        'value': 0,
                        'signal': 0,
                        'histogram': 0
                    },
                    'sma': {  # Calculate SMAs
                        '20': 0,
                        '50': 0,
                        '200': 0
                    }
                }
            }
        except Exception as e:
            return {'error': f"Failed to calculate indicators: {str(e)}"}

    async def _get_historical_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch historical data for the stock"""
        try:
            symbol = params['symbol']
            days = params.get('days', 30)

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{STOCK_DATA_CONFIG['nse_url']}/api/historical?symbol={symbol}&days={days}"
                ) as response:
                    data = await response.json()
                    return {
                        'symbol': symbol,
                        'historical_data': data
                    }
        except Exception as e:
            return {'error': f"Failed to fetch historical data: {str(e)}"}

    async def handle_callback(self, message: Dict[str, Any]) -> None:
        """Handle messages from other agents"""
        if message.get('type') == 'data_request':
            result = await self.process(message['data'])
            # Implement callback mechanism to respond to the requesting agent
            pass
