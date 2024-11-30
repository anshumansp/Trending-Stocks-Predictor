const NSEDataParser = require('../csvParser');
const fs = require('fs').promises;
const path = require('path');

describe('NSEDataParser', () => {
    let parser;
    let testDataPath;

    beforeAll(async () => {
        parser = new NSEDataParser();
        testDataPath = path.join(__dirname, 'testData.csv');

        // Create test CSV file
        const testData = `SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES
TCS,EQ,3500.00,3550.00,3480.00,3525.00,3525.00,3490.00,1000000,3525000000,2023-07-20,5000
INFY,EQ,1300.00,1320.00,1290.00,1310.00,1310.00,1295.00,500000,655000000,2023-07-20,3000
HDFCBANK,EQ,1600.00,1620.00,1580.00,1590.00,1590.00,1610.00,750000,1192500000,2023-07-20,4000`;

        await fs.writeFile(testDataPath, testData);
    });

    afterAll(async () => {
        // Clean up test file
        await fs.unlink(testDataPath);
    });

    describe('transformRow', () => {
        test('should transform valid row data correctly', () => {
            const rawRow = {
                SYMBOL: 'TCS',
                SERIES: 'EQ',
                OPEN: '3500.00',
                HIGH: '3550.00',
                LOW: '3480.00',
                CLOSE: '3525.00',
                LAST: '3525.00',
                PREVCLOSE: '3490.00',
                TOTTRDQTY: '1000000',
                TOTTRDVAL: '3525000000',
                TIMESTAMP: '2023-07-20',
                TOTALTRADES: '5000'
            };

            const transformed = parser.transformRow(rawRow);

            expect(transformed).toMatchObject({
                symbol: 'TCS',
                series: 'EQ',
                priceData: {
                    open: 3500.00,
                    high: 3550.00,
                    low: 3480.00,
                    close: 3525.00
                },
                tradingData: {
                    volume: 1000000,
                    value: 3525000000,
                    trades: 5000
                }
            });

            // Verify calculated metrics
            expect(transformed.metrics).toBeDefined();
            expect(transformed.metrics.dayReturn).toBeDefined();
            expect(transformed.metrics.volatility).toBeDefined();
        });

        test('should return null for invalid row data', () => {
            const invalidRow = {
                SYMBOL: 'TCS',
                SERIES: 'EQ',
                // Missing required fields
            };

            const transformed = parser.transformRow(invalidRow);
            expect(transformed).toBeNull();
        });

        test('should handle invalid numeric values', () => {
            const rowWithInvalidNumbers = {
                SYMBOL: 'TCS',
                SERIES: 'EQ',
                OPEN: 'invalid',
                HIGH: '3550.00',
                LOW: '3480.00',
                CLOSE: '3525.00',
                LAST: '3525.00',
                PREVCLOSE: '3490.00',
                TOTTRDQTY: '1000000',
                TOTTRDVAL: '3525000000',
                TIMESTAMP: '2023-07-20',
                TOTALTRADES: '5000'
            };

            const transformed = parser.transformRow(rowWithInvalidNumbers);
            expect(transformed).toBeNull();
        });
    });

    describe('parseCSVFile', () => {
        test('should parse CSV file successfully', async () => {
            const results = await parser.parseCSVFile(testDataPath);

            expect(results).toHaveProperty('data');
            expect(results).toHaveProperty('metadata');
            expect(results).toHaveProperty('summary');

            expect(results.data.length).toBe(3);
            expect(results.metadata.validRecords).toBe(3);
            
            // Verify summary data
            expect(results.summary.topGainers).toBeDefined();
            expect(results.summary.topLosers).toBeDefined();
            expect(results.summary.mostTraded).toBeDefined();
            expect(results.summary.marketStats).toBeDefined();
        });

        test('should handle non-existent file', async () => {
            await expect(parser.parseCSVFile('nonexistent.csv'))
                .rejects.toThrow();
        });
    });

    describe('exportToJSON', () => {
        test('should export data to JSON file', async () => {
            const testData = {
                data: [{ symbol: 'TCS', price: 3500 }],
                metadata: { records: 1 }
            };
            const outputPath = path.join(__dirname, 'output.json');

            await parser.exportToJSON(testData, outputPath);
            
            // Verify file exists and content
            const fileContent = await fs.readFile(outputPath, 'utf-8');
            const parsedContent = JSON.parse(fileContent);
            
            expect(parsedContent).toEqual(testData);

            // Clean up
            await fs.unlink(outputPath);
        });
    });
});
