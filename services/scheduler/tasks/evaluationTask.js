const axios = require('axios');
const logger = require('../logger');
const config = require('../config');

class EvaluationTask {
    async execute() {
        try {
            logger.info('Starting stock evaluation task');

            // Get stocks to evaluate
            const stocks = await this.getStocksForEvaluation();

            // Process each stock
            for (const stock of stocks) {
                await this.evaluateStock(stock);
            }

            logger.info('Stock evaluation completed', {
                stockCount: stocks.length
            });

        } catch (error) {
            logger.error('Error in stock evaluation task', {
                error: error.message,
                stack: error.stack
            });
            throw error;
        }
    }

    async getStocksForEvaluation() {
        try {
            const response = await axios.get(`${config.API.STOCK_DATA}/list`);
            return response.data.stocks;
        } catch (error) {
            logger.error('Error getting stocks for evaluation', {
                error: error.message
            });
            throw error;
        }
    }

    async evaluateStock(stock) {
        try {
            logger.info(`Evaluating stock ${stock.symbol}`);

            // Gather all necessary data
            const [technicalData, sentimentData, marketData] = await Promise.all([
                this.getTechnicalData(stock.symbol),
                this.getSentimentData(stock.symbol),
                this.getMarketData()
            ]);

            // Perform evaluation
            const evaluation = await this.performEvaluation(stock.symbol, {
                technical: technicalData,
                sentiment: sentimentData,
                market: marketData
            });

            // Store evaluation results
            await this.storeEvaluationResults(stock.symbol, evaluation);

            logger.info(`Completed evaluation for ${stock.symbol}`, {
                recommendation: evaluation.recommendation
            });

        } catch (error) {
            logger.error(`Error evaluating stock ${stock.symbol}`, {
                error: error.message
            });
            throw error;
        }
    }

    async getTechnicalData(symbol) {
        const response = await axios.get(`${config.API.STOCK_DATA}/technical`, {
            params: { symbol }
        });
        return response.data;
    }

    async getSentimentData(symbol) {
        const response = await axios.get(`${config.API.SENTIMENT}/latest`, {
            params: { symbol }
        });
        return response.data;
    }

    async getMarketData() {
        const response = await axios.get(`${config.API.STOCK_DATA}/market`);
        return response.data;
    }

    async performEvaluation(symbol, data) {
        try {
            const response = await axios.post(config.API.EVALUATION, {
                symbol,
                data
            });

            return response.data;
        } catch (error) {
            logger.error(`Error performing evaluation for ${symbol}`, {
                error: error.message
            });
            throw error;
        }
    }

    async storeEvaluationResults(symbol, evaluation) {
        try {
            await axios.post(`${config.API.EVALUATION}/store`, {
                symbol,
                evaluation
            });
        } catch (error) {
            logger.error(`Error storing evaluation results for ${symbol}`, {
                error: error.message
            });
            throw error;
        }
    }

    async updateRecommendations() {
        try {
            logger.info('Updating stock recommendations');

            const evaluations = await this.getAllEvaluations();
            const recommendations = this.generateRecommendations(evaluations);

            await this.storeRecommendations(recommendations);

            logger.info('Stock recommendations updated', {
                recommendationCount: recommendations.length
            });

        } catch (error) {
            logger.error('Error updating recommendations', {
                error: error.message
            });
            throw error;
        }
    }

    async getAllEvaluations() {
        const response = await axios.get(`${config.API.EVALUATION}/all`);
        return response.data.evaluations;
    }

    generateRecommendations(evaluations) {
        // Implement recommendation generation logic
        return evaluations.map(eval => ({
            symbol: eval.symbol,
            recommendation: eval.recommendation,
            confidence: eval.confidence,
            factors: eval.factors,
            timestamp: new Date()
        }));
    }

    async storeRecommendations(recommendations) {
        await axios.post(`${config.API.EVALUATION}/recommendations`, {
            recommendations
        });
    }
}

module.exports = new EvaluationTask();
