require('dotenv').config();

module.exports = {
    // NSE website configuration
    nse: {
        baseUrl: 'https://www.nseindia.com',
        marketDataEndpoint: '/market-data',
        bhavCopyEndpoint: '/reports/equity-derivatives',
        requestTimeout: 30000, // 30 seconds
    },

    // Scraping configuration
    scraper: {
        maxRetries: 3,
        retryDelay: 5000, // 5 seconds
        downloadPath: './data',
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    },

    // Scheduling configuration
    schedule: {
        // Run at 15:30 IST on weekdays
        cronExpression: '30 15 * * 1-5',
        timezone: 'Asia/Kolkata',
    },

    // Logging configuration
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        directory: './logs',
        maxFiles: '14d', // Keep logs for 14 days
    }
};
