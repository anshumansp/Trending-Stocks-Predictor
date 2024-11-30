import asyncio
from stock_data_agent import StockDataAgent

async def test_scraper():
    # Initialize the agent
    agent = StockDataAgent()
    
    # Test with a well-known stock
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    for symbol in test_symbols:
        print(f"\nTesting scraper with {symbol}...")
        try:
            result = await agent.process_request(f"Analyze stock data for {symbol}")
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                continue
                
            # Print raw data
            raw_data = result['raw_data']
            print("\nRaw Stock Data:")
            print(f"Current Price: ${raw_data['current_price']}")
            print(f"Volume: {raw_data['volume']}")
            print(f"Market Cap: ${raw_data['market_cap']}")
            print(f"P/E Ratio: {raw_data['pe_ratio']}")
            print(f"52-Week High: ${raw_data['fifty_two_week_high']}")
            print(f"52-Week Low: ${raw_data['fifty_two_week_low']}")
            print(f"Year Price Change: {raw_data['year_price_change']}%")
            
            # Print if analysis was successful
            if 'stock_data' in result:
                print("\nAnalysis successful! Length of analysis:", 
                      len(str(result['stock_data'])))
            
        except Exception as e:
            print(f"Error testing {symbol}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
