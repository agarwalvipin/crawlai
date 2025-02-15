# Crawl4AI: Advanced LLM-Friendly Web Crawler & Scraper

## Overview

Crawl4AI is a powerful, flexible web crawling and scraping library designed to be highly compatible with Large Language Models (LLMs). It provides advanced extraction strategies, robust rate limiting, and easy configuration.

## Features

- 🌐 Multi-strategy Web Crawling
- 🤖 LLM-Friendly Content Extraction
- 📊 Configurable Crawling Parameters
- 🔒 Advanced Rate Limiting
- 🔍 Flexible Extraction Strategies

## Installation

```bash
pip install crawlai
```

## Quick Start

```python
from crawlai import WebCrawler

# Basic crawling
crawler = WebCrawler(
    start_url='https://docs.example.com',
    max_pages=10,
    extraction_strategy='llm'
)

# Crawl and save results
crawler.crawl()
crawler.save_crawled_data('output.json')
```

## Command Line Usage

```bash
# Crawl a website
crawlai --start-url https://docs.example.com \
        --max-pages 20 \
        --extraction-strategy llm \
        --output-file docs.json
```

## Configuration

### Environment Variables

- `GROQ_KEY`: API key for Groq LLM
- `OLLAMA_HOST`: Ollama server host

### Supported Extractors

- LLM-based Extraction
- CSS Selector Extraction
- XPath Extraction

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Contact

Vipin Agarwal - vipin@example.com
