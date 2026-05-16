import os
import asyncio
import websockets

async def handler(websocket):
    # Keep the connection open and echo messages back to PenguinMod
    async for message in websocket:
        # CloudLink sends ping/pong and text packets
        await websocket.send(message)

async def main():
    # Grab Render's assigned port environment variable
    port = int(os.environ.get("PORT", 10000))
    
    # Bind to 0.0.0.0 for public access
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # keep running forever

if __name__ == "__main__":
    asyncio.run(main())
