const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const db = require('./database');
const TechnicalAnalysis = require('./analysis');
const { logger } = require('./utils');
const config = require('./config');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Error handler middleware
const errorHandler = (err, req, res, next) => {
    logger.error('API Error:', { error: err.message, path: req.path });
    res.status(500).json({ error: 'Internal server error' });
};

// Routes
app.get('/api/stocks', async (req, res) => {
    try {
        const { date } = req.query;
        const stocks = await db.Stock.find({ date: new Date(date) });
        res.json(stocks);
    } catch (error) {
        next(error);
    }
});

app.get('/api/stocks/:symbol', async (req, res) => {
    try {
        const { symbol } = req.params;
        const { days = 30 } = req.query;
        const history = await db.getStockHistory(symbol, parseInt(days));
        
        // Calculate technical indicators
        const analysis = new TechnicalAnalysis(history);
        const technicalData = {
            sma: {
                20: analysis.calculateSMA(20),
                50: analysis.calculateSMA(50)
            },
            rsi: analysis.calculateRSI(),
            macd: analysis.calculateMACD(),
            bollingerBands: analysis.calculateBollingerBands(),
            patterns: analysis.identifyPatterns()
        };

        res.json({
            symbol,
            history,
            technicalData
        });
    } catch (error) {
        next(error);
    }
});

app.get('/api/movers', async (req, res) => {
    try {
        const { date = new Date() } = req.query;
        const movers = await db.getTopMovers(new Date(date));
        res.json(movers);
    } catch (error) {
        next(error);
    }
});

app.get('/api/analysis/:symbol', async (req, res) => {
    try {
        const { symbol } = req.params;
        const history = await db.getStockHistory(symbol, 100);
        const analysis = new TechnicalAnalysis(history);
        
        const signals = analysis.generateSignals();
        const patterns = analysis.identifyPatterns();
        
        res.json({
            symbol,
            signals,
            patterns,
            lastUpdated: new Date()
        });
    } catch (error) {
        next(error);
    }
});

app.get('/api/market/summary', async (req, res) => {
    try {
        const date = new Date();
        const [topMovers, mostTraded] = await Promise.all([
            db.getTopMovers(date),
            db.Stock.find({ date })
                .sort({ 'tradingData.volume': -1 })
                .limit(10)
        ]);

        res.json({
            date,
            topMovers,
            mostTraded,
            marketStatus: {
                isOpen: isMarketOpen(),
                nextOpenTime: getNextMarketOpenTime()
            }
        });
    } catch (error) {
        next(error);
    }
});

// Error handling middleware
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    logger.info(`API server running on port ${PORT}`);
});
