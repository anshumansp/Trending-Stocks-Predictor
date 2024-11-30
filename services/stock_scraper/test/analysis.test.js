const TechnicalAnalysis = require('../analysis');

describe('TechnicalAnalysis', () => {
    let analysis;
    
    beforeEach(() => {
        // Sample historical data
        const historicalData = [
            { date: '2023-01-01', open: 100, high: 105, low: 98, close: 103, volume: 1000 },
            { date: '2023-01-02', open: 103, high: 108, low: 102, close: 107, volume: 1200 },
            { date: '2023-01-03', open: 107, high: 110, low: 105, close: 106, volume: 900 },
            // Add more sample data as needed
        ];
        analysis = new TechnicalAnalysis(historicalData);
    });

    describe('SMA Calculation', () => {
        test('should calculate Simple Moving Average correctly', () => {
            const sma = analysis.calculateSMA(2);
            expect(sma[1]).toBeCloseTo((103 + 107) / 2);
        });
    });

    describe('RSI Calculation', () => {
        test('should calculate RSI within valid range', () => {
            const rsi = analysis.calculateRSI();
            rsi.forEach(value => {
                expect(value).toBeGreaterThanOrEqual(0);
                expect(value).toBeLessThanOrEqual(100);
            });
        });
    });

    describe('MACD Calculation', () => {
        test('should return MACD with all components', () => {
            const macd = analysis.calculateMACD();
            expect(macd).toHaveProperty('macdLine');
            expect(macd).toHaveProperty('signalLine');
            expect(macd).toHaveProperty('histogram');
        });
    });

    describe('Pattern Recognition', () => {
        test('should identify basic patterns', () => {
            const patterns = analysis.identifyPatterns();
            expect(Array.isArray(patterns)).toBe(true);
        });
    });

    describe('Signal Generation', () => {
        test('should generate trading signals', () => {
            const signals = analysis.generateSignals();
            signals.forEach(signal => {
                expect(signal).toHaveProperty('type');
                expect(signal).toHaveProperty('reason');
                expect(signal).toHaveProperty('strength');
                expect(['BUY', 'SELL']).toContain(signal.type);
            });
        });
    });
});
