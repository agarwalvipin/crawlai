import asyncio
import json
import argparse
import logging
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UpstoxCrawler:
    def __init__(self, start_url: str, max_pages: int = 20):
        """
        Initialize the Upstox web crawler
        
        Args:
            start_url (str): Initial URL to start crawling
            max_pages (int): Maximum number of pages to crawl
        """
        self.start_url = start_url
        self.max_pages = max_pages
        self.crawled_urls = set()
        self.crawled_data = []
        logger.info(f"Crawler initialized with start_url: {start_url}, max_pages: {max_pages}")
    
    async def crawl(self):
        """
        Asynchronously crawl the Upstox developer documentation
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                # Navigate to the initial URL
                base_url = "https://upstox.com/developer/api-documentation"
                initial_link = base_url + self.start_url
                
                logger.info(f"Navigating to initial link: {initial_link}")
                await page.goto(initial_link, wait_until='networkidle')
                
                # Check if page loaded successfully
                current_url = page.url
                logger.info(f"Current page URL: {current_url}")
                
                # Extract page content
                content = await page.content()
                title = await page.title()
                
                logger.info(f"Page title: {title}")
                logger.info(f"Content length: {len(content)} characters")
                
                # Save initial page data
                self.crawled_data.append({
                    'url': initial_link,
                    'title': title,
                    'content': content
                })
                self.crawled_urls.add(initial_link)
                
                # Extract links
                links = await page.evaluate("""
                    () => {
                        const links = Array.from(document.querySelectorAll('a'));
                        return links
                            .filter(link => link.href.includes('/developer/api-documentation/'))
                            .map(link => link.href);
                    }
                """)
                
                logger.info(f"Found {len(links)} potential links to crawl")
                
                # Follow links with depth limit
                for link in links[:self.max_pages]:
                    if link not in self.crawled_urls:
                        try:
                            logger.info(f"Navigating to link: {link}")
                            await page.goto(link, wait_until='networkidle')
                            
                            # Extract page content
                            content = await page.content()
                            title = await page.title()
                            
                            logger.info(f"Crawled page: {link}")
                            logger.info(f"Page title: {title}")
                            logger.info(f"Content length: {len(content)} characters")
                            
                            # Save page data
                            self.crawled_data.append({
                                'url': link,
                                'title': title,
                                'content': content
                            })
                            self.crawled_urls.add(link)
                            
                            # Break if max pages reached
                            if len(self.crawled_urls) >= self.max_pages:
                                logger.info(f"Reached maximum pages: {self.max_pages}")
                                break
                        
                        except Exception as e:
                            logger.error(f"Error crawling {link}: {e}")
                
            except Exception as e:
                logger.error(f"Crawling error: {e}")
            
            finally:
                await browser.close()
        
        # Save results
        with open('crawled_data.json', 'w') as f:
            json.dump(self.crawled_data, f, indent=2)
        
        logger.info(f"Crawled {len(self.crawled_data)} pages")
        return self.crawled_data

def main():
    parser = argparse.ArgumentParser(description='Advanced Web Crawler for Upstox Developer Documentation')
    parser.add_argument('--url', default='/open-api/', help='Starting URL path')
    parser.add_argument('--max-pages', type=int, default=20, help='Maximum number of pages to crawl')
    
    args = parser.parse_args()
    
    crawler = UpstoxCrawler(start_url=args.url, max_pages=args.max_pages)
    asyncio.run(crawler.crawl())

if __name__ == "__main__":
    main()
