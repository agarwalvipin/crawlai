import time
import logging
from collections import deque
from threading import Lock
from typing import Optional

class GroqRateLimiter:
    """
    Advanced rate limiter for Groq API with multi-dimensional tracking
    
    Supports:
    - Requests per Minute (RPM)
    - Tokens per Minute (TPM)
    - Requests per Day (RPD)
    - Tokens per Day (TPD)
    """
    def __init__(
        self, 
        rpm_limit: int = 300,  # Default 300 requests per minute
        tpm_limit: int = 6000,  # Default 6000 tokens per minute
        rpd_limit: int = 10000,  # Default 10000 requests per day
        tpd_limit: int = 200000,  # Default 200000 tokens per day
        safety_margin: float = 0.9,  # 90% of limit to provide buffer
        pruning_interval: int = 60  # Prune old records every 60 seconds
    ):
        """
        Initialize rate limiter with configurable limits
        
        Args:
            rpm_limit (int): Requests per minute limit
            tpm_limit (int): Tokens per minute limit
            rpd_limit (int): Requests per day limit
            tpd_limit (int): Tokens per day limit
            safety_margin (float): Percentage of limit to use
            pruning_interval (int): Interval for pruning old records
        """
        self.logger = logging.getLogger(__name__)
        
        self.rpm_limit = int(rpm_limit * safety_margin)
        self.tpm_limit = int(tpm_limit * safety_margin)
        self.rpd_limit = int(rpd_limit * safety_margin)
        self.tpd_limit = int(tpd_limit * safety_margin)
        
        self.requests_minute = deque()
        self.tokens_minute = deque()
        self.requests_day = deque()
        self.tokens_day = deque()
        
        self.lock = Lock()
        self.last_pruned = time.time()
    
    def _prune_old_records(self, current_time: float):
        """
        Remove records older than 1 minute/day
        
        Args:
            current_time (float): Current timestamp
        """
        # Prune minute-based records
        while self.requests_minute and current_time - self.requests_minute[0] > 60:
            self.requests_minute.popleft()
        
        while self.tokens_minute and current_time - self.tokens_minute[0][0] > 60:
            self.tokens_minute.popleft()
        
        # Prune day-based records
        while self.requests_day and current_time - self.requests_day[0] > 86400:
            self.requests_day.popleft()
        
        while self.tokens_day and current_time - self.tokens_day[0][0] > 86400:
            self.tokens_day.popleft()
    
    def wait_if_needed(
        self, 
        token_count: int = 1, 
        request_count: int = 1, 
        timeout: int = 300  # 5-minute maximum wait
    ) -> bool:
        """
        Wait if rate limits would be exceeded
        
        Args:
            token_count (int): Number of tokens in the request
            request_count (int): Number of requests
            timeout (int): Maximum wait time in seconds
        
        Returns:
            bool: Whether waiting was successful
        """
        current_time = time.time()
        
        with self.lock:
            # Periodic pruning of old records
            if current_time - self.last_pruned > 60:
                self._prune_old_records(current_time)
                self.last_pruned = current_time
            
            # Check minute-based limits
            requests_in_minute = len(self.requests_minute)
            tokens_in_minute = sum(t[1] for t in self.tokens_minute)
            
            # Check day-based limits
            requests_in_day = len(self.requests_day)
            tokens_in_day = sum(t[1] for t in self.tokens_day)
            
            # Determine if waiting is needed
            wait_needed = (
                requests_in_minute + request_count > self.rpm_limit or
                tokens_in_minute + token_count > self.tpm_limit or
                requests_in_day + request_count > self.rpd_limit or
                tokens_in_day + token_count > self.tpd_limit
            )
            
            if wait_needed:
                # Calculate potential wait time
                wait_time = 60 if requests_in_minute >= self.rpm_limit else 1
                wait_time = min(wait_time, timeout)
                
                self.logger.warning(
                    f"Rate limit approaching. Waiting {wait_time}s. "
                    f"Current: RPM={requests_in_minute}, TPM={tokens_in_minute}, "
                    f"RPD={requests_in_day}, TPD={tokens_in_day}"
                )
                
                time.sleep(wait_time)
                current_time = time.time()
            
            # Record the request
            self.requests_minute.append(current_time)
            self.requests_day.append(current_time)
            
            self.tokens_minute.append((current_time, token_count))
            self.tokens_day.append((current_time, token_count))
        
        return True
