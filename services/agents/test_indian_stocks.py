import asyncio
from indian_stock_data_agent import IndianStockDataAgent

async def main():
    """Main function to test Indian stock data agent"""
    print("\n=== Starting Indian Stock Market Analysis ===")
    
    async with IndianStockDataAgent() as agent:
        # Test sector analysis
        print("\n=== Starting Sector Analysis ===")
        sector_data = await agent.get_top_sectors()
        
        if 'error' in sector_data:
            print(f"Warning: {sector_data['error']}")
        else:
            print("\nTop Sectors by Timeframe:")
            
            print("\nMonthly Top Performers:")
            for sector in sector_data['weekly'][:3]:
                print(f"  * {sector['name']}: {sector['performance']['avg_1m_return']:.1f}%")
                
            print("\nQuarterly Top Performers:")
            for sector in sector_data['quarterly'][:3]:
                print(f"  * {sector['name']}: {sector['performance']['avg_3m_return']:.1f}%")
        
        # Test individual sector analysis
        print("\n=== Testing Individual Sector Analysis ===")
        sectors_to_test = ['bank', 'it', 'auto']
        for sector in sectors_to_test:
            print(f"\nAnalyzing {sector.upper()} sector...")
            sector_analysis = await agent.analyze_sector(sector)
            if 'error' in sector_analysis:
                print(f"Error: {sector_analysis['error']}")
            else:
                print(f"Sector: {sector_analysis['name']}")
                print(f"Number of stocks: {sector_analysis['performance']['stock_count']}")
                print(f"1-Month Return: {sector_analysis['performance']['avg_1m_return']:.1f}%")
                print(f"3-Month Return: {sector_analysis['performance']['avg_3m_return']:.1f}%")
                print("\nTop Performing Stocks:")
                sorted_stocks = sorted(sector_analysis['stocks'], 
                                    key=lambda x: x['performance']['1m'] if x['performance']['1m'] is not None else float('-inf'), 
                                    reverse=True)
                for stock in sorted_stocks[:3]:
                    print(f"  * {stock['name']}: {stock['performance']['1m']:.1f}% (1M)")
        
        # Test Nifty 50 analysis
        print("\n=== Analyzing Nifty 50 stocks ===")
        nifty_data = await agent.analyze_nifty50()
        
        if 'error' in nifty_data:
            print(f"Error: {nifty_data['error']}")
        else:
            # Print sector performance
            print("\nSector Performance:")
            for sector in nifty_data['sector_performance'][:5]:
                print(f"  * {sector['sector']}: {sector['avg_1m_return']:.1f}% (1M), {sector['avg_3m_return']:.1f}% (3M)")
            
            # Print top performing stocks
            print("\nTop Performing Stocks (1M):")
            sorted_stocks = sorted(nifty_data['stocks'], 
                                key=lambda x: x['performance']['1m'] if x['performance']['1m'] is not None else float('-inf'), 
                                reverse=True)
            for stock in sorted_stocks[:5]:
                print(f"  * {stock['name']} ({stock['sector']})")
                print(f"    - 1M Return: {stock['performance']['1m']:.1f}%")
                print(f"    - Current Price: {stock['current_price']}")
                print(f"    - Market Cap: {stock['market_cap']}")
            
            # Print any errors
            if nifty_data['errors']:
                print("\nErrors encountered:")
                for error in nifty_data['errors']:
                    print(f"  * {error}")

if __name__ == "__main__":
    asyncio.run(main())
