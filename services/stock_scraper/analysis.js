const { logger } = require('./utils');

class TechnicalAnalysis {
    constructor(historicalData) {
        this.data = historicalData;
    }

    calculateSMA(period) {
        const prices = this.data.map(d => d.close);
        const sma = [];
        
        for (let i = 0; i < prices.length; i++) {
            if (i < period - 1) {
                sma.push(null);
                continue;
            }
            
            const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
            sma.push(sum / period);
        }
        
        return sma;
    }

    calculateEMA(period) {
        const prices = this.data.map(d => d.close);
        const ema = [];
        const multiplier = 2 / (period + 1);

        // First EMA is SMA
        const firstSMA = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
        ema.push(firstSMA);

        for (let i = 1; i < prices.length; i++) {
            const value = (prices[i] - ema[i - 1]) * multiplier + ema[i - 1];
            ema.push(value);
        }

        return ema;
    }

    calculateRSI(period = 14) {
        const prices = this.data.map(d => d.close);
        const rsi = [];
        let gains = [];
        let losses = [];

        // Calculate price changes
        for (let i = 1; i < prices.length; i++) {
            const change = prices[i] - prices[i - 1];
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? -change : 0);
        }

        // Calculate initial averages
        let avgGain = gains.slice(0, period).reduce((a, b) => a + b, 0) / period;
        let avgLoss = losses.slice(0, period).reduce((a, b) => a + b, 0) / period;

        // Calculate RSI
        for (let i = period; i < prices.length; i++) {
            avgGain = ((avgGain * (period - 1)) + gains[i - 1]) / period;
            avgLoss = ((avgLoss * (period - 1)) + losses[i - 1]) / period;

            const rs = avgGain / avgLoss;
            rsi.push(100 - (100 / (1 + rs)));
        }

        return rsi;
    }

    calculateMACD(shortPeriod = 12, longPeriod = 26, signalPeriod = 9) {
        const shortEMA = this.calculateEMA(shortPeriod);
        const longEMA = this.calculateEMA(longPeriod);
        const macdLine = shortEMA.map((value, index) => value - longEMA[index]);
        const signalLine = this.calculateEMA(signalPeriod);
        const histogram = macdLine.map((value, index) => value - signalLine[index]);

        return {
            macdLine,
            signalLine,
            histogram
        };
    }

    calculateBollingerBands(period = 20, stdDev = 2) {
        const sma = this.calculateSMA(period);
        const bands = [];

        for (let i = period - 1; i < this.data.length; i++) {
            const slice = this.data.slice(i - period + 1, i + 1);
            const mean = sma[i];
            
            // Calculate standard deviation
            const squaredDiffs = slice.map(d => Math.pow(d.close - mean, 2));
            const variance = squaredDiffs.reduce((a, b) => a + b, 0) / period;
            const std = Math.sqrt(variance);

            bands.push({
                upper: mean + (stdDev * std),
                middle: mean,
                lower: mean - (stdDev * std)
            });
        }

        return bands;
    }

    identifyPatterns() {
        const patterns = [];
        const prices = this.data;

        for (let i = 3; i < prices.length; i++) {
            // Bullish Engulfing
            if (prices[i-1].close < prices[i-1].open && 
                prices[i].close > prices[i].open &&
                prices[i].open < prices[i-1].close &&
                prices[i].close > prices[i-1].open) {
                patterns.push({
                    date: prices[i].date,
                    pattern: 'Bullish Engulfing',
                    significance: 'Potential reversal'
                });
            }

            // Bearish Engulfing
            if (prices[i-1].close > prices[i-1].open &&
                prices[i].close < prices[i].open &&
                prices[i].open > prices[i-1].close &&
                prices[i].close < prices[i-1].open) {
                patterns.push({
                    date: prices[i].date,
                    pattern: 'Bearish Engulfing',
                    significance: 'Potential reversal'
                });
            }

            // Doji
            const bodySize = Math.abs(prices[i].close - prices[i].open);
            const totalSize = prices[i].high - prices[i].low;
            if (bodySize / totalSize < 0.1) {
                patterns.push({
                    date: prices[i].date,
                    pattern: 'Doji',
                    significance: 'Potential trend reversal'
                });
            }
        }

        return patterns;
    }

    generateSignals() {
        const signals = [];
        const rsi = this.calculateRSI();
        const macd = this.calculateMACD();
        const sma20 = this.calculateSMA(20);
        const sma50 = this.calculateSMA(50);

        for (let i = 50; i < this.data.length; i++) {
            // RSI signals
            if (rsi[i] < 30) {
                signals.push({
                    date: this.data[i].date,
                    type: 'BUY',
                    reason: 'RSI oversold',
                    strength: 'Medium'
                });
            } else if (rsi[i] > 70) {
                signals.push({
                    date: this.data[i].date,
                    type: 'SELL',
                    reason: 'RSI overbought',
                    strength: 'Medium'
                });
            }

            // MACD signals
            if (macd.histogram[i] > 0 && macd.histogram[i - 1] < 0) {
                signals.push({
                    date: this.data[i].date,
                    type: 'BUY',
                    reason: 'MACD crossover',
                    strength: 'Strong'
                });
            } else if (macd.histogram[i] < 0 && macd.histogram[i - 1] > 0) {
                signals.push({
                    date: this.data[i].date,
                    type: 'SELL',
                    reason: 'MACD crossover',
                    strength: 'Strong'
                });
            }

            // Moving Average Crossover
            if (sma20[i] > sma50[i] && sma20[i - 1] < sma50[i - 1]) {
                signals.push({
                    date: this.data[i].date,
                    type: 'BUY',
                    reason: 'Golden Cross',
                    strength: 'Strong'
                });
            } else if (sma20[i] < sma50[i] && sma20[i - 1] > sma50[i - 1]) {
                signals.push({
                    date: this.data[i].date,
                    type: 'SELL',
                    reason: 'Death Cross',
                    strength: 'Strong'
                });
            }
        }

        return signals;
    }
}

module.exports = TechnicalAnalysis;
