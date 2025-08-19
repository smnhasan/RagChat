# test_ws_client.py
import asyncio
import websockets

async def ws_chat():
    uri = "wss://chatbot.staging.nascenia.com/api/ws/chat"  # Make sure matches your Nginx endpoint

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server!")

            while True:
                message = input("Enter message to send (or 'exit' to quit): ")
                if message.lower() == "exit":
                    print("Closing connection...")
                    break

                await websocket.send(message)
                response = await websocket.recv()
                print(f"Received: {response}")

    except Exception as e:
        print(f"WebSocket connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(ws_chat())
