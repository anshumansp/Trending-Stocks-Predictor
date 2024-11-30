const { logger } = require('./utils');
const TechnicalAnalysis = require('./analysis');

class StockRankingSystem {
    constructor(config = {}) {
        this.config = {
            // Technical Analysis Weights
            weights: {
                technical: 0.4,    // Technical indicators
                fundamental: 0.3,  // Fundamental metrics
                sentiment: 0.3,    // Market sentiment
                ...config.weights
            },
            
            // Filtering thresholds
            thresholds: {
                minVolume: 100000,           // Minimum daily volume
                minPrice: 10,                // Minimum stock price
                minMarketCap: 1000000000,    // 1 Billion minimum market cap
                maxVolatility: 50,           // Maximum allowed volatility (%)
                minTrades: 1000,             // Minimum number of daily trades
                ...config.thresholds
            },

            // Scoring parameters
            scoring: {
                volumeWeight: 0.2,
                momentumWeight: 0.3,
                trendWeight: 0.3,
                sentimentWeight: 0.2,
                ...config.scoring
            }
        };
    }

    /**
     * Calculate technical score based on various indicators
     * @param {Object} stock Stock data with technical indicators
     * @returns {number} Technical score (0-1)
     */
    calculateTechnicalScore(stock) {
        try {
            const scores = {
                trend: 0,
                momentum: 0,
                volume: 0
            };

            // Trend Analysis
            if (stock.technicalIndicators) {
                const { sma20, sma50, macd } = stock.technicalIndicators;
                
                // Trend score based on moving averages
                if (sma20 > sma50) {
                    scores.trend += 0.6;  // Upward trend
                    if (stock.priceData.close > sma20) {
                        scores.trend += 0.4;  // Strong upward trend
                    }
                }

                // Momentum score based on MACD
                if (macd && macd.histogram > 0) {
                    scores.momentum += 0.5;
                    if (macd.histogram > macd.signal) {
                        scores.momentum += 0.5;  // Strong momentum
                    }
                }
            }

            // Volume Analysis
            const avgVolume = stock.tradingData.volume;
            if (avgVolume > this.config.thresholds.minVolume) {
                scores.volume = Math.min(
                    1,
                    (avgVolume - this.config.thresholds.minVolume) / 
                    (this.config.thresholds.minVolume * 10)
                );
            }

            // Weighted technical score
            return (
                scores.trend * this.config.scoring.trendWeight +
                scores.momentum * this.config.scoring.momentumWeight +
                scores.volume * this.config.scoring.volumeWeight
            );
        } catch (error) {
            logger.error('Error calculating technical score:', { 
                error: error.message,
                symbol: stock.symbol 
            });
            return 0;
        }
    }

    /**
     * Calculate fundamental score based on key metrics
     * @param {Object} stock Stock data with fundamental metrics
     * @returns {number} Fundamental score (0-1)
     */
    calculateFundamentalScore(stock) {
        try {
            let score = 0;

            // Price momentum
            const priceChange = stock.metrics.dayReturn;
            if (priceChange > 0) {
                score += Math.min(priceChange / 10, 0.3);  // Cap at 30%
            }

            // Volume strength
            const volumeScore = Math.min(
                stock.tradingData.volume / (this.config.thresholds.minVolume * 10),
                0.3
            );
            score += volumeScore;

            // Trading activity
            const tradesScore = Math.min(
                stock.tradingData.trades / (this.config.thresholds.minTrades * 2),
                0.2
            );
            score += tradesScore;

            // Volatility check (lower is better)
            const volatilityPenalty = Math.max(
                0,
                stock.metrics.volatility / this.config.thresholds.maxVolatility
            );
            score = Math.max(0, score - volatilityPenalty * 0.2);

            return score;
        } catch (error) {
            logger.error('Error calculating fundamental score:', {
                error: error.message,
                symbol: stock.symbol
            });
            return 0;
        }
    }

    /**
     * Calculate sentiment score from various sources
     * @param {Object} stock Stock data with sentiment metrics
     * @returns {number} Sentiment score (0-1)
     */
    calculateSentimentScore(stock) {
        try {
            if (!stock.sentiment) return 0.5; // Neutral if no sentiment data

            const {
                socialMedia = {},
                newsAnalysis = {},
                analystRatings = {}
            } = stock.sentiment;

            // Social media sentiment (Twitter, Reddit, etc.)
            const socialScore = socialMedia.score || 0.5;

            // News sentiment
            const newsScore = newsAnalysis.score || 0.5;

            // Analyst ratings
            const analystScore = analystRatings.score || 0.5;

            // Weighted average of all sentiment sources
            return (
                socialScore * 0.3 +
                newsScore * 0.3 +
                analystScore * 0.4
            );
        } catch (error) {
            logger.error('Error calculating sentiment score:', {
                error: error.message,
                symbol: stock.symbol
            });
            return 0.5;
        }
    }

    /**
     * Filter stocks based on basic criteria
     * @param {Array} stocks Array of stock data
     * @returns {Array} Filtered stocks
     */
    filterStocks(stocks) {
        return stocks.filter(stock => {
            try {
                const { priceData, tradingData, metrics } = stock;

                return (
                    // Volume threshold
                    tradingData.volume >= this.config.thresholds.minVolume &&
                    // Price threshold
                    priceData.close >= this.config.thresholds.minPrice &&
                    // Volatility threshold
                    metrics.volatility <= this.config.thresholds.maxVolatility &&
                    // Trading activity threshold
                    tradingData.trades >= this.config.thresholds.minTrades
                );
            } catch (error) {
                logger.warn('Error filtering stock:', {
                    error: error.message,
                    symbol: stock.symbol
                });
                return false;
            }
        });
    }

    /**
     * Calculate final score and rank stocks
     * @param {Array} stocks Array of stock data
     * @returns {Array} Ranked stocks with scores
     */
    rankStocks(stocks) {
        try {
            const rankedStocks = this.filterStocks(stocks).map(stock => {
                // Calculate individual scores
                const technicalScore = this.calculateTechnicalScore(stock);
                const fundamentalScore = this.calculateFundamentalScore(stock);
                const sentimentScore = this.calculateSentimentScore(stock);

                // Calculate weighted final score
                const finalScore = (
                    technicalScore * this.config.weights.technical +
                    fundamentalScore * this.config.weights.fundamental +
                    sentimentScore * this.config.weights.sentiment
                );

                return {
                    ...stock,
                    rankings: {
                        technicalScore,
                        fundamentalScore,
                        sentimentScore,
                        finalScore
                    }
                };
            });

            // Sort by final score in descending order
            rankedStocks.sort((a, b) => b.rankings.finalScore - a.rankings.finalScore);

            // Add rank position
            rankedStocks.forEach((stock, index) => {
                stock.rankings.rank = index + 1;
            });

            return rankedStocks;
        } catch (error) {
            logger.error('Error ranking stocks:', { error: error.message });
            throw error;
        }
    }

    /**
     * Get top stock recommendations
     * @param {Array} stocks Array of stock data
     * @param {number} limit Number of stocks to return
     * @returns {Array} Top recommended stocks
     */
    getTopRecommendations(stocks, limit = 10) {
        try {
            const rankedStocks = this.rankStocks(stocks);
            const recommendations = rankedStocks.slice(0, limit);

            // Add recommendation strength
            recommendations.forEach(stock => {
                const { finalScore } = stock.rankings;
                let strength;
                if (finalScore >= 0.8) strength = 'Strong Buy';
                else if (finalScore >= 0.6) strength = 'Buy';
                else if (finalScore >= 0.4) strength = 'Hold';
                else if (finalScore >= 0.2) strength = 'Sell';
                else strength = 'Strong Sell';

                stock.recommendation = {
                    strength,
                    confidence: finalScore * 100,
                    reasons: this.generateRecommendationReasons(stock)
                };
            });

            return recommendations;
        } catch (error) {
            logger.error('Error getting top recommendations:', { error: error.message });
            throw error;
        }
    }

    /**
     * Generate reasons for the recommendation
     * @param {Object} stock Stock data with scores
     * @returns {Array} Array of reason strings
     */
    generateRecommendationReasons(stock) {
        const reasons = [];
        const { technicalScore, fundamentalScore, sentimentScore } = stock.rankings;

        if (technicalScore > 0.7) {
            reasons.push('Strong technical indicators');
        }
        if (fundamentalScore > 0.7) {
            reasons.push('Solid fundamental metrics');
        }
        if (sentimentScore > 0.7) {
            reasons.push('Positive market sentiment');
        }
        if (stock.metrics.dayReturn > 5) {
            reasons.push('Significant price momentum');
        }
        if (stock.tradingData.volume > this.config.thresholds.minVolume * 2) {
            reasons.push('High trading volume');
        }

        return reasons;
    }
}

module.exports = StockRankingSystem;
