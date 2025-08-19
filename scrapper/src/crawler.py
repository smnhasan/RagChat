import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, List
import time
import os
from dotenv import load_dotenv
from .utils import is_valid_url, get_domain, normalize_url, rate_limit, setup_logging

load_dotenv()

class URLCrawler:
    """Crawls websites to discover URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (compatible; WebScraper/1.0)')
        })
        self.max_pages_per_domain = int(os.getenv('MAX_PAGES_PER_DOMAIN', 50))
        self.request_delay = float(os.getenv('REQUEST_DELAY', 1))
        self.logger = setup_logging()
        
    @rate_limit(1)  # Basic rate limiting
    def _fetch_page(self, url: str) -> requests.Response:
        """Fetch a single page with rate limiting."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            raise
    
    def extract_links(self, url: str, html_content: str) -> Set[str]:
        """Extract all valid links from HTML content."""
        links = set()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all anchor tags with href attributes
            for link in soup.find_all('a', href=True):
                href = link['href'].strip()
                
                # Skip empty hrefs, javascript, mailto, etc.
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue
                
                # Normalize the URL
                absolute_url = normalize_url(href, url)
                
                # Validate the URL
                if is_valid_url(absolute_url):
                    links.add(absolute_url)
        
        except Exception as e:
            self.logger.error(f"Error extracting links from {url}: {e}")
        
        return links
    
    def crawl_domain(self, base_url: str) -> Set[str]:
        """Crawl a domain starting from base URL."""
        discovered_urls = set()
        to_visit = {base_url}
        visited = set()
        domain = get_domain(base_url)
        
        self.logger.info(f"Starting crawl of domain: {domain}")
        
        while to_visit and len(discovered_urls) < self.max_pages_per_domain:
            current_url = to_visit.pop()
            
            if current_url in visited:
                continue
                
            # Only crawl URLs from the same domain
            if get_domain(current_url) != domain:
                continue
            
            try:
                self.logger.info(f"Crawling: {current_url}")
                response = self._fetch_page(current_url)
                visited.add(current_url)
                discovered_urls.add(current_url)
                
                # Extract links from the page
                new_links = self.extract_links(current_url, response.text)
                
                # Add new links to visit queue (same domain only)
                for link in new_links:
                    if (get_domain(link) == domain and 
                        link not in visited and 
                        link not in to_visit):
                        to_visit.add(link)
                
                # Respect rate limiting
                time.sleep(self.request_delay)
                
            except Exception as e:
                self.logger.error(f"Failed to crawl {current_url}: {e}")
                visited.add(current_url)  # Mark as visited to avoid retry
                continue
        
        self.logger.info(f"Crawling completed. Discovered {len(discovered_urls)} URLs for {domain}")
        return discovered_urls
    
    def crawl_multiple_domains(self, base_urls: List[str]) -> Set[str]:
        """Crawl multiple domains."""
        all_urls = set()
        
        for base_url in base_urls:
            try:
                urls = self.crawl_domain(base_url)
                all_urls.update(urls)
            except Exception as e:
                self.logger.error(f"Failed to crawl domain {base_url}: {e}")
        
        return all_urls
