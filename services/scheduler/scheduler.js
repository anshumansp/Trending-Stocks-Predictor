const cron = require('node-cron');
const moment = require('moment-timezone');
const Bull = require('bull');
const logger = require('./logger');
const config = require('./config');

// Import tasks
const stockDataTask = require('./tasks/stockDataTask');
const sentimentTask = require('./tasks/sentimentTask');
const evaluationTask = require('./tasks/evaluationTask');

// Initialize queues
const stockDataQueue = new Bull('stockData', {
    redis: config.REDIS,
    defaultJobOptions: config.QUEUE
});

const sentimentQueue = new Bull('sentiment', {
    redis: config.REDIS,
    defaultJobOptions: config.QUEUE
});

const evaluationQueue = new Bull('evaluation', {
    redis: config.REDIS,
    defaultJobOptions: config.QUEUE
});

class Scheduler {
    constructor() {
        this.tasks = new Map();
        this.initialize();
    }

    initialize() {
        // Initialize task queues
        this.setupQueues();

        // Schedule tasks
        this.scheduleTasks();

        // Setup error handling
        this.setupErrorHandling();

        logger.info('Scheduler initialized');
    }

    setupQueues() {
        // Stock data queue processing
        stockDataQueue.process(async job => {
            try {
                await stockDataTask.execute();
                return { status: 'success' };
            } catch (error) {
                logger.error('Stock data task failed', { error: error.message });
                throw error;
            }
        });

        // Sentiment analysis queue processing
        sentimentQueue.process(async job => {
            try {
                await sentimentTask.execute();
                return { status: 'success' };
            } catch (error) {
                logger.error('Sentiment task failed', { error: error.message });
                throw error;
            }
        });

        // Evaluation queue processing
        evaluationQueue.process(async job => {
            try {
                await evaluationTask.execute();
                return { status: 'success' };
            } catch (error) {
                logger.error('Evaluation task failed', { error: error.message });
                throw error;
            }
        });
    }

    scheduleTasks() {
        // Schedule stock data collection
        this.scheduleTask('stockData', config.SCHEDULES.STOCK_DATA, async () => {
            if (this.isMarketDay()) {
                await stockDataQueue.add({
                    timestamp: new Date()
                });
            }
        });

        // Schedule sentiment analysis
        this.scheduleTask('sentiment', config.SCHEDULES.SENTIMENT_ANALYSIS, async () => {
            if (this.isMarketDay()) {
                await sentimentQueue.add({
                    timestamp: new Date()
                });
            }
        });

        // Schedule stock evaluation
        this.scheduleTask('evaluation', config.SCHEDULES.STOCK_EVALUATION, async () => {
            if (this.isMarketDay()) {
                await evaluationQueue.add({
                    timestamp: new Date()
                });
            }
        });

        // Schedule intraday updates
        this.scheduleTask('intradayUpdate', config.SCHEDULES.INTRADAY_UPDATE, async () => {
            if (this.isMarketHours()) {
                await this.runIntradayUpdate();
            }
        });

        // Schedule model retraining
        this.scheduleTask('modelRetrain', config.SCHEDULES.MODEL_RETRAIN, async () => {
            await this.runModelRetraining();
        });
    }

    scheduleTask(name, cronExpression, task) {
        if (!cron.validate(cronExpression)) {
            logger.error(`Invalid cron expression for ${name}`, { cronExpression });
            return;
        }

        const scheduledTask = cron.schedule(cronExpression, async () => {
            try {
                logger.info(`Starting scheduled task: ${name}`);
                await task();
                logger.info(`Completed scheduled task: ${name}`);
            } catch (error) {
                logger.error(`Error in scheduled task: ${name}`, {
                    error: error.message,
                    stack: error.stack
                });
            }
        }, {
            timezone: config.MARKET_TIMEZONE
        });

        this.tasks.set(name, scheduledTask);
        logger.info(`Scheduled task: ${name}`, { cronExpression });
    }

    isMarketDay() {
        const now = moment().tz(config.MARKET_TIMEZONE);
        return now.day() !== 0 && now.day() !== 6;  // Not Sunday or Saturday
    }

    isMarketHours() {
        const now = moment().tz(config.MARKET_TIMEZONE);
        const marketOpen = moment.tz(config.MARKET_OPEN_TIME, 'HH:mm', config.MARKET_TIMEZONE);
        const marketClose = moment.tz(config.MARKET_CLOSE_TIME, 'HH:mm', config.MARKET_TIMEZONE);

        return now.isBetween(marketOpen, marketClose);
    }

    async runIntradayUpdate() {
        try {
            // Update stock data
            await stockDataQueue.add({
                type: 'intraday',
                timestamp: new Date()
            });

            // Update evaluations
            await evaluationQueue.add({
                type: 'intraday',
                timestamp: new Date()
            });

        } catch (error) {
            logger.error('Error in intraday update', {
                error: error.message
            });
        }
    }

    async runModelRetraining() {
        try {
            logger.info('Starting model retraining');
            
            // Add model retraining job
            await evaluationQueue.add({
                type: 'retrain',
                timestamp: new Date()
            }, {
                priority: 10
            });

        } catch (error) {
            logger.error('Error in model retraining', {
                error: error.message
            });
        }
    }

    setupErrorHandling() {
        process.on('uncaughtException', error => {
            logger.error('Uncaught exception', {
                error: error.message,
                stack: error.stack
            });
        });

        process.on('unhandledRejection', error => {
            logger.error('Unhandled rejection', {
                error: error.message,
                stack: error.stack
            });
        });
    }

    async stop() {
        logger.info('Stopping scheduler');

        // Stop all scheduled tasks
        for (const [name, task] of this.tasks) {
            task.stop();
            logger.info(`Stopped task: ${name}`);
        }

        // Close queues
        await Promise.all([
            stockDataQueue.close(),
            sentimentQueue.close(),
            evaluationQueue.close()
        ]);

        logger.info('Scheduler stopped');
    }
}

// Create and start scheduler
const scheduler = new Scheduler();

// Handle shutdown
process.on('SIGTERM', async () => {
    await scheduler.stop();
    process.exit(0);
});

module.exports = scheduler;
