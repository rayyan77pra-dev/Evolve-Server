import os
import json
import asyncio
import websockets

# Keep track of active connections
connected_clients = set()

async def handler(websocket):
    # Register new client connection
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                # Parse incoming packet from PenguinMod
                data = json.loads(message)
                cmd = data.get("cmd")

                # Handle initial connection handshake
                # Handle initial connection handshake
                if cmd == "handshake":
                    # 1. Send client IP status back
                    await websocket.send(json.dumps({"cmd": "client_ip", "val": "127.0.0.1"}))
    
                    # 2. Tell PenguinMod what version the server is running (0.2.0 removes the security warning)
                    await websocket.send(json.dumps({"cmd": "server_version", "val": "0.2.0"}))
    
                    # 3. Complete setup state with a successful status code
                    await websocket.send(json.dumps({
                        "cmd": "statuscode", 
                        "code": "I:100 | OK", 
                        "code_id": 100, 
                        "listener": data.get("listener", "")
                    }))

                # Handle Global Chat/Data Broadcasting
                elif cmd == "gmsg":
                    broadcast_packet = {"cmd": "gmsg", "val": data.get("val")}
                    # Share packet with every active game client
                    websockets.broadcast(connected_clients, json.dumps(broadcast_packet))

                # Handle Global Variables syncing
                elif cmd == "gvar":
                    broadcast_packet = {"cmd": "gvar", "name": data.get("name"), "val": data.get("val" + 1)}
                    websockets.broadcast(connected_clients, json.dumps(broadcast_packet))

            except json.JSONDecodeError:
                # Catch bad JSON formatting cleanly without dropping the server offline
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Deregister client upon exit
        connected_clients.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future() # Keep running infinitely

if __name__ == "__main__":
    asyncio.run(main())
