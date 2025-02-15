import os
import time
import json
import logging
import requests
from typing import List, Dict, Optional

from ..models.extraction_schema import DocumentationExtractionDetails
from ..utils.rate_limiter import GroqRateLimiter
from .base_extractor import BaseExtractor

class LLMExtractor(BaseExtractor):
    """
    LLM-based content extraction strategy
    """
    def __init__(
        self, 
        model: str = 'qwen-2.5-32b',
        api_key: Optional[str] = None,
        base_url: str = 'https://api.groq.com/openai/v1',
        max_retries: int = 5,
        timeout: int = 30,
        backoff_factor: float = 1.5
    ):
        """
        Initialize LLM extractor
        
        Args:
            model (str): LLM model to use
            api_key (str, optional): API key
            base_url (str): Base URL for API
            max_retries (int): Number of retry attempts
            timeout (int): Request timeout
            backoff_factor (float): Exponential backoff multiplier
        """
        self.logger = logging.getLogger(__name__)
        
        # Prioritize passed API key, then environment variable
        self.api_key = api_key or os.environ.get('GROQ_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided")
        
        self.model = model
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        
        # Initialize rate limiter
        self.rate_limiter = GroqRateLimiter()
    
    def _compact_html_extraction(self, url: str, html: str) -> str:
        """
        Create a compact extraction prompt
        
        Args:
            url (str): Source URL
            html (str): HTML content
        
        Returns:
            str: Compact extraction prompt
        """
        # Truncate HTML to prevent overwhelming the model
        truncated_html = html[:4000]  # Reduced from 8000
        
        # More concise prompt
        return f"""Extract key technical details from {url}:

HTML:
{truncated_html}

INSTRUCTIONS:
1. Provide technical content summary
2. Focus on: purpose, features, code/config
3. Use JSON schema:
   {{
     "section_name": str,
     "description": str,
     "key_features": [str],
     "code_examples": [str],
     "configuration_options": {{str: str}}
   }}
4. Minimal/empty if no details
5. Technical, actionable info"""
    
    def extract(
        self, 
        url: str, 
        html: str, 
        **kwargs
    ) -> List[Dict[str, str]]:
        """
        Extract content from technical documentation
        
        Args:
            url (str): Source URL
            html (str): HTML content
            **kwargs: Additional arguments
        
        Returns:
            List of extracted content dictionaries
        """
        # Prepare extraction prompt
        prompt = self._compact_html_extraction(url, html)
        
        # Estimate token count
        estimated_tokens = len(prompt) // 4
        
        # Wait if needed to respect rate limits
        self.rate_limiter.wait_if_needed(token_count=estimated_tokens)
        
        # Prepare API request payload
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system', 
                    'content': 'You are a precise technical documentation extractor. Respond with a valid, compact JSON.'
                },
                {
                    'role': 'user', 
                    'content': prompt
                }
            ],
            'response_format': {'type': 'json_object'},
            'temperature': 0.1,  # Very deterministic
            'max_tokens': 512,
            'top_p': 0.9
        }
        
        # Retry mechanism with exponential backoff
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f'{self.base_url}/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json=payload,
                    timeout=self.timeout
                )
                
                # Check response
                if response.status_code == 429:  # Rate limit error
                    wait_time = (self.backoff_factor ** attempt)
                    self.logger.warning(f"Rate limited. Waiting {wait_time:.2f}s (Attempt {attempt + 1})")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code != 200:
                    self.logger.error(f"Extraction error for {url}: {response.text}")
                    return [{'content': 'API request failed'}]
                
                # Parse response
                result = response.json()
                content_text = result['choices'][0]['message']['content'].strip()
                
                # Validate and process extraction
                validated_result = self._validate_extraction([{
                    'content': content_text
                }])
                
                return validated_result
            
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request attempt {attempt + 1} failed: {e}")
                wait_time = (self.backoff_factor ** attempt)
                time.sleep(wait_time)
                
                if attempt == self.max_retries - 1:
                    return [{'content': f'Extraction failed after {self.max_retries} attempts'}]
        
        return [{'content': 'Unexpected extraction failure'}]
