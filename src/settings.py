BOT_NAME = 'immovlan'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Delay settings
DOWNLOAD_DELAY = 1  
RANDOMIZE_DOWNLOAD_DELAY = True

# Concurrent requests
CONCURRENT_REQUESTS = 16  # Async crawling
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Pipelines
ITEM_PIPELINES = {
    'src.pipelines.ImmovlanPipeline': 300,
}

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'src.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Feed export default
FEED_EXPORT_ENCODING = 'utf-8'
FEED_FORMAT = 'csv'
FEED_URI = 'output/properties_data.csv'

# Error log file
LOG_FILE = 'logs/scrapy.log'

