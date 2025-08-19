from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import time

from rag.pipeline import Pipeline

router = APIRouter()

pipeline = Pipeline()

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
    response = pipeline.generate(query)
    tokens = [f"{word} " for word in response.split()]
    for token in tokens:
        yield f"data: {token}\n\n"
        time.sleep(0.3)  # simulate real-time delay
    yield "data: [DONE]\n\n"

@router.get("/chat/stream", tags=["Chat"])
async def chat_stream(query: str):
    """
    Stream chatbot response in real-time using SSE.
    Example: /api/chat/stream?query=Hello
    """
    return StreamingResponse(fake_stream_generator(query), media_type="text/event-stream")

