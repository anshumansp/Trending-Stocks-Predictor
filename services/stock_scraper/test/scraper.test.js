const NSEStockScraper = require('../index');
const fs = require('fs');
const path = require('path');

describe('NSEStockScraper', () => {
    let scraper;

    beforeEach(() => {
        scraper = new NSEStockScraper();
    });

    afterEach(async () => {
        if (scraper) {
            await scraper.close();
        }
    });

    test('should create download directory if it doesn\'t exist', () => {
        const downloadPath = path.join(__dirname, '../data');
        expect(fs.existsSync(downloadPath)).toBe(true);
    });

    test('should initialize browser successfully', async () => {
        await scraper.initializeBrowser();
        expect(scraper.browser).toBeDefined();
        expect(scraper.page).toBeDefined();
    });

    // Note: Add more specific tests based on your needs
});
