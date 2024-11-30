const NSEDataParser = require('./csvParser');
const path = require('path');
const { logger } = require('./utils');

async function processStockData(inputFile) {
    try {
        const parser = new NSEDataParser();
        
        // Parse the CSV file
        logger.info('Starting CSV parsing...', { file: inputFile });
        const results = await parser.parseCSVFile(inputFile);

        // Log some statistics
        logger.info('Parsing completed', {
            totalRecords: results.metadata.validRecords,
            processingTime: results.metadata.processingTimeMs + 'ms'
        });

        // Log market summary
        logger.info('Market Summary', {
            advancers: results.summary.marketStats.advancers,
            decliners: results.summary.marketStats.decliners,
            unchanged: results.summary.marketStats.unchanged,
            totalValue: results.summary.marketStats.totalTradedValue.toLocaleString()
        });

        // Export to JSON
        const outputFile = path.join(
            path.dirname(inputFile),
            `processed_${path.basename(inputFile, '.csv')}.json`
        );
        await parser.exportToJSON(results, outputFile);

        // Print top gainers and losers
        console.log('\nTop Gainers:');
        results.summary.topGainers.forEach(stock => {
            console.log(`${stock.symbol}: ${stock.metrics.dayReturn}%`);
        });

        console.log('\nTop Losers:');
        results.summary.topLosers.forEach(stock => {
            console.log(`${stock.symbol}: ${stock.metrics.dayReturn}%`);
        });

        console.log('\nMost Traded:');
        results.summary.mostTraded.forEach(stock => {
            console.log(`${stock.symbol}: ₹${(stock.tradingData.value / 10000000).toFixed(2)} Cr`);
        });

        return results;

    } catch (error) {
        logger.error('Error processing stock data:', { error: error.message });
        throw error;
    }
}

// If running directly, process the file specified in command line
if (require.main === module) {
    const inputFile = process.argv[2];
    if (!inputFile) {
        console.error('Please provide the path to the CSV file');
        process.exit(1);
    }

    processStockData(inputFile)
        .then(() => process.exit(0))
        .catch(() => process.exit(1));
}

module.exports = processStockData;
