# Web Scraper

A Python web scraper that crawls websites starting from base URLs, discovers new URLs, and extracts text content to store in a Redis database.

## Features

- **URL Crawling**: Discovers URLs within the same domain starting from base URLs
- **Content Extraction**: Extracts clean text content and page titles
- **Redis Storage**: Stores scraped content with metadata in Redis
- **Rate Limiting**: Respectful crawling with configurable delays
- **Duplicate Detection**: Avoids re-scraping already processed URLs
- **Logging**: Comprehensive logging of the scraping process

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Redis**:
   - Install Redis server locally or use a cloud Redis service
   - Update `.env` file with your Redis connection details

3. **Add Base URLs**:
   - Edit `data/base_urls.txt` and add the starting URLs (one per line)

4. **Configure Settings**:
   - Modify `.env` file to adjust scraping parameters:
     - `MAX_PAGES_PER_DOMAIN`: Maximum pages to crawl per domain
     - `REQUEST_DELAY`: Delay between requests (in seconds)
     - `USER_AGENT`: User agent string for requests

## Usage

Run the scraper:
```bash
cd web_scraper
python -m src.main
```

The scraper will:
1. Load base URLs from `data/base_urls.txt`
2. Crawl each domain to discover URLs
3. Extract and clean text content from each page
4. Store the content in Redis with metadata

## Project Structure

```
web_scraper/
├── src/
│   ├── main.py          # Main application entry point
│   ├── crawler.py       # URL discovery and crawling
│   ├── scrapper.py      # Content extraction and scraping
│   ├── db.py           # Redis database operations
│   └── utils.py        # Utility functions
├── data/
│   └── base_urls.txt   # Input URLs
├── tests/
│   └── test_scrapper.py # Unit tests
├── requirements.txt    # Dependencies
├── .env               # Environment configuration
└── README.md          # This file
```

## Configuration

Key environment variables in `.env`:

- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `REDIS_DB`: Redis database number
- `MAX_PAGES_PER_DOMAIN`: Limit pages per domain
- `REQUEST_DELAY`: Delay between requests
- `USER_AGENT`: HTTP User-Agent header

## Redis Data Structure

- **Content**: Stored as hashes with keys like `content:<url_hash>`
- **URL Index**: Set of scraped URLs in `scraped_urls`
- **Metadata**: Includes title, content, timestamp, and content length

## Testing

Run tests:
```bash
python -m pytest tests/
```

## Notes

- The scraper respects robots.txt limitations through rate limiting
- Only crawls URLs within the same domain as the base URL
- Automatically skips already scraped URLs
- Handles errors gracefully and continues processing
- Logs all activities to both console and log file
