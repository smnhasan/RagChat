# News Reporter AI

A complete **News Reporter AI** system that verifies news and rumors using trusted sources. It consists of three main components:

1. **Backend** – Handles query processing, information retrieval, and response generation using a Retrieval-Augmented Generation (RAG) pipeline.
2. **Frontend** – Modern, responsive chatbot interface for interacting with users and displaying verified news.
3. **Scraper** – Crawls verified news websites, extracts articles, and stores them in Redis to feed the backend’s knowledge base.

---

## Project Features

* ✅ **Real-Time News Verification** – Ask about recent events or rumors and receive verified information from credible sources.
* ✅ **RAG Pipeline** – Combines retrieved news content with AI language models for accurate responses.
* ✅ **Streaming Responses** – Token-by-token streaming for a smooth, interactive chat experience.
* ✅ **Scalable Architecture** – Backend built with FastAPI, frontend with Next.js, and Redis/ChromaDB for caching and vector storage.
* ✅ **News Scraping Automation** – Scraper continuously collects and updates news articles from trusted sources.
* ✅ **Responsive UI** – Mobile-friendly chat interface built with React, Next.js, and Tailwind CSS.
* ✅ **Logging & Monitoring** – Logs maintained for backend, frontend, and scraper to track activity and errors.

---

## Project Structure

```
root/
├── backend/     # FastAPI backend (RAG pipeline)
├── frontend/    # Next.js frontend chatbot interface
└── scrapper/    # Python scraper for collecting news articles
```

---

## Installation & Setup

Each stack has separate setup instructions. You can run them independently or together.

---

### 1. Backend

#### Prerequisites

* Python 3.10.13
* Conda (recommended)

#### Setup

```bash
cd backend
conda create -n backend-env python=3.10.13
conda activate backend-env
pip install -r requirements.txt
```

#### Configure Environment

* Copy `config.py` to `.env` or set environment variables. Example:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
CHROMA_DB_PATH=./app/api/rag/db/knowledge_base
```

#### Run Backend

```bash
bash run.sh
# or
uvicorn main:app --host 0.0.0.0 --port 8000
```

* **Endpoints**:

  * `/api/chat` – Send user queries for news verification
  * `/api/health` – Health check

---

### 2. Frontend

#### Prerequisites

* Node.js 18+
* npm or yarn

#### Setup

```bash
cd frontend
npm install
# or
yarn install
```

#### Configure Environment

```bash
cp .env.example .env.local
```

* Set backend API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Run Frontend

```bash
npm run dev
# or
yarn dev
```

* Open [http://localhost:3000](http://localhost:3000) in your browser.

---

### 3. Scraper

#### Prerequisites

* Python 3.10.13
* Conda

#### Setup

```bash
cd scrapper
conda create -n scrapper-env python=3.10.13
conda activate scrapper-env
pip install -r requirements.txt
```

#### Configure Data

* Add trusted news URLs to `data/base_urls.txt`
* Ensure Redis is running for storage

#### Run Scraper

```bash
bash run.sh
# or
python src/main.py
```

---

## Notes

* Backend must be running for frontend to work properly.
* Scraper continuously updates the knowledge base for accurate responses.
* Logs are maintained separately for backend (`logs/`), frontend (`.next/`), and scraper (`scraper.log`).
* Each stack can be deployed independently (e.g., backend on a server, frontend on Vercel).
