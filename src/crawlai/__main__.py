import os
import sys
import argparse
import asyncio
import logging
from typing import Optional

from .core.crawler import WebCrawler
from .extractors.llm_extractor import LLMExtractor

def configure_logging(verbose: bool = False):
    """
    Configure logging for the application
    
    Args:
        verbose (bool): Enable verbose logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('crawlai.log', encoding='utf-8')
        ]
    )

async def async_main(args):
    """
    Async main function to run the crawler
    
    Args:
        args (argparse.Namespace): Parsed command-line arguments
    """
    logger = logging.getLogger(__name__)

    try:
        # Validate and set API key
        api_key = args.api_key or os.environ.get('GROQ_KEY')
        if not api_key and 'groq' in args.provider:
            logger.error("Groq API key is required but not provided")
            sys.exit(1)
        
        # Create extractor
        extractor = LLMExtractor(
            model=args.provider.split('/')[-1],
            api_key=api_key
        )
        
        # Initialize crawler
        crawler = WebCrawler(
            start_url=args.start_url,
            max_pages=args.max_pages,
            depth_limit=args.depth_limit,
            extraction_strategy=args.extraction_strategy,
            extractor=extractor
        )
        
        # Run crawler
        await crawler.crawl()
        
        # Save crawled data
        crawler.save_crawled_data(
            output_file=args.output_file,
            output_dir=args.output_dir
        )
    
    except Exception as e:
        logger.error(f"Crawling failed: {e}")
        sys.exit(1)

def main():
    """
    Main entry point for Crawl4AI
    """
    parser = argparse.ArgumentParser(description='Crawl4AI: Advanced Web Crawler')
    
    # Crawler configuration
    parser.add_argument(
        '--start-url', 
        type=str, 
        required=True, 
        help='Starting URL for the crawler'
    )
    parser.add_argument(
        '--max-pages', 
        type=int, 
        default=10, 
        help='Maximum number of pages to crawl'
    )
    parser.add_argument(
        '--depth-limit', 
        type=int, 
        default=3, 
        help='Maximum crawl depth'
    )
    
    # Extraction strategy
    parser.add_argument(
        '--extraction-strategy', 
        type=str, 
        default='llm', 
        choices=['llm', 'css', 'xpath'], 
        help='Content extraction strategy'
    )
    
    # LLM configuration
    parser.add_argument(
        '--provider', 
        type=str, 
        default='groq/qwen-2.5-32b', 
        help='LLM provider and model'
    )
    parser.add_argument(
        '--api-key', 
        type=str, 
        help='API key for LLM provider'
    )
    
    # Output configuration
    parser.add_argument(
        '--output-file', 
        type=str, 
        default='crawled_data.json', 
        help='Output file for crawled data'
    )
    parser.add_argument(
        '--output-dir', 
        type=str, 
        help='Directory to save output file'
    )
    
    # Logging
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Enable verbose logging'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Configure logging
    configure_logging(args.verbose)
    
    # Run async main
    asyncio.run(async_main(args))

if __name__ == '__main__':
    main()
