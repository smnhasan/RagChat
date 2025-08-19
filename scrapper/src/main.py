import os
import sys
from pathlib import Path
from .crawler import URLCrawler
from .scrapper import WebScraper
from .db import RedisDB
from .utils import setup_logging

def load_base_urls(file_path: str = "data/base_urls.txt") -> list:
    """Load base URLs from file."""
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith('#'):
                    urls.append(url)
    except FileNotFoundError:
        print(f"Base URLs file not found: {file_path}")
        return []
    
    return urls

def main():
    """Main function to run the web scraper."""
    logger = setup_logging()
    
    # Initialize components
    db = RedisDB()
    crawler = URLCrawler()
    scraper = WebScraper()
    
    # Test Redis connection
    if not db.test_connection():
        logger.error("Failed to connect to Redis. Please check your configuration.")
        return
    
    logger.info("Starting web scraper...")
    
    # Load base URLs
    base_urls = load_base_urls()
    if not base_urls:
        logger.error("No base URLs found. Please add URLs to data/base_urls.txt")
        return
    
    logger.info(f"Loaded {len(base_urls)} base URLs")
    
    # Crawl URLs
    logger.info("Phase 1: Crawling URLs...")
    discovered_urls = crawler.crawl_multiple_domains(base_urls)
    logger.info(f"Discovered {len(discovered_urls)} URLs to scrape")
    
    # Scrape content
    logger.info("Phase 2: Scraping content...")
    stats = scraper.scrape_urls(list(discovered_urls))
    
    # Print final statistics
    db_stats = db.get_stats()
    logger.info("=== SCRAPING COMPLETED ===")
    logger.info(f"URLs discovered: {len(discovered_urls)}")
    logger.info(f"Successfully scraped: {stats['success']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info(f"Skipped (already scraped): {stats['skipped']}")
    logger.info(f"Total URLs in database: {db_stats['total_scraped_urls']}")

if __name__ == "__main__":
    main()
    