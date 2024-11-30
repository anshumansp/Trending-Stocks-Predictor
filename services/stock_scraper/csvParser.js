const fs = require('fs').promises;
const csv = require('csv-parser');
const { createReadStream } = require('fs');
const { Transform } = require('stream');
const path = require('path');
const { logger } = require('./utils');

class NSEDataParser {
    constructor() {
        this.requiredFields = [
            'SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE',
            'TOTTRDQTY', 'TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES'
        ];
    }

    /**
     * Validates and transforms raw CSV data
     * @param {Object} row Raw CSV row
     * @returns {Object|null} Transformed data or null if invalid
     */
    transformRow(row) {
        try {
            // Check if all required fields are present
            if (!this.requiredFields.every(field => field in row)) {
                logger.warn('Missing required fields in row:', row);
                return null;
            }

            // Parse numeric values and validate
            const numericFields = {
                open: parseFloat(row.OPEN),
                high: parseFloat(row.HIGH),
                low: parseFloat(row.LOW),
                close: parseFloat(row.CLOSE),
                last: parseFloat(row.LAST),
                previousClose: parseFloat(row.PREVCLOSE),
                volume: parseInt(row.TOTTRDQTY, 10),
                value: parseFloat(row.TOTTRDVAL),
                trades: parseInt(row.TOTALTRADES, 10)
            };

            // Validate numeric fields
            for (const [key, value] of Object.entries(numericFields)) {
                if (isNaN(value)) {
                    logger.warn(`Invalid numeric value for ${key} in row:`, row);
                    return null;
                }
            }

            // Calculate additional metrics
            const dayReturn = ((numericFields.close - numericFields.previousClose) / numericFields.previousClose) * 100;
            const volatility = ((numericFields.high - numericFields.low) / numericFields.low) * 100;
            const averagePrice = (numericFields.high + numericFields.low) / 2;

            return {
                symbol: row.SYMBOL,
                series: row.SERIES,
                timestamp: new Date(row.TIMESTAMP),
                priceData: {
                    open: numericFields.open,
                    high: numericFields.high,
                    low: numericFields.low,
                    close: numericFields.close,
                    last: numericFields.last,
                    previousClose: numericFields.previousClose
                },
                tradingData: {
                    volume: numericFields.volume,
                    value: numericFields.value,
                    trades: numericFields.trades
                },
                metrics: {
                    dayReturn: parseFloat(dayReturn.toFixed(2)),
                    volatility: parseFloat(volatility.toFixed(2)),
                    averagePrice: parseFloat(averagePrice.toFixed(2)),
                    volumeWeightedPrice: parseFloat((numericFields.value / numericFields.volume).toFixed(2))
                }
            };
        } catch (error) {
            logger.error('Error transforming row:', { error: error.message, row });
            return null;
        }
    }

    /**
     * Creates a transform stream for processing CSV data
     * @returns {Transform} Transform stream
     */
    createTransformStream() {
        return new Transform({
            objectMode: true,
            transform: (chunk, encoding, callback) => {
                const transformedData = this.transformRow(chunk);
                if (transformedData) {
                    callback(null, transformedData);
                } else {
                    callback();
                }
            }
        });
    }

    /**
     * Parses a CSV file and returns structured data
     * @param {string} filePath Path to CSV file
     * @returns {Promise<Object>} Parsed and processed data
     */
    async parseCSVFile(filePath) {
        try {
            const startTime = Date.now();
            const results = {
                data: [],
                metadata: {
                    fileName: path.basename(filePath),
                    processedAt: new Date().toISOString(),
                    totalRecords: 0,
                    validRecords: 0,
                    processingTimeMs: 0
                },
                summary: {
                    topGainers: [],
                    topLosers: [],
                    mostTraded: [],
                    marketStats: {
                        totalTradedValue: 0,
                        totalTradedVolume: 0,
                        advancers: 0,
                        decliners: 0,
                        unchanged: 0
                    }
                }
            };

            await new Promise((resolve, reject) => {
                createReadStream(filePath)
                    .pipe(csv())
                    .pipe(this.createTransformStream())
                    .on('data', (data) => {
                        results.data.push(data);
                        results.metadata.validRecords++;

                        // Update market statistics
                        results.summary.marketStats.totalTradedValue += data.tradingData.value;
                        results.summary.marketStats.totalTradedVolume += data.tradingData.volume;

                        if (data.metrics.dayReturn > 0) results.summary.marketStats.advancers++;
                        else if (data.metrics.dayReturn < 0) results.summary.marketStats.decliners++;
                        else results.summary.marketStats.unchanged++;
                    })
                    .on('end', () => {
                        // Sort and get top movers
                        results.data.sort((a, b) => b.metrics.dayReturn - a.metrics.dayReturn);
                        results.summary.topGainers = results.data.slice(0, 10)
                            .filter(stock => stock.metrics.dayReturn > 0);
                        results.summary.topLosers = results.data.slice(-10)
                            .filter(stock => stock.metrics.dayReturn < 0)
                            .reverse();

                        // Get most traded stocks
                        results.summary.mostTraded = [...results.data]
                            .sort((a, b) => b.tradingData.value - a.tradingData.value)
                            .slice(0, 10);

                        results.metadata.processingTimeMs = Date.now() - startTime;
                        resolve();
                    })
                    .on('error', reject);
            });

            logger.info('CSV parsing completed', {
                file: results.metadata.fileName,
                records: results.metadata.validRecords,
                time: results.metadata.processingTimeMs
            });

            return results;

        } catch (error) {
            logger.error('Error parsing CSV file:', { error: error.message, filePath });
            throw error;
        }
    }

    /**
     * Exports processed data to JSON file
     * @param {Object} data Processed data
     * @param {string} outputPath Output file path
     */
    async exportToJSON(data, outputPath) {
        try {
            await fs.writeFile(outputPath, JSON.stringify(data, null, 2));
            logger.info('Data exported to JSON successfully', { outputPath });
        } catch (error) {
            logger.error('Error exporting to JSON:', { error: error.message, outputPath });
            throw error;
        }
    }
}

module.exports = NSEDataParser;
