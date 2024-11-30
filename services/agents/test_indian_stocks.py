import asyncio
import pandas as pd
from datetime import datetime
from indian_stock_data_agent import IndianStockDataAgent

async def analyze_sectors(agent):
    """Analyze all sectors and generate report"""
    print("\n=== Starting Sector Analysis ===")
    
    try:
        # Get sector analysis
        print("\nAnalyzing sector performance...")
        sector_data = await agent.get_top_sectors()
        
        if 'error' in sector_data:
            print(f"Warning: {sector_data['error']}")
            return
            
        # Create Excel report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Indian_Market_Analysis_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Create summary sheet
            summary_data = []
            for timeframe in ['weekly', 'monthly', 'quarterly', 'yearly']:
                sectors = sector_data[timeframe]
                for sector in sectors:
                    summary_data.append({
                        'Timeframe': timeframe.capitalize(),
                        'Sector': sector['sector'],
                        'Performance': sector['performance'][timeframe],
                        'Momentum Score': sector['momentum_score']
                    })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Format the summary sheet
            workbook = writer.book
            worksheet = writer.sheets['Summary']
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#D9EAD3',
                'border': 1
            })
            
            # Apply formats
            for col_num, value in enumerate(summary_df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Adjust column widths
            worksheet.set_column('A:A', 12)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 15)
            
        print(f"\nSector analysis saved to {filename}")
        
        # Display top sectors for each timeframe
        print("\nTop Sectors by Timeframe:\n")
        for timeframe in ['weekly', 'monthly', 'quarterly', 'yearly']:
            print(f"{timeframe.capitalize()}:")
            top_sectors = sector_data[timeframe][:3]
            for sector in top_sectors:
                perf = sector['performance'][timeframe]
                print(f"  * {sector['sector'].capitalize()}: {perf:.1f}%")
            print()
            
    except Exception as e:
        print(f"Error in sector analysis: {str(e)}")

async def test_indian_stocks():
    """Test the Indian stock data agent"""
    print("=== Starting Indian Stock Market Analysis ===")
    print("=== Starting Indian Stock Market Analysis ===")
    
    agent = IndianStockDataAgent()
    
    # Analyze sectors
    await analyze_sectors(agent)
    
    # Analyze Nifty 50 stocks
    print("\n=== Analyzing Nifty 50 stocks ===")
    try:
        nifty_data = await agent.process_request("Analyze NIFTY50")
        if 'error' in nifty_data:
            print(f"Warning: {nifty_data['error']}")
        elif 'data' in nifty_data:
            # Sort stocks by performance
            stocks = nifty_data['data']
            stocks.sort(key=lambda x: float(str(x.get('change_percent', '0')).replace('%', '')), reverse=True)
            
            # Display top gainers and losers
            print("\nTop Gainers:")
            for stock in stocks[:5]:
                print(f"  * {stock['symbol']}: {stock.get('change_percent', 'N/A')}%")
                
            print("\nTop Losers:")
            for stock in stocks[-5:]:
                print(f"  * {stock['symbol']}: {stock.get('change_percent', 'N/A')}%")
        else:
            print("Warning: Unexpected response format from Nifty 50 analysis")
            
    except Exception as e:
        print(f"Error analyzing Nifty 50: {str(e)}")

if __name__ == "__main__":
    print("=== Starting Indian Stock Market Analysis ===")
    asyncio.run(test_indian_stocks())
