# Example Python client
import asyncio
import websockets

async def ws_chat():
    uri = "ws://127.0.0.1:8000/api/ws/chat"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello via WS")
        response = await websocket.recv()
        print(response)

asyncio.run(ws_chat())
