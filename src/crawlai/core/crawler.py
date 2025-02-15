import os
import json
import logging
import asyncio
from typing import List, Dict, Optional, Union
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

from ..extractors.base_extractor import BaseExtractor
from ..extractors.llm_extractor import LLMExtractor

class WebCrawler:
    """
    Advanced async web crawler with flexible extraction strategies
    """
    def __init__(
        self, 
        start_url: str, 
        max_pages: int = 10,
        extraction_strategy: str = 'llm',
        extractor: Optional[BaseExtractor] = None,
        allowed_domains: Optional[List[str]] = None,
        depth_limit: int = 3,
        timeout: int = 30,
        user_agent: str = 'CrawlAI/0.1.0'
    ):
        """
        Initialize web crawler
        
        Args:
            start_url (str): Initial URL to start crawling
            max_pages (int): Maximum number of pages to crawl
            extraction_strategy (str): Content extraction strategy
            extractor (BaseExtractor, optional): Custom extractor
            allowed_domains (List[str], optional): Domains to restrict crawling
            depth_limit (int): Maximum crawl depth
            timeout (int): Request timeout
            user_agent (str): User agent for requests
        """
        self.logger = logging.getLogger(__name__)
        
        self.start_url = start_url
        self.max_pages = max_pages
        self.extraction_strategy = extraction_strategy
        self.depth_limit = depth_limit
        self.timeout = timeout
        
        # Set allowed domains
        self.allowed_domains = allowed_domains or [
            urlparse(start_url).netloc
        ]
        
        # Set up extractor
        self.extractor = extractor or LLMExtractor()
        
        # Tracking
        self.crawled_urls = set()
        self.crawled_data = []
        
        # Request headers
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and allowed
        
        Args:
            url (str): URL to validate
        
        Returns:
            bool: Whether URL is valid and allowed
        """
        try:
            parsed_url = urlparse(url)
            return (
                parsed_url.scheme in ['http', 'https'] and
                any(domain in parsed_url.netloc for domain in self.allowed_domains) and
                url not in self.crawled_urls
            )
        except Exception:
            return False
    
    async def _extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract links from HTML
        
        Args:
            html (str): HTML content
            base_url (str): Base URL for resolving relative links
        
        Returns:
            List of extracted links
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html)
            
            # Extract links
            links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a'))
                    .map(a => a.href)
                    .filter(href => href && href.startsWith('http'))
            }''')
            
            await browser.close()
            
            # Resolve and filter links
            resolved_links = [
                urljoin(base_url, link) 
                for link in links 
                if self._is_valid_url(urljoin(base_url, link))
            ]
            
            return list(set(resolved_links))
    
    async def crawl(self) -> List[Dict[str, Union[str, Dict]]]:
        """
        Perform web crawling
        
        Returns:
            List of crawled page data
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Start crawling
            queue = [(self.start_url, 0)]
            
            while queue and len(self.crawled_urls) < self.max_pages:
                current_url, depth = queue.pop(0)
                
                if current_url in self.crawled_urls or depth > self.depth_limit:
                    continue
                
                try:
                    # Navigate to page
                    await page.goto(current_url, timeout=self.timeout * 1000)
                    
                    # Get page content
                    html_content = await page.content()
                    title = await page.title()
                    
                    # Extract content
                    extracted_content = self.extractor.extract(
                        url=current_url, 
                        html=html_content
                    )
                    
                    # Record crawled data
                    crawl_result = {
                        'url': current_url,
                        'title': title,
                        'content': extracted_content
                    }
                    
                    self.crawled_data.append(crawl_result)
                    self.crawled_urls.add(current_url)
                    
                    # Extract and queue new links
                    new_links = await self._extract_links(html_content, current_url)
                    queue.extend(
                        (link, depth + 1) 
                        for link in new_links 
                        if link not in self.crawled_urls
                    )
                    
                    self.logger.info(f"Crawled page: {current_url}")
                
                except Exception as e:
                    self.logger.error(f"Error crawling {current_url}: {e}")
            
            await browser.close()
        
        return self.crawled_data
    
    def save_crawled_data(
        self, 
        output_file: str = 'crawled_data.json', 
        output_dir: Optional[str] = None
    ):
        """
        Save crawled data to a JSON file
        
        Args:
            output_file (str): Name of output file
            output_dir (str, optional): Directory to save file
        """
        # Determine full output path
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            full_path = os.path.join(output_dir, output_file)
        else:
            full_path = output_file
        
        # Save data
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(self.crawled_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Crawled data saved to {full_path}")
        self.logger.info(f"Total pages crawled: {len(self.crawled_urls)}")
