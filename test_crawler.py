import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log Python path and current working directory
logger.info(f"Python Path: {sys.path}")
logger.info(f"Current Working Directory: {os.getcwd()}")

# Import crawler
try:
    from src.crawlai.core.crawler import WebCrawler
except ImportError as e:
    logger.error(f"Import Error: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

async def test_crawler():
    try:
        # Test crawling a simple, safe website
        crawler = WebCrawler(
            start_url='https://www.python.org/about/',
            max_pages=3,
            depth_limit=2
        )
        
        # Perform crawling
        results = await crawler.crawl()
        
        # Basic assertions
        assert len(results) > 0, "No pages were crawled"
        assert len(results) <= 3, "Exceeded max pages limit"
        
        # Log results
        logger.info(f"Crawled {len(results)} pages")
        for result in results:
            logger.info(f"Crawled URL: {result['url']}")
        
        # Save results for manual inspection
        crawler.save_crawled_data(
            output_file='test_crawl_results.json', 
            output_dir='/home/vipin/projects/crawlai'
        )
    
    except Exception as e:
        logger.error(f"Crawler test failed: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    asyncio.run(test_crawler())
