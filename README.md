# Indian Stock Market AI Analyzer 🚀

A comprehensive AI-powered system for analyzing Indian stock market data, providing advanced technical analysis, sector performance tracking, and market insights.

## 🌟 Features

### Stock Data Analysis
- Real-time stock data retrieval from NSE and BSE
- Complete coverage of Nifty 50 stocks
- Accurate price and volume tracking
- Comprehensive stock metrics (P/E ratio, market cap, dividend yield)

### Technical Indicators
- Moving Averages (20, 50, 200 day)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Volume Trend Analysis
- Custom Momentum Scoring

### Sector Analysis
- Coverage of 40+ sector indices
- Major sector indices (Auto, Bank, IT, Pharma, etc.)
- Thematic indices (ESG, Digital, Defence, etc.)
- Multi-timeframe performance tracking
- Momentum-based sector rankings

### Performance Analysis
- Weekly momentum tracking
- Monthly trend analysis
- Quarterly performance metrics
- Yearly performance evaluation

### Reporting
- Detailed Excel reports
- Technical analysis summaries
- Sector performance rankings
- Top gainers and losers
- Market momentum indicators

## 📊 Supported Indices

### Major Sector Indices
- Nifty Auto Index
- Nifty Bank Index
- Nifty Financial Services Index
- Nifty FMCG Index
- Nifty Healthcare Index
- Nifty IT Index
- Nifty Media Index
- Nifty Metal Index
- Nifty Pharma Index
- Nifty Private Bank Index
- Nifty PSU Bank Index
- Nifty Realty Index
- Nifty Consumer Durables Index
- Nifty Oil and Gas Index

### Thematic Indices
- Nifty Commodities Index
- Nifty CPSE Index
- Nifty EV & New Age Automotive Index
- Nifty Energy Index
- Nifty India Consumption Index
- Nifty India Defence
- Nifty India Digital
- Nifty India Manufacturing Index
- Nifty Infrastructure Index
- And many more...

## 🛠️ Technical Architecture

### Components
- `indian_stock_data_agent.py`: Core analysis engine
- `test_indian_stocks.py`: Testing and reporting framework
- `base_agent.py`: Base agent functionality

### Dependencies
```
yfinance==0.2.36
pandas==2.1.0
xlsxwriter==3.1.9
python-dotenv==1.0.0
requests==2.31.0
```

## 🤖 Multi-Agent Orchestration System

Our system employs a sophisticated multi-agent orchestration architecture to provide comprehensive stock market analysis. The orchestrator intelligently coordinates between specialized agents, each focusing on different aspects of market analysis.

### 🎭 Agent Roles

1. **Market Data Agent** (`indian_stock_data_agent.py`)
   - Real-time stock price monitoring
   - Technical indicator calculations
   - Sector performance tracking
   - Historical data analysis

2. **Sentiment Analysis Agent** (`sentiment_analyzer_agent.py`)
   - News sentiment processing
   - Social media trend analysis
   - Market sentiment scoring
   - Real-time sentiment alerts

3. **Fundamental Analysis Agent** (`fundamental_analysis_agent.py`)
   - Company financial metrics
   - Balance sheet analysis
   - Profit & Loss evaluation
   - Cash flow assessment

4. **Prediction Agent** (`prediction_agent.py`)
   - ML-based price predictions
   - Trend forecasting
   - Risk assessment
   - Market pattern recognition

### 🎯 Orchestrator Intelligence

The Multi-Agent Orchestrator (`agent_orchestrator.py`) uses advanced decision-making algorithms to:

1. **Task Distribution**
   ```python
   async def distribute_task(self, request: MarketRequest) -> AgentResponse:
       if request.type == "SENTIMENT":
           return await self.sentiment_agent.process()
       elif request.type == "TECHNICAL":
           return await self.market_data_agent.process()
       # ... other routing logic
   ```

2. **Data Aggregation**
   ```python
   async def aggregate_analysis(self, stock_symbol: str) -> CompleteAnalysis:
       # Parallel processing of different aspects
       technical = await self.market_data_agent.analyze(stock_symbol)
       sentiment = await self.sentiment_agent.analyze(stock_symbol)
       fundamental = await self.fundamental_agent.analyze(stock_symbol)
       
       return self.combine_insights(technical, sentiment, fundamental)
   ```

3. **Priority Management**
   - Real-time market data takes precedence
   - Sentiment analysis runs in parallel
   - Fundamental analysis updates periodically

### 🔄 Workflow Example

1. **User Query Processing**
   ```python
   # User requests complete analysis of RELIANCE
   analysis = await orchestrator.process_request({
       "symbol": "RELIANCE.NS",
       "analysis_type": "COMPLETE",
       "timeframe": "1D"
   })
   ```

2. **Orchestrator Decision Making**
   - Checks request type and urgency
   - Determines required agents
   - Plans execution strategy

3. **Parallel Processing**
   ```python
   async def complete_analysis(self, request: AnalysisRequest):
       tasks = [
           self.market_data_agent.get_technical_analysis(),
           self.sentiment_agent.get_market_sentiment(),
           self.fundamental_agent.get_company_metrics()
       ]
       results = await asyncio.gather(*tasks)
   ```

4. **Result Aggregation**
   - Combines insights from all agents
   - Weighs different factors
   - Generates final recommendation

### 📊 Sample Multi-Agent Output

```json
{
    "symbol": "RELIANCE.NS",
    "timestamp": "2024-01-20T10:30:00Z",
    "technical_analysis": {
        "trend": "BULLISH",
        "support": 2380.5,
        "resistance": 2460.75,
        "indicators": {/* ... */}
    },
    "sentiment_analysis": {
        "overall_score": 0.75,
        "news_sentiment": "POSITIVE",
        "social_sentiment": "NEUTRAL",
        "sentiment_sources": [/* ... */]
    },
    "fundamental_analysis": {
        "pe_ratio": 22.5,
        "book_value": 1234.56,
        "debt_equity": 0.8,
        "metrics": {/* ... */}
    },
    "combined_recommendation": {
        "action": "BUY",
        "confidence": 0.85,
        "time_horizon": "MEDIUM_TERM",
        "risk_level": "MODERATE"
    }
}
```

### 🔐 Agent Communication Security

- Encrypted inter-agent communication
- Rate limiting and request throttling
- Secure credential management
- Access control and authentication

### 📈 Performance Optimization

- Caching frequently requested data
- Load balancing between agents
- Efficient resource allocation
- Request batching and pooling

### 🔄 Scalability

- Horizontal scaling of agents
- Dynamic agent instantiation
- Load-based resource allocation
- Distributed processing support

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/indian-stock-analyzer.git
cd indian-stock-analyzer
```

2. Install dependencies:
```bash
pip install -r services/agents/requirements.txt
```

3. Run the analysis:
```bash
cd services/agents
python test_indian_stocks.py
```

## 📈 Usage Examples

### Analyze Nifty 50 Stocks
```python
from indian_stock_data_agent import IndianStockDataAgent
import asyncio

agent = IndianStockDataAgent()
result = asyncio.run(agent.process_request("Analyze NIFTY50"))
```

### Get Sector Analysis
```python
# Get top performing sectors
sectors = asyncio.run(agent.get_top_sectors())

# Analyze specific sector
bank_analysis = asyncio.run(agent.analyze_sector('bank'))
```

### Technical Analysis
```python
# Get stock with technical indicators
stock_data = agent.get_current_price("RELIANCE.NS")
```

## 📊 Output Format

### Stock Data
```json
{
    "symbol": "RELIANCE.NS",
    "name": "Reliance Industries Limited",
    "current_price": "₹2,450.75",
    "change_percent": 1.25,
    "volume": "2,345,678",
    "market_cap": "₹1,234.56B",
    "pe_ratio": 22.5
}
```

### Sector Analysis
```json
{
    "sector": "bank",
    "momentum_score": 0.85,
    "technical_indicators": {
        "rsi": 65.4,
        "macd": 12.3,
        "sma_20": 42580.5
    }
}
```

## 🔒 Security

- No sensitive credentials in code
- Rate limiting implementation
- Error handling for API failures
- Secure data handling

## 🔄 Updates & Maintenance

The system is actively maintained with:
- Regular data source updates
- New technical indicators
- Additional sector indices
- Performance optimizations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions and feedback, please open an issue in the GitHub repository.
