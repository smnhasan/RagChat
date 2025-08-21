# News Scraper for Reporter Chatbot

A Python-based web scraper designed to power a **News Reporter Chatbot**. The scraper crawls verified news websites, extracts articles, and stores them in a Redis database. This enables the chatbot to answer user queries about recent events and verify rumors or social media claims with reliable sources.

## Features

* **Focused URL Crawling**: Crawls only trusted news domains starting from predefined base URLs.
* **Verified Content Extraction**: Extracts clean article text, headlines, and publication details.
* **Redis Integration**: Stores articles with metadata for fast retrieval by the chatbot.
* **Duplicate Prevention**: Skips already scraped URLs to avoid redundant storage.
* **Rate Limiting**: Configurable delay between requests to ensure respectful crawling.
* **Comprehensive Logging**: Tracks crawling, scraping, and storage activities.

## Project Structure

```
.scrapper/
├── data/
│   └── base_urls.txt       # List of news source URLs
├── dump.rdb                # Redis database file
├── README.md               # This file
├── redis/
│   └── dump.rdb            # Redis persistence file
├── requirements.txt        # Python dependencies
├── run_scrapper.log        # Log file for run.sh
├── run.sh                  # Bash script to run the scraper
├── scraper.log             # Scraper activity log
├── src/
│   ├── crawler.py          # URL discovery and crawling
│   ├── db.py               # Redis database operations
│   ├── __init__.py
│   ├── main.py             # Main entry point
│   ├── scrapper.py         # Article extraction and cleaning
│   └── utils.py            # Utility functions
└── tests/
    └── test_scrapper.py    # Unit tests
```

## Setup

### 1. Create Python Environment

Create a Conda environment with Python 3.10.13:

```bash
conda create -n scrapper-env python=3.10.13 -y
conda activate scrapper-env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Redis

* Install Redis locally or use a cloud Redis service.
* Ensure Redis is running and accessible.
* Default Redis persistence file is stored at `redis/dump.rdb`.

### 4. Add Trusted News Sources

Edit `data/base_urls.txt` and list the base URLs of news websites to scrape, one URL per line.

### 5. Configure Settings (Optional)

You can adjust scraping parameters in the `.env` file if available:

* `MAX_PAGES_PER_DOMAIN` → Maximum articles per domain
* `REQUEST_DELAY` → Delay between requests (seconds)
* `USER_AGENT` → HTTP User-Agent header

---

## Usage

### Run Scraper via Bash Script

The `run.sh` script will activate the environment, run the scraper, and log output:

```bash
bash run.sh
```

This will:

1. Load base URLs from `data/base_urls.txt`
2. Crawl each domain to discover new URLs
3. Extract and clean article text and metadata
4. Store articles in Redis
5. Log scraping activity to `scraper.log` and `run_scrapper.log`

### Run Directly with Python

```bash
cd src
python main.py
```

---

## Redis Data Structure

* **Articles**: Stored as hashes with keys like `news:<url_hash>`
* **Scraped URL Index**: Set `scraped_urls` stores all processed URLs
* **Metadata**: Includes headline, content, source, timestamp, and length

---

## Testing

Run unit tests:

```bash
pytest tests/
```

---

## Notes

* Only crawls **trusted news domains** listed in `base_urls.txt`.
* Automatically skips duplicate URLs.
* Handles errors gracefully without stopping the scraping process.
* Respects rate limits to avoid overwhelming servers.
* Provides structured and reliable data for the **News Reporter Chatbot**.

