import redis
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class RedisDB:
    """Redis database handler for fetching scraped content."""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6376)),
            decode_responses=True
        )
        
    def test_connection(self) -> bool:
        """Test Redis connection."""
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def _get_url_hash(self, url: str) -> str:
        """Generate a hash for URL to use as Redis key."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get_content(self, url: str) -> Optional[Dict]:
        """Retrieve content for a specific URL."""
        try:
            key = f"content:{self._get_url_hash(url)}"
            data = self.redis_client.hgetall(key)
            return data if data else None
        except Exception as e:
            print(f"Error retrieving content for {url}: {e}")
            return None
    
    def is_url_scraped(self, url: str) -> bool:
        """Check if URL has already been scraped."""
        return self.redis_client.sismember('scraped_urls', url)
    
    def get_all_scraped_urls(self) -> List[str]:
        """Get list of all scraped URLs."""
        return list(self.redis_client.smembers('scraped_urls'))
    
    def get_stats(self) -> Dict:
        """Get scraping statistics."""
        total_urls = self.redis_client.scard('scraped_urls')
        return {
            'total_scraped_urls': total_urls,
            'redis_memory_usage': self.redis_client.memory_usage('scraped_urls') if total_urls > 0 else 0
        }
    
    