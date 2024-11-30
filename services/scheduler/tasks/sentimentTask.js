const axios = require('axios');
const logger = require('../logger');
const config = require('../config');

class SentimentTask {
    async execute() {
        try {
            logger.info('Starting sentiment analysis task');

            // Get list of stocks to analyze
            const stocks = await this.getStocksForAnalysis();

            // Process each stock
            for (const stock of stocks) {
                await this.analyzeSentiment(stock);
            }

            logger.info('Sentiment analysis completed', {
                stockCount: stocks.length
            });

        } catch (error) {
            logger.error('Error in sentiment analysis task', {
                error: error.message,
                stack: error.stack
            });
            throw error;
        }
    }

    async getStocksForAnalysis() {
        try {
            const response = await axios.get(`${config.API.STOCK_DATA}/list`);
            return response.data.stocks;
        } catch (error) {
            logger.error('Error getting stocks for sentiment analysis', {
                error: error.message
            });
            throw error;
        }
    }

    async analyzeSentiment(stock) {
        try {
            logger.info(`Analyzing sentiment for ${stock.symbol}`);

            // Fetch sentiment data from various sources
            const [socialMedia, news] = await Promise.all([
                this.getSocialMediaSentiment(stock.symbol),
                this.getNewsSentiment(stock.symbol)
            ]);

            // Combine and analyze sentiment
            const sentiment = await this.combineSentiment(stock.symbol, socialMedia, news);

            // Store sentiment results
            await this.storeSentimentResults(stock.symbol, sentiment);

            logger.info(`Completed sentiment analysis for ${stock.symbol}`, {
                sentiment: sentiment.score
            });

        } catch (error) {
            logger.error(`Error analyzing sentiment for ${stock.symbol}`, {
                error: error.message
            });
            throw error;
        }
    }

    async getSocialMediaSentiment(symbol) {
        const response = await axios.get(config.API.SENTIMENT, {
            params: {
                symbol,
                source: 'social_media'
            }
        });
        return response.data;
    }

    async getNewsSentiment(symbol) {
        const response = await axios.get(config.API.SENTIMENT, {
            params: {
                symbol,
                source: 'news'
            }
        });
        return response.data;
    }

    async combineSentiment(symbol, socialMedia, news) {
        // Implement sentiment combination logic
        const combinedScore = (socialMedia.score * 0.3) + (news.score * 0.7);

        return {
            symbol,
            score: combinedScore,
            confidence: this.calculateConfidence(socialMedia, news),
            sources: {
                socialMedia,
                news
            },
            timestamp: new Date()
        };
    }

    calculateConfidence(socialMedia, news) {
        // Implement confidence calculation logic
        return (socialMedia.confidence * 0.3) + (news.confidence * 0.7);
    }

    async storeSentimentResults(symbol, sentiment) {
        try {
            await axios.post(`${config.API.SENTIMENT}/store`, {
                symbol,
                sentiment
            });
        } catch (error) {
            logger.error(`Error storing sentiment results for ${symbol}`, {
                error: error.message
            });
            throw error;
        }
    }
}

module.exports = new SentimentTask();
