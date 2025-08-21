from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import time
import os

# Get current working directory
current_dir = os.getcwd()

print("Current Directory:", current_dir)


from .rag.pipeline import Pipeline
from .rag.ingestor import Ingestor

pipeline = Pipeline()
ingestor = Ingestor()


router = APIRouter()

# -------------------------
# Non-WebSocket endpoint
# -------------------------
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    answer: str

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    dummy_answer = f"This is a dummy response for: '{request.query}'"
    return ChatResponse(query=request.query, answer=dummy_answer)

# -------------------------
# WebSocket endpoint
# -------------------------

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            dummy_answer = f"This is a dummy WS response for: '{data}'"
            await websocket.send_text(dummy_answer)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")

# -------------------------
# Streaming endpoint (SSE)
# -------------------------
def fake_stream_generator(query: str):
    """
    Fake generator simulating token-by-token streaming.
    """
    response = pipeline.run(query)
    tokens = [f"{word} " for word in response.split()]
    for token in tokens:
        yield f"data: {token}\n\n"
        time.sleep(0.05)  # simulate real-time delay
    yield "data: [DONE]\n\n"

@router.get("/chat/stream", tags=["Chat"])
async def chat_stream(query: str):
    """
    Stream chatbot response in real-time using SSE.
    Example: /api/chat/stream?query=Hello
    """
    return StreamingResponse(fake_stream_generator(query), media_type="text/event-stream")



def run_ingestion_task():
    """Wrapper for background ingestion with logging & error handling."""
    try:
        result = ingestor.ingest()
        # logger.info(f"Ingestion completed: {result}")
    except Exception as e:
        # logger.error(f"Ingestion failed: {e}")
        pass  # Avoid crashing background thread

# -------------------------
# Ingestor endpoint (GET with Background Task)
# -------------------------
@router.get("/ingest", tags=["Ingest"])
async def ingest_endpoint(background_tasks: BackgroundTasks):
    """
    Trigger ingestion in the background (non-blocking).
    Returns immediately with status message.
    """
    try:
        print(f'Ingestion request is accepted...')
        background_tasks.add_task(run_ingestion_task)
        return JSONResponse(
            content={"status": "started", "message": "Ingestion has been triggered and is running in the background."},
            status_code=202,  # Accepted, since processing is async
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start ingestion: {str(e)}")
    
