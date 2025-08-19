import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scrapper import WebScraper
from crawler import URLCrawler
from db import RedisDB
from utils import clean_text, is_valid_url, get_domain

class TestWebScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = WebScraper()
    
    @patch('scrapper.requests.Session.get')
    def test_scrape_url_success(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.text = '<html><title>Test</title><body>Test content</body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Mock database
        self.scraper.db.is_url_scraped = Mock(return_value=False)
        self.scraper.db.store_content = Mock(return_value=True)
        
        result = self.scraper.scrape_url('http://example.com')
        self.assertTrue(result)
    
    def test_extract_content(self):
        html = '<html><title>Test Title</title><body><p>Test content here</p></body></html>'
        result = self.scraper.extract_content(html)
        
        self.assertEqual(result['title'], 'Test Title')
        self.assertIn('Test content here', result['content'])

class TestURLCrawler(unittest.TestCase):
    
    def setUp(self):
        self.crawler = URLCrawler()
    
    def test_extract_links(self):
        html = '''
        <html>
            <body>
                <a href="/page1">Page 1</a>
                <a href="https://example.com/page2">Page 2</a>
                <a href="javascript:void(0)">JS Link</a>
                <a href="mailto:test@example.com">Email</a>
            </body>
        </html>
        '''
        
        links = self.crawler.extract_links('https://example.com', html)
        
        # Should extract valid links and ignore javascript/mailto
        self.assertEqual(len(links), 2)
        self.assertIn('https://example.com/page1', links)
        self.assertIn('https://example.com/page2', links)

class TestRedisDB(unittest.TestCase):
    
    def setUp(self):
        # Mock Redis client
        with patch('db.redis.Redis') as mock_redis:
            self.mock_client = Mock()
            mock_redis.return_value = self.mock_client
            self.db = RedisDB()
    
    def test_store_content(self):
        self.mock_client.hset.return_value = True
        self.mock_client.sadd.return_value = True
        
        result = self.db.store_content('http://example.com', 'Test content', 'Test Title')
        self.assertTrue(result)
        
        # Verify Redis operations were called
        self.mock_client.hset.assert_called_once()
        self.mock_client.sadd.assert_called_once_with('scraped_urls', 'http://example.com')
    
    def test_is_url_scraped(self):
        self.mock_client.sismember.return_value = True
        
        result = self.db.is_url_scraped('http://example.com')
        self.assertTrue(result)
        
        self.mock_client.sismember.assert_called_once_with('scraped_urls', 'http://example.com')

class TestUtils(unittest.TestCase):
    
    def test_clean_text(self):
        dirty_text = "  This   is    \n\n  messy   text!  \t\t  "
        clean = clean_text(dirty_text)
        self.assertEqual(clean, "This is messy text!")
    
    def test_is_valid_url(self):
        self.assertTrue(is_valid_url('https://example.com'))
        self.assertTrue(is_valid_url('http://test.org/path'))
        self.assertFalse(is_valid_url('not-a-url'))
        self.assertFalse(is_valid_url('javascript:void(0)'))
    
    def test_get_domain(self):
        self.assertEqual(get_domain('https://example.com/path'), 'example.com')
        self.assertEqual(get_domain('http://test.org:8080'), 'test.org:8080')
        self.assertIsNone(get_domain('not-a-url'))

if __name__ == '__main__':
    unittest.main()
    