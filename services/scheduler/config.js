require('dotenv').config();

module.exports = {
    // Market schedule
    MARKET_TIMEZONE: 'Asia/Kolkata',  // IST for NSE
    MARKET_OPEN_TIME: '09:15',
    MARKET_CLOSE_TIME: '15:30',
    PRE_MARKET_TIME: '09:00',
    POST_MARKET_TIME: '16:00',

    // Task schedules
    SCHEDULES: {
        STOCK_DATA: '30 9 * * 1-5',  // 9:30 AM on weekdays
        SENTIMENT_ANALYSIS: '35 9 * * 1-5',  // 9:35 AM on weekdays
        STOCK_EVALUATION: '40 9 * * 1-5',  // 9:40 AM on weekdays
        INTRADAY_UPDATE: '*/15 9-15 * * 1-5',  // Every 15 mins during market hours
        MODEL_RETRAIN: '0 17 * * 5'  // 5 PM on Fridays
    },

    // API endpoints
    API: {
        STOCK_DATA: `${process.env.API_BASE_URL}/api/v1/stock/data`,
        SENTIMENT: `${process.env.API_BASE_URL}/api/v1/stock/sentiment`,
        EVALUATION: `${process.env.API_BASE_URL}/api/v1/stock/evaluate`
    },

    // Redis configuration
    REDIS: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379
    },

    // MongoDB configuration
    MONGODB: {
        uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/stock_analysis'
    },

    // Queue configuration
    QUEUE: {
        attempts: 3,
        backoff: {
            type: 'exponential',
            delay: 1000
        }
    },

    // Logging configuration
    LOGGING: {
        level: process.env.LOG_LEVEL || 'info',
        filename: 'scheduler.log'
    }
};
