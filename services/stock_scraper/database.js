const mongoose = require('mongoose');
const { logger } = require('./utils');
const config = require('./config');

// Stock Schema
const stockSchema = new mongoose.Schema({
    symbol: { type: String, required: true },
    series: { type: String, required: true },
    date: { type: Date, required: true },
    priceData: {
        open: Number,
        high: Number,
        low: Number,
        close: Number,
        previousClose: Number
    },
    tradingData: {
        volume: Number,
        value: Number,
        trades: Number
    },
    metrics: {
        dayReturn: Number,
        volatility: Number,
        volumeWeightedPrice: Number
    },
    technicalIndicators: {
        sma20: Number,
        sma50: Number,
        rsi: Number,
        macd: {
            value: Number,
            signal: Number,
            histogram: Number
        }
    },
    created_at: { type: Date, default: Date.now }
});

// Create indexes
stockSchema.index({ symbol: 1, date: 1 }, { unique: true });
stockSchema.index({ date: 1 });

const Stock = mongoose.model('Stock', mongoose.Schema);

// Historical Data Schema
const historicalDataSchema = new mongoose.Schema({
    symbol: { type: String, required: true },
    data: [{
        date: Date,
        open: Number,
        high: Number,
        low: Number,
        close: Number,
        volume: Number
    }],
    lastUpdated: { type: Date, default: Date.now }
});

historicalDataSchema.index({ symbol: 1 }, { unique: true });

const HistoricalData = mongoose.model('HistoricalData', historicalDataSchema);

class DatabaseService {
    constructor() {
        this.isConnected = false;
    }

    async connect() {
        try {
            await mongoose.connect(config.database.uri, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
                useCreateIndex: true
            });
            this.isConnected = true;
            logger.info('Successfully connected to MongoDB');
        } catch (error) {
            logger.error('MongoDB connection error:', { error: error.message });
            throw error;
        }
    }

    async saveStockData(stockData) {
        try {
            const operations = stockData.map(data => ({
                updateOne: {
                    filter: { symbol: data.symbol, date: data.date },
                    update: { $set: data },
                    upsert: true
                }
            }));

            const result = await Stock.bulkWrite(operations);
            logger.info(`Saved ${result.upsertedCount} new stocks, modified ${result.modifiedCount} existing records`);
            return result;
        } catch (error) {
            logger.error('Error saving stock data:', { error: error.message });
            throw error;
        }
    }

    async getStockHistory(symbol, days = 30) {
        try {
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(startDate.getDate() - days);

            return await Stock.find({
                symbol,
                date: { $gte: startDate, $lte: endDate }
            }).sort({ date: 1 });
        } catch (error) {
            logger.error('Error fetching stock history:', { error: error.message });
            throw error;
        }
    }

    async getTopMovers(date, limit = 10) {
        try {
            const dayData = await Stock.find({ date })
                .sort({ 'metrics.dayReturn': -1 })
                .limit(limit);

            return {
                gainers: dayData.filter(stock => stock.metrics.dayReturn > 0),
                losers: dayData.filter(stock => stock.metrics.dayReturn < 0).reverse()
            };
        } catch (error) {
            logger.error('Error fetching top movers:', { error: error.message });
            throw error;
        }
    }

    async updateHistoricalData(symbol, historicalData) {
        try {
            await HistoricalData.updateOne(
                { symbol },
                { 
                    $set: { 
                        data: historicalData,
                        lastUpdated: new Date()
                    }
                },
                { upsert: true }
            );
            logger.info(`Updated historical data for ${symbol}`);
        } catch (error) {
            logger.error('Error updating historical data:', { error: error.message });
            throw error;
        }
    }

    async close() {
        if (this.isConnected) {
            await mongoose.connection.close();
            this.isConnected = false;
            logger.info('Closed MongoDB connection');
        }
    }
}

module.exports = new DatabaseService();
