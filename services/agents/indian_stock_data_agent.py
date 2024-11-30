from typing import Dict, Any, Optional
import yfinance as yf
import pandas as pd
from base_agent import BaseStockAgent
import time
from requests.exceptions import ConnectionError, ReadTimeout
import asyncio
from typing import Tuple

class IndianStockDataAgent(BaseStockAgent):
    def __init__(self):
        super().__init__(
            name="Indian Stock Data Agent",
            description="Specializes in Indian stock market data from NSE and BSE, including prices, volumes, and technical indicators."
        )
        self.cache = {}
        self.exchange_suffixes = {
            'NSE': '.NS',  # For National Stock Exchange
            'BSE': '.BO'   # For Bombay Stock Exchange
        }
        
        # Nifty 50 symbols
        self.nifty_50_symbols = [
            "ADANIENT.NS",   # Adani Enterprises
            "ADANIPORTS.NS", # Adani Ports & SEZ
            "APOLLOHOSP.NS", # Apollo Hospitals
            "ASIANPAINT.NS", # Asian Paints
            "AXISBANK.NS",   # Axis Bank
            "BAJAJ-AUTO.NS", # Bajaj Auto
            "BAJFINANCE.NS", # Bajaj Finance
            "BAJAJFINSV.NS", # Bajaj Finserv
            "BEL.NS",        # Bharat Electronics
            "BHARTIARTL.NS", # Bharti Airtel
            "BPCL.NS",       # BPCL
            "CIPLA.NS",      # Cipla
            "COALINDIA.NS",  # Coal India
            "DRREDDY.NS",    # Dr. Reddy's Lab
            "EICHERMOT.NS",  # Eicher Motors
            "GRASIM.NS",     # Grasim
            "HCLTECH.NS",    # HCL Technologies
            "HDFCBANK.NS",   # HDFC Bank
            "HDFCLIFE.NS",   # HDFC Life Insurance
            "HEROMOTOCO.NS", # Hero MotoCorp
            "HINDALCO.NS",   # Hindalco
            "HINDUNILVR.NS", # Hindustan Unilever
            "ICICIBANK.NS",  # ICICI Bank
            "INDUSINDBK.NS", # IndusInd Bank
            "INFY.NS",       # Infosys
            "IOC.NS",        # IOC
            "ITC.NS",        # ITC
            "JSWSTEEL.NS",   # JSW Steel
            "KOTAKBANK.NS",  # Kotak Mahindra Bank
            "LT.NS",         # L&T
            "M&M.NS",        # M&M
            "MARUTI.NS",     # Maruti Suzuki
            "NESTLEIND.NS",  # Nestle
            "NTPC.NS",       # NTPC
            "ONGC.NS",       # ONGC
            "POWERGRID.NS",  # Power Grid
            "RELIANCE.NS",   # Reliance Industries
            "SBIN.NS",       # SBI
            "SBILIFE.NS",    # SBI Life Insurance
            "SHRIRAMFIN.NS", # Shriram Finance
            "SUNPHARMA.NS",  # Sun Pharma
            "TATACONSUM.NS", # Tata Consumer
            "TATAMOTORS.NS", # Tata Motors
            "TATASTEEL.NS",  # Tata Steel
            "TCS.NS",        # TCS
            "TECHM.NS",      # Tech Mahindra
            "TITAN.NS",      # Titan
            "TRENT.NS",      # Trent
            "ULTRACEMCO.NS", # UltraTech Cement
            "WIPRO.NS"       # Wipro
        ]

        # Add sector indices
        self.sector_indices = {
            # Major Sector Indices
            'auto': '^CNXAUTO',
            'bank': '^NSEBANK',
            'financial_services': '^CNXFIN',
            'fmcg': '^CNXFMCG',
            'healthcare': '^CNXHEALTH',
            'it': '^CNXIT',
            'media': '^CNXMEDIA',
            'metal': '^CNXMETAL',
            'pharma': '^CNXPHARMA',
            'private_bank': '^NIFTYPRBANK',
            'psu_bank': '^CNXPSUBANK',
            'realty': '^CNXREALTY',
            'consumer_durables': '^CNXCONSUM',
            'oil_gas': '^CNXENERGY',
            
            # Thematic Indices
            'commodities': '^CNXCOMM',
            'cpse': '^CNXCPSE',
            'ev_auto': '^CNXEVAUTO',
            'energy': '^CNXENERGY',
            'consumption': '^CNXCONSUM',
            'defence': '^CNXDEFENCE',
            'digital': '^CNXDIGITAL',
            'manufacturing': '^CNXMANUF',
            'infrastructure': '^CNXINFRA',
            'mnc': '^CNXMNC',
            'pse': '^CNXPSE',
            'services': '^CNXSERV',
            'esg': '^NIFTYESG'
        }
        
    def get_stock_data_with_retry(self, symbol: str, max_retries: int = 3) -> Tuple[yf.Ticker, dict, pd.DataFrame]:
        """Get stock data with retry logic"""
        for attempt in range(max_retries):
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                # Use 1mo period instead of 1y for more reliable data
                hist = stock.history(period="1mo")
                if not hist.empty:
                    return stock, info, hist
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to get data for {symbol} after {max_retries} attempts: {str(e)}")
                time.sleep(1)  # Wait before retry
        
        # Return empty data if all retries fail
        return yf.Ticker(symbol), {}, pd.DataFrame()

    def calculate_technical_indicators(self, hist_data):
        """Calculate technical indicators for analysis"""
        if hist_data.empty:
            return {}
            
        # Calculate basic technical indicators
        hist_data['SMA_20'] = hist_data['Close'].rolling(window=20).mean()
        hist_data['SMA_50'] = hist_data['Close'].rolling(window=50).mean()
        hist_data['SMA_200'] = hist_data['Close'].rolling(window=200).mean()
        
        # RSI
        delta = hist_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist_data['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = hist_data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist_data['Close'].ewm(span=26, adjust=False).mean()
        hist_data['MACD'] = exp1 - exp2
        hist_data['Signal_Line'] = hist_data['MACD'].ewm(span=9, adjust=False).mean()
        
        # Momentum
        hist_data['Momentum'] = hist_data['Close'].pct_change(periods=10)
        
        # Volume trend
        hist_data['Volume_MA'] = hist_data['Volume'].rolling(window=20).mean()
        
        return {
            'current_price': hist_data['Close'].iloc[-1],
            'sma_20': hist_data['SMA_20'].iloc[-1],
            'sma_50': hist_data['SMA_50'].iloc[-1],
            'sma_200': hist_data['SMA_200'].iloc[-1],
            'rsi': hist_data['RSI'].iloc[-1],
            'macd': hist_data['MACD'].iloc[-1],
            'macd_signal': hist_data['Signal_Line'].iloc[-1],
            'momentum': hist_data['Momentum'].iloc[-1],
            'volume_trend': hist_data['Volume'].iloc[-1] / hist_data['Volume_MA'].iloc[-1],
            'price_change_1m': hist_data['Close'].pct_change(periods=20).iloc[-1],
            'price_change_3m': hist_data['Close'].pct_change(periods=60).iloc[-1],
            'price_change_1y': hist_data['Close'].pct_change(periods=252).iloc[-1]
        }

    async def analyze_sector(self, sector_name: str) -> Dict[str, Any]:
        """Analyze a specific sector's performance"""
        try:
            symbol = self.sector_indices.get(sector_name)
            if not symbol:
                return {'error': f'Sector {sector_name} not found'}

            stock = yf.Ticker(symbol)
            
            # Get historical data for different timeframes
            hist_data = {
                'weekly': stock.history(period='5d'),
                'monthly': stock.history(period='1mo'),
                'quarterly': stock.history(period='3mo'),
                'yearly': stock.history(period='1y')
            }
            
            # Calculate performance for each timeframe
            performance = {}
            for timeframe, data in hist_data.items():
                if not data.empty:
                    start_price = data['Close'].iloc[0]
                    end_price = data['Close'].iloc[-1]
                    performance[timeframe] = ((end_price - start_price) / start_price) * 100
                else:
                    performance[timeframe] = float('nan')
            
            # Get current technical indicators
            current_data = hist_data['monthly']  # Use monthly data for indicators
            if not current_data.empty:
                # Calculate technical indicators
                current_data['SMA_20'] = current_data['Close'].rolling(window=20).mean()
                current_data['Volume_MA'] = current_data['Volume'].rolling(window=20).mean()
                
                rsi = self.calculate_rsi(current_data['Close'])
                macd, signal = self.calculate_macd(current_data['Close'])
                
                technical_indicators = {
                    'rsi': rsi.iloc[-1] if not rsi.empty else None,
                    'macd': macd.iloc[-1] if not macd.empty else None,
                    'sma_20': current_data['SMA_20'].iloc[-1] if 'SMA_20' in current_data else None,
                    'volume_trend': current_data['Volume'].iloc[-1] / current_data['Volume_MA'].iloc[-1] if 'Volume_MA' in current_data and current_data['Volume_MA'].iloc[-1] != 0 else 1.0
                }
            else:
                technical_indicators = {
                    'rsi': None,
                    'macd': None,
                    'sma_20': None,
                    'volume_trend': 1.0
                }
            
            # Calculate momentum score
            momentum_score = self.calculate_momentum_score(technical_indicators, performance)
            
            return {
                'sector': sector_name,
                'symbol': symbol,
                'performance': performance,
                'technical_indicators': technical_indicators,
                'momentum_score': momentum_score
            }
            
        except Exception as e:
            print(f"Error analyzing sector {sector_name}: {str(e)}")
            return {
                'sector': sector_name,
                'symbol': self.sector_indices.get(sector_name),
                'performance': {
                    'weekly': float('nan'),
                    'monthly': float('nan'),
                    'quarterly': float('nan'),
                    'yearly': float('nan')
                },
                'technical_indicators': {
                    'rsi': None,
                    'macd': None,
                    'sma_20': None,
                    'volume_trend': 1.0
                },
                'momentum_score': 0
            }

    async def get_top_sectors(self, timeframe: str = "all") -> dict:
        """Get top 5 sectors based on momentum for different timeframes"""
        all_sectors = []
        
        print("\nAnalyzing sector performance...")
        total_sectors = len(self.sector_indices)
        
        for idx, (sector_name, _) in enumerate(self.sector_indices.items(), 1):
            print(f"Processing {sector_name} ({idx}/{total_sectors})")
            analysis = await self.analyze_sector(sector_name)
            if 'error' not in analysis:
                all_sectors.append(analysis)
            time.sleep(0.5)  # Rate limiting
            
        if not all_sectors:
            return {'error': 'No sector data available'}
            
        # Sort sectors by different timeframes
        weekly = sorted(all_sectors, key=lambda x: x['performance']['weekly'], reverse=True)[:5]
        monthly = sorted(all_sectors, key=lambda x: x['performance']['monthly'], reverse=True)[:5]
        quarterly = sorted(all_sectors, key=lambda x: x['performance']['quarterly'], reverse=True)[:5]
        yearly = sorted(all_sectors, key=lambda x: x['performance']['yearly'], reverse=True)[:5]
        
        return {
            'weekly': weekly,
            'monthly': monthly,
            'quarterly': quarterly,
            'yearly': yearly
        }

    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process an Indian stock data request"""
        try:
            # Handle sector analysis requests
            if "ANALYZE SECTORS" in request.upper():
                return await self.get_top_sectors()
                
            # Special handling for market indices
            if "NIFTY50" in request.upper() or "NIFTY 50" in request.upper():
                # Get all Nifty 50 data with progress
                print("Fetching Nifty 50 data...")
                data = []
                for i, symbol in enumerate(self.nifty_50_symbols, 1):
                    print(f"Processing {symbol} ({i}/{len(self.nifty_50_symbols)})")
                    stock_data = self.get_current_price(symbol)
                    if 'error' not in stock_data:
                        data.append(stock_data)
                    time.sleep(0.5)  # Rate limiting
                
                if not data:
                    return {
                        'error': 'Failed to fetch Nifty 50 data',
                        'source': 'yfinance',
                        'analysis_type': 'nifty50_data'
                    }
                
                return {
                    'data': data,
                    'source': 'yfinance',
                    'analysis_type': 'nifty50_data'
                }
                
            # Handle specific sector analysis
            for sector_name in self.sector_indices.keys():
                if sector_name.upper() in request.upper():
                    return await self.analyze_sector(sector_name)
                    
            # Handle individual stock analysis
            symbol, exchange = self._extract_symbol_and_exchange(request)
            if not symbol:
                return {
                    'error': 'No valid Indian stock symbol found in request',
                    'source': 'yfinance',
                    'analysis_type': 'indian_stock_data'
                }

            # Format symbol with exchange suffix
            formatted_symbol = self._format_symbol(symbol, exchange)
        
            # Get detailed stock data
            stock_data = self.get_current_price(formatted_symbol)
            
            if 'error' in stock_data:
                return {
                    'error': stock_data['error'],
                    'source': 'yfinance',
                    'analysis_type': 'indian_stock_data'
                }
            
            return {
                'data': stock_data,
                'source': 'yfinance',
                'analysis_type': 'indian_stock_data'
            }

        except Exception as e:
            return {
                'error': str(e),
                'source': 'yfinance',
                'analysis_type': 'indian_stock_data'
            }
            
    def _extract_symbol_and_exchange(self, request: str) -> tuple[str, str]:
        """Extract stock symbol and exchange from request"""
        words = request.upper().split()
        
        # Default to NSE
        exchange = 'NSE'
        symbol = None
        
        # Look for exchange specification
        if 'NSE' in words:
            exchange = 'NSE'
        elif 'BSE' in words:
            exchange = 'BSE'
            
        # Extract symbol - it's the first word that's not 'ANALYZE' or an exchange
        for word in words:
            if word not in ['ANALYZE', 'NSE', 'BSE']:
                symbol = word
                break
                
        return symbol, exchange

    def _format_symbol(self, symbol: str, exchange: str = 'NSE') -> str:
        """Format symbol with correct exchange suffix"""
        # Remove any existing suffixes
        symbol = symbol.upper().split('.')[0]
        # Add exchange suffix
        return f"{symbol}{self.exchange_suffixes.get(exchange.upper(), '.NS')}"

    def get_current_price(self, symbol: str) -> dict:
        """Fetch accurate current price and key stats of a single stock."""
        try:
            # Get stock data with retry logic
            stock, info, hist = self.get_stock_data_with_retry(symbol)
            
            # Get the most accurate current price
            current_price = (
                info.get('regularMarketPrice') or 
                info.get('currentPrice') or 
                info.get('previousClose') or
                (hist['Close'].iloc[-1] if not hist.empty else None) or
                'N/A'
            )
            
            # Format market cap in billions for readability
            market_cap = info.get("marketCap", "N/A")
            if market_cap != "N/A":
                market_cap = f"₹{market_cap/1e9:.2f}B"
            
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol.split('.')[0]),
                "current_price": f"₹{current_price:.2f}" if current_price != "N/A" else "N/A",
                "change_percent": info.get("regularMarketChangePercent", 0),
                "volume": format(info.get("regularMarketVolume", 0), ','),
                "market_cap": market_cap,
                "pe_ratio": info.get("forwardPE", info.get("trailingPE", "N/A")),
                "52_week_high": f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}",
                "52_week_low": f"₹{info.get('fiftyTwoWeekLow', 'N/A')}",
                "avg_volume": format(info.get("averageVolume", 0), ','),
                "dividend_yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A"
            }
        except Exception as e:
            return {"symbol": symbol, "error": str(e)}

    def calculate_rsi(self, prices: pd.Series, periods: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.copy()
        losses = delta.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=periods).mean()
        avg_losses = losses.rolling(window=periods).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD and Signal line"""
        # Calculate EMAs
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        
        # Calculate MACD line
        macd = exp1 - exp2
        
        # Calculate Signal line
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        
        return macd, signal_line
        
    def calculate_momentum_score(self, technical_indicators: Dict[str, float], performance: Dict[str, float]) -> float:
        """Calculate momentum score based on technical indicators and performance"""
        try:
            score = 0.0
            
            # RSI component (30%)
            if technical_indicators['rsi'] is not None:
                rsi = technical_indicators['rsi']
                if rsi > 70:
                    score += 0.3  # Overbought
                elif rsi < 30:
                    score += 0.1  # Oversold
                else:
                    score += 0.2  # Neutral
                    
            # MACD component (15%)
            if technical_indicators['macd'] is not None:
                if technical_indicators['macd'] > 0:
                    score += 0.15
                    
            # SMA trend component (20%)
            if technical_indicators['sma_20'] is not None:
                if technical_indicators['sma_20'] > 0:
                    score += 0.2
                    
            # Volume trend component (15%)
            volume_trend = technical_indicators['volume_trend']
            if volume_trend > 1.1:  # Volume increasing
                score += 0.15
            elif volume_trend > 0.9:  # Volume stable
                score += 0.1
                
            # Performance component (20%)
            if not pd.isna(performance['monthly']):
                monthly_perf = performance['monthly']
                if monthly_perf > 5:
                    score += 0.2
                elif monthly_perf > 0:
                    score += 0.1
                    
            return score
            
        except Exception as e:
            print(f"Error calculating momentum score: {str(e)}")
            return 0.0

if __name__ == "__main__":
    # Example usage
    agent = IndianStockDataAgent()
    
    # Fetch all Nifty 50 data
    print("Fetching Nifty 50 data...")
    asyncio.run(agent.process_request("Analyze NIFTY50"))