const StockRankingSystem = require('./stockRanking');
const NSEDataParser = require('./csvParser');
const { logger } = require('./utils');

async function generateStockRecommendations(csvFilePath) {
    try {
        // Parse stock data
        const parser = new NSEDataParser();
        const stockData = await parser.parseCSVFile(csvFilePath);

        // Configure ranking system
        const rankingSystem = new StockRankingSystem({
            weights: {
                technical: 0.4,
                fundamental: 0.3,
                sentiment: 0.3
            },
            thresholds: {
                minVolume: 100000,
                minPrice: 10,
                maxVolatility: 50
            }
        });

        // Get top recommendations
        const recommendations = rankingSystem.getTopRecommendations(stockData.data);

        // Print recommendations
        console.log('\nTop Stock Recommendations:');
        console.log('=========================\n');

        recommendations.forEach((stock, index) => {
            console.log(`${index + 1}. ${stock.symbol}`);
            console.log(`   Price: ₹${stock.priceData.close.toFixed(2)}`);
            console.log(`   Day Return: ${stock.metrics.dayReturn.toFixed(2)}%`);
            console.log(`   Recommendation: ${stock.recommendation.strength}`);
            console.log(`   Confidence: ${stock.recommendation.confidence.toFixed(1)}%`);
            console.log('   Reasons:');
            stock.recommendation.reasons.forEach(reason => {
                console.log(`     - ${reason}`);
            });
            console.log('   Scores:');
            console.log(`     - Technical: ${(stock.rankings.technicalScore * 100).toFixed(1)}%`);
            console.log(`     - Fundamental: ${(stock.rankings.fundamentalScore * 100).toFixed(1)}%`);
            console.log(`     - Sentiment: ${(stock.rankings.sentimentScore * 100).toFixed(1)}%`);
            console.log();
        });

        // Generate summary statistics
        const summary = {
            totalStocks: stockData.data.length,
            filteredStocks: recommendations.length,
            averageConfidence: recommendations.reduce((sum, stock) => 
                sum + stock.recommendation.confidence, 0) / recommendations.length,
            recommendationBreakdown: recommendations.reduce((acc, stock) => {
                acc[stock.recommendation.strength] = (acc[stock.recommendation.strength] || 0) + 1;
                return acc;
            }, {})
        };

        console.log('Summary Statistics:');
        console.log('==================');
        console.log(`Total Stocks Analyzed: ${summary.totalStocks}`);
        console.log(`Stocks Meeting Criteria: ${summary.filteredStocks}`);
        console.log(`Average Confidence: ${summary.averageConfidence.toFixed(1)}%`);
        console.log('\nRecommendation Breakdown:');
        Object.entries(summary.recommendationBreakdown).forEach(([strength, count]) => {
            console.log(`${strength}: ${count} stocks`);
        });

        return {
            recommendations,
            summary
        };

    } catch (error) {
        logger.error('Error generating stock recommendations:', { error: error.message });
        throw error;
    }
}

// Run if called directly
if (require.main === module) {
    const csvFile = process.argv[2];
    if (!csvFile) {
        console.error('Please provide the path to the CSV file');
        process.exit(1);
    }

    generateStockRecommendations(csvFile)
        .then(() => process.exit(0))
        .catch(() => process.exit(1));
}

module.exports = generateStockRecommendations;
