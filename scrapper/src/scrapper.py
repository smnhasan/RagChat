import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import time
import os
from dotenv import load_dotenv
from .utils import clean_text, setup_logging, rate_limit
from .db import RedisDB

load_dotenv()

class WebScraper:
    """Scrapes web pages and extracts text content."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (compatible; WebScraper/1.0)')
        })
        self.request_delay = float(os.getenv('REQUEST_DELAY', 1))
        self.db = RedisDB()
        self.logger = setup_logging()
        
    @rate_limit(1)
    def _fetch_page(self, url: str) -> requests.Response:
        """Fetch a single page with rate limiting."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            raise
    
    def extract_content(self, html_content: str) -> Dict[str, str]:
        """Extract title and text content from HTML."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title_tag = soup.find('title')
            title = clean_text(title_tag.get_text()) if title_tag else ""
            
            # Extract main content
            # Try to find main content areas first
            content_selectors = [
                'main', 'article', '.content', '.post', '.entry',
                '.main-content', '#content', '#main'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text()
                    break
            
            # If no specific content area found, use body
            if not content_text:
                body = soup.find('body')
                content_text = body.get_text() if body else soup.get_text()
            
            # Clean the extracted content
            clean_content = clean_text(content_text)
            
            return {
                'title': title,
                'content': clean_content
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting content: {e}")
            return {'title': '', 'content': ''}
    
    def scrape_url(self, url: str) -> bool:
        """Scrape a single URL and store in database."""
        # Check if already scraped
        if self.db.is_url_scraped(url):
            self.logger.info(f"URL already scraped: {url}")
            return True
        
        try:
            self.logger.info(f"Scraping: {url}")
            
            # Fetch the page
            response = self._fetch_page(url)
            
            # Extract content
            extracted = self.extract_content(response.text)
            
            # Store in database
            success = self.db.store_content(
                url=url,
                content=extracted['content'],
                title=extracted['title']
            )
            
            if success:
                self.logger.info(f"Successfully scraped and stored: {url}")
            else:
                self.logger.error(f"Failed to store content for: {url}")
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to scrape {url}: {e}")
            return False
    
    def scrape_urls(self, urls: list) -> Dict[str, int]:
        """Scrape multiple URLs."""
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        self.logger.info(f"Starting to scrape {len(urls)} URLs")
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Progress: {i}/{len(urls)}")
            
            if self.db.is_url_scraped(url):
                stats['skipped'] += 1
                continue
                
            success = self.scrape_url(url)
            if success:
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        self.logger.info(f"Scraping completed. Stats: {stats}")
        return stats
    