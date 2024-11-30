const puppeteer = require('puppeteer');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const cron = require('node-cron');
const config = require('./config');
const { logger, retry, validateCSVData, formatDate, isMarketOpen } = require('./utils');

class NSEStockScraper {
    constructor() {
        this.baseUrl = config.nse.baseUrl;
        this.downloadPath = path.resolve(config.scraper.downloadPath);
        this.ensureDirectories();
    }

    ensureDirectories() {
        // Ensure download and log directories exist
        [this.downloadPath, config.logging.directory].forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        });
    }

    async initializeBrowser() {
        try {
            this.browser = await puppeteer.launch({
                headless: 'new',
                args: ['--no-sandbox', '--disable-setuid-sandbox'],
                timeout: config.nse.requestTimeout
            });
            this.page = await this.browser.newPage();

            // Configure page settings
            await this.page.setUserAgent(config.scraper.userAgent);
            await this.page.setDefaultTimeout(config.nse.requestTimeout);
            await this.page.setDefaultNavigationTimeout(config.nse.requestTimeout);

            // Set download behavior
            await this.page._client.send('Page.setDownloadBehavior', {
                behavior: 'allow',
                downloadPath: this.downloadPath
            });

            logger.info('Browser initialized successfully');
        } catch (error) {
            logger.error('Failed to initialize browser:', { error: error.message });
            throw error;
        }
    }

    async downloadStockData() {
        if (!isMarketOpen()) {
            logger.info('Market is currently closed');
            return null;
        }

        try {
            logger.info('Starting stock data download process');
            
            // Use retry mechanism for navigation
            await retry(async () => {
                await this.page.goto(this.baseUrl + config.nse.marketDataEndpoint, {
                    waitUntil: 'networkidle0'
                });
            });

            logger.info('Successfully navigated to market data page');

            // Wait for and find the download link
            const downloadLink = await retry(async () => {
                await this.page.waitForSelector('a[href*="bhav"]');
                return this.page.evaluate(() => {
                    const link = document.querySelector('a[href*="bhav"]');
                    return link ? link.href : null;
                });
            });

            if (!downloadLink) {
                throw new Error('Bhavcopy download link not found');
            }

            // Download the file
            const fileName = `nse_bhavcopy_${formatDate()}.csv`;
            const filePath = path.join(this.downloadPath, fileName);

            const response = await retry(async () => {
                return axios({
                    method: 'GET',
                    url: downloadLink,
                    responseType: 'stream',
                    headers: {
                        'Referer': this.baseUrl,
                        'User-Agent': config.scraper.userAgent
                    },
                    timeout: config.nse.requestTimeout
                });
            });

            // Save the file
            const writer = fs.createWriteStream(filePath);
            response.data.pipe(writer);

            return new Promise((resolve, reject) => {
                writer.on('finish', async () => {
                    if (validateCSVData(filePath)) {
                        logger.info(`Successfully downloaded stock data to ${filePath}`);
                        resolve(filePath);
                    } else {
                        fs.unlinkSync(filePath);
                        reject(new Error('Downloaded file failed validation'));
                    }
                });
                writer.on('error', reject);
            });

        } catch (error) {
            logger.error('Error downloading stock data:', { error: error.message });
            throw error;
        }
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
            logger.info('Browser closed successfully');
        }
    }
}

// Function to run the scraper
async function runScraper() {
    const scraper = new NSEStockScraper();
    try {
        await scraper.initializeBrowser();
        await scraper.downloadStockData();
    } catch (error) {
        logger.error('Scraper run failed:', { error: error.message });
    } finally {
        await scraper.close();
    }
}

// Schedule the scraper
cron.schedule(config.schedule.cronExpression, () => {
    logger.info('Running scheduled stock data download');
    runScraper();
}, {
    timezone: config.schedule.timezone
});

// Export the scraper class
module.exports = NSEStockScraper;

// Run immediately if called directly
if (require.main === module) {
    runScraper();
}
