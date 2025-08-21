# News Reporter AI Backend

## Overview

The News Reporter AI Backend is the server-side component of the News Reporter AI project, designed to power a Retrieval-Augmented Generation (RAG) system for verifying news and rumors. This backend integrates advanced AI models to retrieve information from credible sources, process queries, and stream accurate responses to the frontend. Built with Python and FastAPI, it provides a robust and scalable API for real-time news verification.

## Project Structure

```
backend/
├── app/                      # Core application code
│   ├── api/                  # API endpoints and RAG logic
│   │   ├── chat.py           # Chat endpoint for streaming responses
│   │   ├── health.py         # Health check endpoint
│   │   ├── rag/              # RAG-specific components
│   │   │   ├── db/           # Database and vector store
│   │   │   │   ├── knowledge_base/  # ChromaDB storage
│   │   │   │   ├── redis_client.py # Redis client for caching
│   │   │   │   └── vectorstore.py  # Vector store management
│   │   │   ├── ingestor.py   # Data ingestion for knowledge base
│   │   │   ├── models/       # AI models
│   │   │   │   ├── embedding_model.py  # Embedding model
│   │   │   │   └── llm.py    # Language model
│   │   │   ├── pipeline.py   # RAG pipeline logic
│   │   │   ├── prompts.py    # Prompt templates
│   │   │   └── retriever.py  # Information retrieval
│   ├── __init__.py           # Package initialization
│   └── __pycache__/          # Compiled Python files
├── config.py                 # Configuration settings
├── cookbook/                 # Notebooks and scripts for testing
│   ├── models_test.ipynb     # Model testing notebook
│   ├── streaming_test.py     # Streaming response tests
│   └── websocket_test.py     # WebSocket tests
├── logs/                     # Log files
│   ├── access.log            # Access logs
│   ├── error.log             # Error logs
│   └── info.log              # Info logs
├── main.py                   # FastAPI application entry point
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run.sh                    # Script to run the application
└── tests/                    # Unit and integration tests
    ├── test_api.py           # API endpoint tests
    └── test_rag.py           # RAG pipeline tests
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/news-reporter-ai-backend.git
   cd news-reporter-ai-backend
   ```

2. **Set Up a Conda Environment**: Ensure you have Conda installed. Create and activate a Conda environment with Python 3.10.13:

   ```bash
   conda create -n backend-env python=3.10.13
   conda activate backend-env
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:

   - Copy `config.py` to a `.env` file or set environment variables for sensitive settings (e.g., API keys, database credentials).
   - Example `.env`:

     ```env
     REDIS_HOST=localhost
     REDIS_PORT=6379
     CHROMA_DB_PATH=./app/api/rag/db/knowledge_base
     ```

5. **Run the Application**:

   ```bash
   bash run.sh
   ```

   Alternatively, run directly:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Usage

The backend exposes a FastAPI-based API for the News Reporter AI frontend. Key endpoints include:

- **/api/chat**: Handles user queries, streams verified news responses using the RAG pipeline.
- **/api/health**: Checks the health status of the backend services.

To interact with the API, use the frontend interface or send HTTP requests. Example using `curl`:

```bash
curl -X POST "http://localhost:8000/api/chat" -H "Content-Type: application/json" -d '{"query": "Is the recent earthquake rumor true?"}'
```

## Key Features

- **Real-time News Verification**: Retrieves and verifies news from credible sources using a RAG pipeline.
- **Streaming Responses**: Streams AI-generated responses token-by-token for a seamless user experience.
- **Scalable Architecture**: Built with FastAPI for high performance and asynchronous processing.
- **Vector Store Integration**: Uses ChromaDB for efficient storage and retrieval of news data embeddings.
- **Caching with Redis**: Optimizes query performance with Redis caching.
- **Logging**: Comprehensive logging (`access.log`, `error.log`, `info.log`) for debugging and monitoring.

## How It Works

1. **Query Processing**: User queries are received via the `/api/chat` endpoint (`chat.py`).
2. **Information Retrieval**: The retriever (`retriever.py`) fetches relevant data from the vector store (`vectorstore.py`) using embeddings (`embedding_model.py`).
3. **Response Generation**: The RAG pipeline (`pipeline.py`) combines retrieved data with the language model (`llm.py`) to generate verified responses.
4. **Streaming**: Responses are streamed to the frontend for real-time interaction.

## Development Setup

1. **Install Development Tools**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests**:

   ```bash
   pytest tests/
   ```

3. **Test Models Locally**: Use the Jupyter notebook `cookbook/models_test.ipynb` to experiment with embedding and language models.

4. **Ingest Data**: Run the ingestor (`ingestor.py`) to populate the knowledge base with news data:

   ```bash
   python -m app.api.rag.ingestor
   ```


## Acknowledgements

- Built with FastAPI for the API framework.
- Uses ChromaDB for vector storage.
- Powered by Redis for caching.