from fastapi import FastAPI
from app.api import chat, health

# Create FastAPI instance
app = FastAPI(title="RAG Chatbot API", version="0.1.0")

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to RAG Chatbot Backend!"}
