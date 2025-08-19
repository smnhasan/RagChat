from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, health

# Create FastAPI instance
app = FastAPI(title="RAG Chatbot API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to RAG Chatbot Backend!"}
