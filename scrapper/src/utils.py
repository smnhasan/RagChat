import re
import time
import logging
from urllib.parse import urljoin, urlparse
from typing import Optional, Set

def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:]', '', text)
    
    return text

def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        return urlparse(url).netloc
    except:
        return None

def normalize_url(url: str, base_url: str) -> str:
    """Normalize and resolve relative URLs."""
    return urljoin(base_url, url)

def rate_limit(delay: float):
    """Simple rate limiting decorator."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator
