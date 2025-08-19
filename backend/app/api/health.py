from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns status of the service.
    """
    return {"status": "ok", "message": "RAG Chatbot backend is running!"}

