const fs = require('fs');
const csv = require('csv-parser');
const { logger } = require('./utils');

class StockDataProcessor {
    constructor(filePath) {
        this.filePath = filePath;
        this.data = [];
    }

    async processFile() {
        return new Promise((resolve, reject) => {
            fs.createReadStream(this.filePath)
                .pipe(csv())
                .on('data', (row) => {
                    // Process each row of the CSV
                    const processedRow = {
                        symbol: row.SYMBOL,
                        series: row.SERIES,
                        open: parseFloat(row.OPEN),
                        high: parseFloat(row.HIGH),
                        low: parseFloat(row.LOW),
                        close: parseFloat(row.CLOSE),
                        volume: parseInt(row.TOTTRDQTY),
                        value: parseFloat(row.TOTTRDVAL),
                        timestamp: row.TIMESTAMP
                    };
                    this.data.push(processedRow);
                })
                .on('end', () => {
                    logger.info(`Processed ${this.data.length} stock entries`);
                    resolve(this.data);
                })
                .on('error', (error) => {
                    logger.error('Error processing CSV file:', { error: error.message });
                    reject(error);
                });
        });
    }

    calculateMetrics() {
        const metrics = {};
        
        for (const stock of this.data) {
            metrics[stock.symbol] = {
                dayReturn: ((stock.close - stock.open) / stock.open) * 100,
                volatility: ((stock.high - stock.low) / stock.low) * 100,
                volumeWeightedPrice: stock.value / stock.volume
            };
        }

        return metrics;
    }

    getTopMovers(limit = 10) {
        const metrics = this.calculateMetrics();
        
        // Sort stocks by absolute percentage change
        const sortedStocks = Object.entries(metrics)
            .sort((a, b) => Math.abs(b[1].dayReturn) - Math.abs(a[1].dayReturn))
            .slice(0, limit);

        return {
            topGainers: sortedStocks.filter(([, metrics]) => metrics.dayReturn > 0),
            topLosers: sortedStocks.filter(([, metrics]) => metrics.dayReturn < 0)
        };
    }
}

module.exports = StockDataProcessor;

// Example usage if run directly
if (require.main === module) {
    const processor = new StockDataProcessor('./data/latest.csv');
    processor.processFile()
        .then(() => {
            const topMovers = processor.getTopMovers();
            console.log('Top Movers:', topMovers);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
