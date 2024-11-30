const winston = require('winston');
const { format } = require('winston');
const path = require('path');
const config = require('./config');

// Configure logger
const logger = winston.createLogger({
    level: config.logging.level,
    format: format.combine(
        format.timestamp(),
        format.json(),
        format.printf(({ timestamp, level, message, ...rest }) => {
            return `${timestamp} [${level.toUpperCase()}]: ${message} ${Object.keys(rest).length ? JSON.stringify(rest) : ''}`;
        })
    ),
    transports: [
        new winston.transports.File({
            filename: path.join(config.logging.directory, 'error.log'),
            level: 'error',
            maxFiles: config.logging.maxFiles
        }),
        new winston.transports.File({
            filename: path.join(config.logging.directory, 'combined.log'),
            maxFiles: config.logging.maxFiles
        })
    ]
});

if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: format.simple()
    }));
}

// Retry mechanism with exponential backoff
async function retry(fn, options = {}) {
    const maxRetries = options.maxRetries || config.scraper.maxRetries;
    const initialDelay = options.retryDelay || config.scraper.retryDelay;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await fn();
        } catch (error) {
            if (attempt === maxRetries) {
                throw error;
            }
            
            const delay = initialDelay * Math.pow(2, attempt - 1);
            logger.warn(`Attempt ${attempt} failed. Retrying in ${delay}ms...`, {
                error: error.message,
                attempt,
                delay
            });
            
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// Validate CSV data
function validateCSVData(filePath) {
    // Add validation logic here
    return true;
}

// Format date for file naming
function formatDate(date = new Date()) {
    return date.toISOString().split('T')[0];
}

// Check if market is open
function isMarketOpen() {
    const now = new Date();
    const day = now.getDay();
    const hours = now.getHours();
    const minutes = now.getMinutes();

    // Market is closed on weekends (Saturday = 6, Sunday = 0)
    if (day === 0 || day === 6) return false;

    // Market hours are 9:15 AM to 3:30 PM IST
    const timeInMinutes = hours * 60 + minutes;
    return timeInMinutes >= 555 && timeInMinutes <= 930;
}

module.exports = {
    logger,
    retry,
    validateCSVData,
    formatDate,
    isMarketOpen
};
