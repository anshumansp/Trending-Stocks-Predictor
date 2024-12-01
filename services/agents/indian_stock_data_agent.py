from typing import Dict, Any, Optional, Tuple, List
import yfinance as yf
import pandas as pd
from base_agent import BaseStockAgent
import time
from requests.exceptions import ConnectionError, ReadTimeout
import asyncio
import aiohttp
import json

class IndianStockDataAgent(BaseStockAgent):
    def __init__(self):
        """Initialize the Indian Stock Data Agent"""
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

        # NSE sector indices mapping
        self.sectors = {
            'auto': 'NIFTY AUTO',
            'bank': 'NIFTY BANK',
            'financial_services': 'NIFTY FINANCIAL SERVICES',
            'fmcg': 'NIFTY FMCG',
            'healthcare': 'NIFTY HEALTHCARE',
            'it': 'NIFTY IT',
            'media': 'NIFTY MEDIA',
            'metal': 'NIFTY METAL',
            'pharma': 'NIFTY PHARMA',
            'psu_bank': 'NIFTY PSU BANK',
            'realty': 'NIFTY REALTY',
            'consumer_durables': 'NIFTY CONSUMER DURABLES',
            'oil_gas': 'NIFTY OIL & GAS',
            'infrastructure': 'NIFTY INFRASTRUCTURE',
            'mnc': 'NIFTY MNC'
        }

        # NSE URLs
        self.base_url = "https://www.nseindia.com"
        self.sector_url = f"{self.base_url}/api/equity-stockIndices?index="
        
        # Headers for NSE requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        self.session = None
        self.cookies = {}

    async def _init_session(self):
        """Initialize session with required cookies"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(headers=self.headers)
            
            # Get cookies from main page
            async with self.session.get(self.base_url) as response:
                if response.status == 200:
                    # Store cookies
                    self.cookies = {key: value.value for key, value in response.cookies.items()}
                    
                    # Update headers with cookies
                    cookie_string = '; '.join([f'{key}={value}' for key, value in self.cookies.items()])
                    self.headers['Cookie'] = cookie_string
                    
                    return True
                else:
                    print(f"Failed to initialize session: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"Error initializing session: {str(e)}")
            return False

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

    async def analyze_nifty50(self) -> Dict[str, Any]:
        """Analyze Nifty 50 stocks performance and metrics"""
        try:
            print("\nAnalyzing Nifty 50 stocks...")
            results = []
            errors = []
            
            for symbol in self.nifty_50_symbols:
                try:
                    print(f"Processing {symbol}")
                    # Get stock data with retry logic
                    stock, info, hist = self.get_stock_data_with_retry(symbol)
                    
                    if hist.empty:
                        errors.append(f"{symbol}: No historical data available")
                        continue
                        
                    # Calculate technical indicators
                    indicators = self.calculate_technical_indicators(hist)
                    
                    # Get sector information
                    sector = info.get('sector', 'Unknown')
                    industry = info.get('industry', 'Unknown')
                    
                    # Format market cap in billions
                    market_cap = info.get("marketCap", 0)
                    market_cap_b = f"Rs. {market_cap/1e9:.2f}B" if market_cap else "N/A"
                    
                    stock_data = {
                        "symbol": symbol,
                        "name": info.get("longName", symbol.split('.')[0]),
                        "sector": sector,
                        "industry": industry,
                        "current_price": f"Rs. {indicators['current_price']:.2f}",
                        "market_cap": market_cap_b,
                        "pe_ratio": info.get("forwardPE", info.get("trailingPE", "N/A")),
                        "dividend_yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A",
                        "technical_indicators": {
                            "rsi": round(indicators['rsi'], 2) if not pd.isna(indicators['rsi']) else None,
                            "macd": round(indicators['macd'], 2) if not pd.isna(indicators['macd']) else None,
                            "momentum": round(indicators['momentum'] * 100, 2) if not pd.isna(indicators['momentum']) else None
                        },
                        "performance": {
                            "1m": round(indicators['price_change_1m'] * 100, 2) if not pd.isna(indicators['price_change_1m']) else None,
                            "3m": round(indicators['price_change_3m'] * 100, 2) if not pd.isna(indicators['price_change_3m']) else None,
                            "1y": round(indicators['price_change_1y'] * 100, 2) if not pd.isna(indicators['price_change_1y']) else None
                        }
                    }
                    results.append(stock_data)
                    
                except Exception as e:
                    errors.append(f"{symbol}: {str(e)}")
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            # Group stocks by sector
            sector_groups = {}
            for stock in results:
                sector = stock['sector']
                if sector not in sector_groups:
                    sector_groups[sector] = []
                sector_groups[sector].append(stock)
            
            # Calculate sector performance
            sector_performance = []
            for sector, stocks in sector_groups.items():
                if stocks:  # Only process if there are stocks in the sector
                    monthly_returns = [s['performance']['1m'] for s in stocks if s['performance']['1m'] is not None]
                    quarterly_returns = [s['performance']['3m'] for s in stocks if s['performance']['3m'] is not None]
                    
                    avg_1m = sum(monthly_returns) / len(monthly_returns) if monthly_returns else 0
                    avg_3m = sum(quarterly_returns) / len(quarterly_returns) if quarterly_returns else 0
                    
                    sector_performance.append({
                        'sector': sector,
                        'stock_count': len(stocks),
                        'avg_1m_return': round(avg_1m, 2),
                        'avg_3m_return': round(avg_3m, 2)
                    })
            
            return {
                'stocks': results,
                'sector_performance': sorted(sector_performance, key=lambda x: x['avg_1m_return'], reverse=True),
                'errors': errors if errors else None
            }
            
        except Exception as e:
            return {'error': f'Error analyzing Nifty 50: {str(e)}'}

    async def analyze_sector(self, sector_name: str) -> Dict[str, Any]:
        """Analyze a sector's performance using constituent stocks"""
        try:
            # Map sector name to its constituent stocks
            sector_stocks = {
                'auto': ["TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS"],
                'bank': ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "SBIN.NS", "KOTAKBANK.NS"],
                'financial_services': ["BAJFINANCE.NS", "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS"],
                'it': ["TCS.NS", "INFY.NS", "HCLTECH.NS", "TECHM.NS", "WIPRO.NS"],
                'metal': ["HINDALCO.NS", "JSWSTEEL.NS", "TATASTEEL.NS"],
                'oil_gas': ["RELIANCE.NS", "BPCL.NS", "IOC.NS", "ONGC.NS"],
                'pharma': ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
                'consumer': ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "TITAN.NS", "TATACONSUM.NS"]
            }
            
            if sector_name not in sector_stocks:
                return {'error': f'Sector {sector_name} not found or not supported'}
            
            stocks = sector_stocks[sector_name]
            results = []
            errors = []
            
            for symbol in stocks:
                try:
                    # Get stock data with retry logic
                    stock, info, hist = self.get_stock_data_with_retry(symbol)
                    
                    if not hist.empty:
                        # Calculate technical indicators
                        indicators = self.calculate_technical_indicators(hist)
                        
                        # Handle potential None values in performance metrics
                        monthly_return = indicators.get('price_change_1m', None)
                        quarterly_return = indicators.get('price_change_3m', None)
                        
                        stock_data = {
                            "symbol": symbol,
                            "name": info.get("longName", symbol.split('.')[0]),
                            "current_price": f"Rs. {indicators.get('current_price', 0):.2f}",
                            "change_percent": info.get("regularMarketChangePercent", 0),
                            "market_cap": f"Rs. {info.get('marketCap', 0)/1e9:.2f}B",
                            "performance": {
                                "1m": round(monthly_return * 100, 2) if monthly_return is not None else 0,
                                "3m": round(quarterly_return * 100, 2) if quarterly_return is not None else 0
                            }
                        }
                        results.append(stock_data)
                    else:
                        errors.append(f"No data available for {symbol}")
                    
                except Exception as e:
                    errors.append(f"Error processing {symbol}: {str(e)}")
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            if not results:
                return {'error': f'No data available for sector {sector_name}. Errors: {", ".join(errors)}'}
            
            # Calculate sector metrics with error handling
            monthly_returns = [s['performance']['1m'] for s in results]
            quarterly_returns = [s['performance']['3m'] for s in results]
            
            # Filter out zero values for average calculations
            valid_monthly = [r for r in monthly_returns if r != 0]
            valid_quarterly = [r for r in quarterly_returns if r != 0]
            
            sector_data = {
                'name': sector_name,
                'stocks': results,
                'performance': {
                    'avg_1m_return': round(sum(valid_monthly) / len(valid_monthly), 2) if valid_monthly else 0,
                    'avg_3m_return': round(sum(valid_quarterly) / len(valid_quarterly), 2) if valid_quarterly else 0,
                    'stock_count': len(results)
                }
            }
            
            if errors:
                sector_data['errors'] = errors
                
            return sector_data
            
        except Exception as e:
            return {'error': f'Error analyzing sector {sector_name}: {str(e)}'}

    async def get_top_sectors(self) -> dict:
        """Get top sectors based on momentum"""
        all_sectors = []
        errors = []
        
        print("\nAnalyzing sector performance...")
        total_sectors = len(self.sectors)
        
        for idx, (sector_name, _) in enumerate(self.sectors.items(), 1):
            print(f"Processing {sector_name} ({idx}/{total_sectors})")
            try:
                analysis = await self.analyze_sector(sector_name)
                if 'error' in analysis:
                    errors.append(f"{sector_name}: {analysis['error']}")
                else:
                    # Only add sectors with valid performance data
                    if analysis['performance']['avg_1m_return'] != 0 or analysis['performance']['avg_3m_return'] != 0:
                        all_sectors.append(analysis)
            except Exception as e:
                errors.append(f"{sector_name}: {str(e)}")
            
            # Rate limiting
            await asyncio.sleep(1)
            
        if not all_sectors:
            error_msg = "\n".join(errors)
            return {'error': f'No sector data available. Errors encountered:\n{error_msg}'}
            
        # Sort sectors by different timeframes with error handling
        try:
            # Helper function to safely get performance values
            def safe_get_performance(sector, metric):
                try:
                    return sector.get('performance', {}).get(metric, 0) or 0
                except:
                    return 0

            weekly = sorted(all_sectors, 
                          key=lambda x: safe_get_performance(x, 'avg_1m_return'), 
                          reverse=True)[:5]
            monthly = sorted(all_sectors, 
                           key=lambda x: safe_get_performance(x, 'avg_1m_return'), 
                           reverse=True)[:5]
            quarterly = sorted(all_sectors, 
                             key=lambda x: safe_get_performance(x, 'avg_3m_return'), 
                             reverse=True)[:5]
            yearly = sorted(all_sectors, 
                          key=lambda x: safe_get_performance(x, 'avg_3m_return'), 
                          reverse=True)[:5]
            
            return {
                'weekly': weekly,
                'monthly': monthly,
                'quarterly': quarterly,
                'yearly': yearly,
                'errors': errors if errors else None
            }
        except Exception as e:
            return {'error': f'Error sorting sector data: {str(e)}'}

    async def calculate_momentum_score(self, symbol: str) -> dict:
        """Calculate momentum score for a given symbol"""
        try:
            # Get historical data for different timeframes
            data = yf.download(symbol, period="1y", interval="1d")
            if data.empty:
                return {'error': f'No data available for {symbol}'}

            # Calculate returns for different timeframes
            current_price = data['Close'][-1]
            weekly_price = data['Close'][-5] if len(data) >= 5 else data['Close'][0]
            monthly_price = data['Close'][-21] if len(data) >= 21 else data['Close'][0]
            quarterly_price = data['Close'][-63] if len(data) >= 63 else data['Close'][0]
            yearly_price = data['Close'][0]

            performance = {
                'weekly': ((current_price / weekly_price) - 1) * 100,
                'monthly': ((current_price / monthly_price) - 1) * 100,
                'quarterly': ((current_price / quarterly_price) - 1) * 100,
                'yearly': ((current_price / yearly_price) - 1) * 100
            }

            # Calculate momentum score
            momentum_score = (
                performance['weekly'] * 0.3 +
                performance['monthly'] * 0.3 +
                performance['quarterly'] * 0.2 +
                performance['yearly'] * 0.2
            )

            return {
                'symbol': symbol,
                'performance': performance,
                'momentum_score': momentum_score,
                'current_price': current_price
            }

        except Exception as e:
            return {'error': f'Error calculating momentum score: {str(e)}'}

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
            for sector_name in self.sectors.keys():
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
                market_cap = f"Rs. {market_cap/1e9:.2f}B"
            
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol.split('.')[0]),
                "current_price": f"Rs. {current_price:.2f}" if current_price != "N/A" else "N/A",
                "change_percent": info.get("regularMarketChangePercent", 0),
                "volume": format(info.get("regularMarketVolume", 0), ','),
                "market_cap": market_cap,
                "pe_ratio": info.get("forwardPE", info.get("trailingPE", "N/A")),
                "52_week_high": f"Rs. {info.get('fiftyTwoWeekHigh', 'N/A')}",
                "52_week_low": f"Rs. {info.get('fiftyTwoWeekLow', 'N/A')}",
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
        
    async def calculate_momentum_score(self, symbol: str) -> dict:
        """Calculate momentum score for a given symbol"""
        try:
            # Get historical data for different timeframes
            data = yf.download(symbol, period="1y", interval="1d")
            if data.empty:
                return {'error': f'No data available for {symbol}'}

            # Calculate returns for different timeframes
            current_price = data['Close'][-1]
            weekly_price = data['Close'][-5] if len(data) >= 5 else data['Close'][0]
            monthly_price = data['Close'][-21] if len(data) >= 21 else data['Close'][0]
            quarterly_price = data['Close'][-63] if len(data) >= 63 else data['Close'][0]
            yearly_price = data['Close'][0]

            performance = {
                'weekly': ((current_price / weekly_price) - 1) * 100,
                'monthly': ((current_price / monthly_price) - 1) * 100,
                'quarterly': ((current_price / quarterly_price) - 1) * 100,
                'yearly': ((current_price / yearly_price) - 1) * 100
            }

            # Calculate momentum score
            momentum_score = (
                performance['weekly'] * 0.3 +
                performance['monthly'] * 0.3 +
                performance['quarterly'] * 0.2 +
                performance['yearly'] * 0.2
            )

            return {
                'symbol': symbol,
                'performance': performance,
                'momentum_score': momentum_score,
                'current_price': current_price
            }

        except Exception as e:
            return {'error': f'Error calculating momentum score: {str(e)}'}

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

if __name__ == "__main__":
    # Example usage
    agent = IndianStockDataAgent()
    
    # Fetch all Nifty 50 data
    print("Fetching Nifty 50 data...")
    asyncio.run(agent.process_request("Analyze NIFTY50"))